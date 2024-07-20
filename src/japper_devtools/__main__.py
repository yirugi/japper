import os
import subprocess
import rich_click as click
from rich.console import Console

console = Console()

from .project_init import init_project_cli
from .utils import save_config, load_config, build_docker_image, check_cur_conda_env, prompt, confirm, run_command, \
    run_japper_app, get_docker_up_cmd, snake, add_page, JAPPER_DEV, exit_with_msg

WORKING_DIR = os.getcwd().replace('\\', '/')
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_config():
    config = load_config()
    if config is None or 'project_name' not in config:
        exit_with_msg("No project found. Please run 'japper init' first.")

    return config


@click.group()
def cli():
    pass


@click.command(help='Initiate a new Japper project')
@click.option('-mg', '--mygeohub', help="create MyGeoHub Tool structure", default=False, is_flag=True)
def init(mygeohub):
    init_project_cli(mygeohub=mygeohub)


@click.command(help='Run this Japper project')
@click.argument('mode', type=click.Choice(['dev', 'preview', 'prod']))
@click.option('-v', '--verbose', help="verbose mode", default=False, is_flag=True)
def run(mode, verbose):
    """
    Run the project in a specified environment.
    """

    config = get_config()
    run_env = 'docker' if config['dev_env'] == 'docker' else 'local'
    mygeohub = 'mygeohub' in config
    is_preview = mode == 'preview'

    # if config['dev_env'] == 'local':
    #     console.print(
    #         "The project is set to run in manual mode. Please make sure both voila and jupyterlab are installed",
    #         style='bold yellow')

    if mygeohub and mode == 'prod':
        console.print("This is a MyGeoHub Tool. Production mode is not allowed.", style='bold red')
        return

    if run_env == 'local' and mode == 'prod':
        ret = confirm("The production mode will be run in Docker. Do you want to continue?")
        if not ret:
            return
        run_env = 'docker'

    mode_desc = {
        'dev': 'development',
        'preview': 'production preview',
        'prod': 'production'
    }

    console.print(f"Running the project in '{mode_desc[mode]}' mode", style="bold magenta")
    japper_up_msg = f"[green]Japper App [bold magenta]{config['project_title']}[/bold magenta] is running" + \
                    f" \[[white]{mode_desc[mode]},{config['dev_env']}[/white]]\n\n"

    if mygeohub:
        japper_up_msg += " - App:   http://localhost:8888/apps/app.ipynb?appmode_scroll=0"
        check_voila_running = False
        check_jupyter_running = True

        build_docker_image('appmode', quiet=not verbose, preview_mode=is_preview)
        cmd = get_docker_up_cmd('appmode', preview_mode=is_preview)


    else:
        japper_up_msg += " - App:   http://localhost:8888/"
        if mode == 'dev':
            japper_up_msg += "\n - JuptyerLab: http://localhost:8889/lab"

        if run_env == 'docker':
            docker_env = 'prod' if mode == 'prod' else 'dev'
            # Build the docker image
            build_docker_image(docker_env, quiet=not verbose, preview_mode=is_preview)
            cmd = get_docker_up_cmd(docker_env, preview_mode=is_preview)

        elif run_env == 'local':  # conda or manual
            # check env fist for conda env
            if config['dev_env'] == 'conda':
                check_cur_conda_env(config['conda']['env_name'])
            cmd = "voila ./app.ipynb --no-browser --port=8888 --debug --show_tracebacks=True"
            if mode == 'dev':
                cmd = f"""export JAPPER_APP_DEV=1 && {MODULE_DIR}/parallel_cmd.sh "{cmd}" "jupyter lab --allow-root --no-browser --port=8889 --IdentityProvider.token='' --ServerApp.password=''" """
            else:
                cmd = "export JAPPER_APP_DEV=0 && " + cmd

        check_voila_running = True
        check_jupyter_running = mode == 'dev'

    japper_up_msg += "\n\n[yellow]Press Ctrl+C to stop the app"

    run_japper_app(cmd, verbose, japper_up_msg, check_voila_running, check_jupyter_running)


@click.command(help="Build this Japper project")
@click.argument('mode', type=click.Choice(['docker']))
def build(mode):
    config = get_config()

    if mode == 'docker':
        if 'mygeohub' in config:
            console.print("This is a MyGeoHub Tool. No build is required.", style='bold yellow')
            return

        if config['dev_env'] == 'local':
            ret = confirm(
                "The project is set to run in local environment. Do you want to build the production Docker image?")
            if not ret:
                return

        console.print("Building the Docker image in production environment", style='bold cyan')
        build_docker_image('prod')
        console.print(f"Docker image built successfully. Please check the image '{config['project_name']}'",
                      style='bold green')


