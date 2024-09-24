from contextlib import contextmanager
from re import sub
import os, sys
import subprocess
import select
import yaml
import webbrowser
from jinja2 import Environment, FileSystemLoader
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from rich.console import Console

JAPPER_DEV = False


# global console
class Global:
    console = Console()
    devtool_interface = 'cli'


console = Global.console

# jinja2 environment
env = Environment(loader=FileSystemLoader(os.path.dirname(__file__) + '/templates'))

CONFIG_FILENAME = 'japper.yml'
WORKING_DIR = os.getcwd().replace('\\', '/')


class InitConfig:
    # Directories to be created
    DIRS_TO_CREATE = ['app', 'app/assets', 'app/models', 'app/controllers', 'app/views', 'container']


def run_command(cmd, fail_msg=None, print_cmd=False, streaming_output=False, stdout_style=None, stderr_style='red'):
    if print_cmd:
        console.print(f'Running command: {cmd}', style='cyan')

    if Global.devtool_interface == 'forge':
        streaming_output = True
        stdout_style = 'white'
        stderr_style = 'bright_red'

    if streaming_output:
        ret = run_command_with_streaming_output(cmd, stdout_style=stdout_style, stderr_style=stderr_style)
    else:
        ret = os.system(cmd)

    if ret != 0:
        exit_with_msg(fail_msg)
    return ret


def run_command_with_streaming_output(cmd, stdout_style=None, stderr_style='red'):
    if isinstance(cmd, str):
        cmd = ['bash', '-c', cmd]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outputs = {process.stdout: False, process.stderr: False}

    while not all(outputs.values()):
        for fd in select.select([process.stdout, process.stderr], [], [])[0]:
            output = fd.read1()
            if output == b"":
                outputs[fd] = True
            else:
                try:
                    decoded = output.decode().rstrip()
                except UnicodeDecodeError:
                    continue

                if fd == process.stdout:
                    console.print(decoded, style=stdout_style)
                else:
                    console.print(decoded, style=stderr_style)

    return process.poll()


def run_command_with_bottom_msg(cmd, bottom_msg, fail_msg=None, color_err=False):
    if Global.devtool_interface == 'forge':
        return run_command(cmd, fail_msg=fail_msg)

    error_style = 'red' if color_err else 'white'

    with console.status("[bold deep_sky_blue1]" + bottom_msg) as status:
        run_command(cmd, fail_msg=fail_msg, streaming_output=True, stderr_style=error_style)


def save_config(config: dict):
    with open(CONFIG_FILENAME, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)


def load_config():
    if not os.path.exists(CONFIG_FILENAME):
        return None
    with open(CONFIG_FILENAME, 'r') as f:
        return yaml.safe_load(f)


def prompt(text, optional=False, allow_spaces=False, **kwargs):
    """
        Prompt the user for input.

        Parameters:
        text (str): The prompt text.
        optional (bool, optional): Whether the input is optional. Defaults to False.
        allow_spaces (bool, optional): Whether to allow spaces in the input. Defaults to False.

        Returns:
        str: The user's input.
    """
    while True:
        user_input = Prompt.ask(text, **kwargs)
        if not user_input:
            if optional:
                return None
            else:
                console.print('This field is required', style='bold red')
                continue

        if not allow_spaces and ' ' in user_input:
            console.print('This field cannot contain spaces', style='bold red')
            continue

        return user_input


def confirm(text, **kwargs):
    return Confirm.ask(text, **kwargs)


def has_special_chars(s, allow_spaces=False):
    if not s.strip():
        return False
    return not (s.replace(' ', '') if allow_spaces else s).isalnum()


def snake(s):
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()


def camel(s):
    return ''.join([word.capitalize() for word in s.split(' ')])


def to_camel_space(s):
    return ' '.join(word.capitalize() for word in s.replace('_', ' ').replace('-', ' ').split())


def create_file(file_path, content=''):
    with open(file_path, 'w') as f:
        f.write(content)


def add_page(page_name: str, icon: str = None, verbose=False):  # deprecated
    snake_page_name = snake(page_name)
    camel_page_name = camel(page_name)

    file_controller, file_view, file_model = (render_template('app.controllers.__name__.py.jinja2',
                                                              name=snake_page_name,
                                                              page_name=camel_page_name),
                                              render_template('app.views.__name__.py.jinja2',
                                                              name=snake_page_name,
                                                              page_name=camel_page_name),
                                              render_template('app.models.__name__.py.jinja2',
                                                              name=snake_page_name,
                                                              page_name=camel_page_name))
    if verbose:
        console.print(f"Adding page files...\n{file_controller}\n{file_view}\n{file_model}")

    # update __init__.py files
    with open('app/controllers/__init__.py', 'a') as f:
        f.write(f"from .{snake_page_name} import {camel_page_name}Controller\n")
    with open('app/views/__init__.py', 'a') as f:
        f.write(f"from .{snake_page_name} import {camel_page_name}View\n")
    with open('app/models/__init__.py', 'a') as f:
        f.write(f"from .{snake_page_name} import {camel_page_name}Model\n")

    # update app_main.py
    with open('app/app_main.py', 'r') as f:
        lines = f.readlines()

    # add controller
    for i in range(len(lines)):
        if 'from .controllers import' in lines[i]:
            lines[i] = lines[i].replace('from .controllers import',
                                        f'from .controllers import {camel_page_name}Controller,')
            break

    # add page by backtracking from the end of the file
    addpage_code = f"app_main.add_page(name='{page_name}', controller={camel_page_name}Controller()"
    if icon:
        addpage_code += f", icon='{icon}'"
    addpage_code += ')\n'

    line_inserted = None
    for i in range(len(lines)):
        if 'def add_pages(app_main):' in lines[i] and '"""This method is' in lines[i + 1]:
            tab = lines[i][:lines[i].index('def')] + '    '
            # find the end of function to add
            for j in range(i + 2, len(lines)):
                if lines[j][:len(tab)] != tab:
                    lines.insert(j, tab + addpage_code)
                    line_inserted = j
                    break

            if line_inserted is not None:
                break

    with open('app/app_main.py', 'w') as f:
        f.write(''.join(lines))
        f.write('\n')

    if line_inserted is None:
        exit_with_msg(
            "Failed to add the page. Please add the following code to your app_main.py file manually:\n\n"
            + addpage_code)

    if verbose:
        console.print(
            f"Page '{page_name}' added successfully (at app_main.py:{line_inserted}). " +
            "Please check you app_main.py file to make sure the page is added correctly." +
            " If not, please add it manually the following code:", style='bold green')
        console.print(addpage_code)


def render_template(template_name, name=None, names=None, no_file_extension=False, **kwargs):
    template = env.get_template(template_name)
    content = template.render(**kwargs)
    tokens = template_name[:-7].split('.')  # remove .jinja2 and split by .
    if no_file_extension:
        file_path = '/'.join(tokens)
    else:
        file_path = '/'.join(tokens[:-1]) + '.' + tokens[-1]

    if name:
        file_path = file_path.replace('__name__', name)
    elif names:
        for name in names:
            file_path = file_path.replace('__name__', name, 1)

    create_file(file_path, content)

    return file_path


def get_conda_env_list():
    ret = subprocess.run(['conda', 'env', 'list'], capture_output=True)
    envs = ret.stdout.decode('utf-8').split('\n')
    envs = [env.split()[0] for env in envs if env and env[0] != '#']
    return envs


def check_cur_conda_env(app_env_name):
    cur_env = os.environ['CONDA_DEFAULT_ENV']
    if cur_env != app_env_name:
        exit_with_msg(
            f"Please activate the conda environment {app_env_name} first: [white] conda activate {app_env_name}[/white]")


def build_docker_image(env, quiet=False, preview_mode=False):
    console.print('Build the Docker image', style='bold cyan')
    cmd = f'cd container/{env} && docker compose'
    if preview_mode:
        cmd += ' -f docker-compose_preview.yml'
    cmd += ' build'
    if quiet:
        cmd += ' -q'

    run_command_with_bottom_msg(cmd, 'Building the Docker image...'
                                , fail_msg='Failed to build the Docker image'
                                , color_err=True)


def run_japper_app(cmd, verbose, japper_up_msg, check_voila_running, check_jupyter_running):
    # print(cmd)
    log_file = f'{WORKING_DIR}/japper_run.log'
    # clean the log
    with open(log_file, 'w') as f:
        f.write('')

    console.print(f"Starting the app", style='bold cyan')
    if not verbose:
        console.print(
            f"  App running logs are being written to file:///{log_file}\n"
            + "  You can use -v or --verbose option to see the logs.", style='yellow')

    voila_running = not check_voila_running
    jupyter_running = not check_jupyter_running
    app_initialized = False

    with console.status("[bold deep_sky_blue1] Initializing the app running environment...") as status:
        process = subprocess.Popen(['bash', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            text = process.stdout.read1().decode("utf-8")
            if verbose:
                print(text, end='', flush=True)
            else:
                with open(log_file, 'a') as f:
                    f.write(text)
            if not app_initialized:
                if '[Voila] Voilà is running at:' in text:
                    voila_running = True
                if 'Jupyter ' in text and 'is running at:' in text:
                    jupyter_running = True
                if voila_running and jupyter_running:
                    status.update(Panel(japper_up_msg), spinner='dots', speed=0.1)
                    app_initialized = True
                    webbrowser.open('http://localhost:8888')

            if process.poll() is not None:
                break
        ret = process.poll()

    # Check the return code of the process
    if ret != 0 and ret != 33280 and not verbose:
        exit_with_msg(f'Failed to start the app. Please check the logs in file:///{log_file}')

    console.print("App stopped", style='bold yellow')


def get_docker_up_cmd(env, preview_mode):
    cmd = f'cd container/{env} && docker compose'
    if preview_mode:
        cmd += ' -f docker-compose_preview.yml'
    cmd += ' up --remove-orphans'

    return cmd


def exit_with_msg(msg=None, code=-1):
    if msg:
        console.print(msg, style='bold red')

    if Global.devtool_interface == 'forge':
        raise SystemExit(msg)
    else:
        exit(code)


def get_console():
    return Global.console


def set_devtool_interface(interface: str):
    Global.devtool_interface = interface

    if interface == 'forge':
        set_console_theme_monokai()
        Global.console = Console(width=75)
        global console
        console = Global.console


def set_console_theme_monokai():
    from rich.terminal_theme import DEFAULT_TERMINAL_THEME, MONOKAI

    DEFAULT_TERMINAL_THEME.foreground_color = MONOKAI.foreground_color
    DEFAULT_TERMINAL_THEME.background_color = MONOKAI.background_color
    DEFAULT_TERMINAL_THEME.ansi_colors = MONOKAI.ansi_colors


@contextmanager
def chdir(path):
    """Change the current working directory to the given path."""
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)