@click.command(help="Deploy this Japper project")
@click.argument('target', type=click.Choice(['registry']), default='registry')
@click.option('-t', '--tag', help="tag for container image", default='latest')
def deploy(target, tag):
    config = get_config()

    if target == 'registry':
        if 'registry_url' not in config:
            registry_url = prompt("Enter the Docker registry URL", default='docker.io')
            # validate the registry URL
            if registry_url[:4] == 'http':
                registry_url = registry_url.split('//')[1]
            if registry_url[-1] == '/':
                registry_url = registry_url[:-1]

            if registry_url == 'docker.io':
                registry_namespace = prompt("Enter the docker.io username")
            else:
                registry_namespace = prompt("Enter the Docker registry namespace (optional)", optional=True)

            registry_image_name = prompt("Enter the remote image name", default=config['project_name'])

            config['registry_url'] = registry_url
            config['registry_namespace'] = registry_namespace
            config['registry_image_name'] = registry_image_name
            save_config(config)
        else:
            config = load_config()
            registry_url = config['registry_url']
            registry_namespace = config['registry_namespace']
            registry_image_name = config['registry_image_name']

        project_name = config['project_name']

        ret = subprocess.run(['docker', 'images', '-q', config['project_name']], stdout=subprocess.PIPE)
        if ret.stdout.decode('utf-8') == '':
            console.print('No Docker image found. Building the Docker image...')
            build_docker_image('prod')

        console.print("Logging in to the Docker registry...", style='bold cyan')
        run_command(f'docker login {config["registry_url"]}', 'Failed to login to the Docker registry', print_cmd=True)

        console.print("Tagging the Docker image...", style='bold cyan')
        if registry_url == 'docker.io':
            full_image_name = f'{registry_namespace}/{registry_image_name}:{tag}'
        else:
            if registry_namespace:
                full_image_name = f'{registry_url}/{registry_namespace}/{registry_image_name}:{tag}'
            else:
                full_image_name = f'{registry_url}/{registry_image_name}:{tag}'
        run_command(f'docker tag {project_name} {full_image_name}', 'Failed to tag the Docker image', print_cmd=True)

        console.print("Uploading the Docker image to the registry...", style='bold cyan')
        run_command(f'docker push {full_image_name}', 'Failed to upload the Docker image', print_cmd=True)

        console.print(f"Successfully uploaded the Docker image to {full_image_name}", style='bold green')


@click.command(help="Add a new component to this Japper project")
@click.argument('component', type=click.Choice(['page']))
def add(component):
    config = get_config()

    """Handle add subcommand"""
    if component == 'page':
        page_name = prompt("Enter the new page name", allow_spaces=True)
        icon = prompt(
            "Enter the material design icon name (optional) (e.g. mdi-home or home)\n" +
            " (You can check the full list of icons here: https://pictogrammers.github.io/@mdi/font/7.4.47)",
            optional=True)
        if icon and icon[:4] != 'mdi-':
            icon = 'mdi-' + icon

        snake_name = snake(page_name)
        if snake_name == page_name:
            page_msg = f"Page {page_name}"
        else:
            page_msg = f"Page {page_name} ({snake_name})"
        if os.path.exists(f'app/presenters/{snake_name}') or os.path.exists(
                f'app/views/{snake_name}') or os.path.exists(f'app/models/{snake_name}'):
            exit_with_msg(page_msg + " already exists")

        add_page(page_name, icon=icon, verbose=True)


@click.command(help="Generate documentation")
def doc():
    console.print("Generating documentation", style='bold magenta')
    ret = run_command('pdoc --html --config show_source_code=False -o docs --force app ',
                      'Failed to generate documentation')
    console.print("\nDocumentation generated at docs/app/index.html\n"
                  + f"   Open in browser: file:///{WORKING_DIR}/docs/app/index.html", style='bold green')


@click.command(help='Run Japper Forge Web App')
@click.option('-v', '--verbose', help="verbose mode", default=False, is_flag=True)
@click.option('-mg', '--mygeohub', help="create MyGeoHub Tool structure", default=False, is_flag=True)
def forge(verbose, mygeohub):
    cmd = f"export JAPPER_WORKING_DIR=`pwd` && voila {MODULE_DIR}/forge/app.ipynb --port=8890"
    if JAPPER_DEV:
        cmd = f"export JAPPER_APP_DEV=1 && {cmd} --debug --show_tracebacks=True"
        # console.print(cmd)

    japper_up_msg = f"[green]Japper Forge is running\n\n"
    japper_up_msg += " - Japper Forge:   http://localhost:8890/"
    japper_up_msg += "\n\n[yellow]Press Ctrl+C to stop the app"

    run_japper_app(cmd, verbose, japper_up_msg, True, False)


cli.add_command(init)
cli.add_command(run)
cli.add_command(build)
cli.add_command(deploy)
# cli.add_command(add)
cli.add_command(doc)
cli.add_command(forge)


def main():
    cli()


if __name__ == '__main__':
    main()
