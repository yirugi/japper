import os
import yaml
import importlib
from japper import JapperStyle
from jinja2 import Environment, FileSystemLoader

from japper.debug import debug
from japper_devtools.utils import snake, camel
from .config import Config
from japper.app_config import AppConfig


def get_japper_config() -> dict | None:
    # check if japper config exists
    japper_config_path = os.path.join(Config.JAPPER_WORKING_DIR, 'japper.yml')

    if not os.path.exists(japper_config_path):
        return None

    with open(japper_config_path, 'r') as f:
        return yaml.safe_load(f)


def get_app_config_path() -> str:
    return os.path.join(Config.JAPPER_WORKING_DIR, 'app', 'app_config.yml')


def get_app_config() -> (AppConfig, dict):
    # check if app config exists
    app_config_path = get_app_config_path()

    if not os.path.exists(app_config_path):
        return None, None

    with open(app_config_path, 'r') as file:
        config_dict = yaml.safe_load(file)

    return AppConfig.from_yaml(app_config_path), config_dict


def save_app_config_dict(app_config_dict: dict):
    with open(get_app_config_path(), 'w') as file:
        yaml.dump(app_config_dict, file)


def link_working_dir():
    if os.path.islink(Config.LINKED_WORKING_DIR):
        os.unlink(Config.LINKED_WORKING_DIR)

    os.symlink(Config.JAPPER_WORKING_DIR, Config.LINKED_WORKING_DIR)


def get_page_templates():
    # page_templates_path = os.path.join(Config.JAPPER_WORKING_DIR, 'page_templates')

    if not os.path.exists(Config.PAGE_TEMPLATES_PATH):
        return []

    page_templates = []
    with open(os.path.join(Config.PAGE_TEMPLATES_PATH, 'templates.yml'), 'r') as file:
        page_templates = yaml.safe_load(file)['templates']

    page_template_configs = []
    for page_template in page_templates:
        template_path = os.path.join(Config.PAGE_TEMPLATES_PATH, page_template)

        with open(os.path.join(template_path, 'config.yml'), 'r') as file:
            page_template_configs.append(yaml.safe_load(file))

    return page_template_configs


def get_raw_page_template_settings(template_name: str):
    template_path = os.path.join(Config.PAGE_TEMPLATES_PATH, template_name)

    with open(os.path.join(template_path, 'config.yml'), 'r') as file:
        return yaml.safe_load(file).get('settings', None)


def get_default_page_template_settings(template_name: str):
    template_settings = get_raw_page_template_settings(template_name)

    if template_settings is None:
        return None

    default_settings = {}

    def get_default(current_settings, setting):
        if setting['type'] in ['section', 'switch_section']:
            current_settings.setdefault(setting['name'], {})
            if setting['type'] == 'switch_section':
                current_settings[setting['name']]['enabled'] = setting['enabled_default']
            for fields in setting['fields']:
                get_default(current_settings[setting['name']], fields)
        else:
            current_settings.setdefault(setting['name'], setting['default'])

    for setting in template_settings:
        get_default(default_settings, setting)

    return default_settings


def fill_and_get_page_template_settings(page_title: str, template_name: str, config_data: dict):
    def prepare_setting(setting, parent_name=None):
        attribute_name = parent_name + '.' + setting['name'] if parent_name is not None else setting['name']
        setting['name'] = {'setting_name': 'pages', 'page_title': page_title, 'attribute': attribute_name}
        if setting['type'] in ['section', 'switch_section']:
            for fields in setting['fields']:
                prepare_setting(fields, attribute_name)

    def fill_value(setting, data, parent_name=None):
        # data_item = data.get(setting['name'], None)
        data_item = data[setting['name']]

        attribute_name = parent_name + '.' + setting['name'] if parent_name is not None else setting['name']
        setting['name'] = {'setting_name': 'pages', 'page_title': page_title, 'attribute': attribute_name}

        if setting['type'] in ['section', 'switch_section']:
            if setting['type'] == 'switch_section':
                setting['enabled'] = data_item['enabled']
            for fields in setting['fields']:
                fill_value(fields, data_item, attribute_name)
        else:
            setting['value'] = data_item

    template_settings = get_raw_page_template_settings(template_name)

    # 'name': {'setting_name': 'pages', 'page_title': page.title,
    #                                                  'attribute': 'icon'},
    if template_settings is not None:
        for setting in template_settings:
            fill_value(setting, config_data, 'template.data')
            # prepare_setting(setting, 'template.data')

        # for setting in template_settings:
        #     fill_value(setting, config_data)

    return template_settings


def check_page_file_exists(page_title) -> (bool, str):
    snake_page_name = snake(page_title)
    PAGE_TEMPLATE_TYPES = ['controller', 'model', 'view']

    for template_type in PAGE_TEMPLATE_TYPES:
        output_filename = os.path.join(Config.JAPPER_WORKING_DIR, 'app', template_type + 's', f'{snake_page_name}.py')
        if os.path.exists(output_filename):
            return True, os.path.join(template_type + 's', f'{snake_page_name}.py')

    return False, ''


def add_page(page_title, template_name):
    page_file_exists, _ = check_page_file_exists(page_title)
    if page_file_exists:
        raise ValueError(f"Page with title '{page_title}' already exists")

    snake_page_name = snake(page_title)
    camel_page_name = camel(page_title)

    # render and write template files
    PAGE_TEMPLATE_TYPES = ['controller', 'model', 'view']
    template_path = os.path.join(Config.PAGE_TEMPLATES_PATH, template_name)

    env = Environment(loader=FileSystemLoader(os.path.join(template_path, 'src')))
    for template_type in PAGE_TEMPLATE_TYPES:
        output_filename = os.path.join(Config.JAPPER_WORKING_DIR, 'app', template_type + 's', f'{snake_page_name}.py')

        template = env.get_template(f'{template_type}.py.jinja2')
        rendered = template.render(page_name=snake_page_name, PageName=camel_page_name, page_title=page_title)

        with open(output_filename, 'w') as file:
            file.write(rendered)

    template_default_settings = get_default_page_template_settings(template_name)

    _, app_config_dict = get_app_config()

    new_page_config_dict = {
        'title': page_title,
        'name': snake_page_name,
        'controller_name': f'{camel_page_name}Controller',
        'template': {
            'name': template_name,
            'data': template_default_settings
        }
    }

    app_config_dict['pages'].append(new_page_config_dict)
    save_app_config_dict(app_config_dict)

    return new_page_config_dict


def delete_page(page_title):
    snake_page_name = snake(page_title)
    _, app_config_dict = get_app_config()

    for i, page in enumerate(app_config_dict['pages']):
        if page['title'] == page_title:
            del app_config_dict['pages'][i]
            break

    save_app_config_dict(app_config_dict)

    PAGE_TEMPLATE_TYPES = ['controller', 'model', 'view']
    for template_type in PAGE_TEMPLATE_TYPES:
        output_filename = os.path.join(Config.JAPPER_WORKING_DIR, 'app', template_type + 's', f'{snake_page_name}.py')
        if os.path.exists(output_filename):
            os.remove(output_filename)


def render_page_template_preview(page: AppConfig.Page, preview_app_style: JapperStyle):
    # if page.template.name == 'blank':
    #     return ''

    PAGE_TEMPLATE_TYPES = ['controller', 'model', 'view']
    template_path = os.path.join(Config.PAGE_TEMPLATES_PATH, page.template.name)

    rendered_pages = {}
    env = Environment(loader=FileSystemLoader(os.path.join(template_path, 'src')))
    for template_type in PAGE_TEMPLATE_TYPES:
        template = env.get_template(f'{template_type}.py.jinja2')
        rendered = template.render(page_name='template_preview', PageName='TemplatePreview', page_title=page.title,
                                   preview=True)
        rendered_pages[template_type] = rendered

    preview_code = f"""
template_data = None
app_style = None
def get_page_template_config(_):
    return template_data

{rendered_pages['model']}
{rendered_pages['view']}
{rendered_pages['controller']}

#ASSETS_PATH = '{Config.LINKED_ASSETS_PATH}'
ASSETS_PATH = ''

def render(_template_data, _app_style):
    global template_data, app_style
    template_data = _template_data
    app_style = _app_style

    controller = TemplatePreviewController()
    controller.render()
    
    return controller.get_content()
    """

    # debug(preview_code)

    output_filename = './tmp_preview.py'
    with open(output_filename, 'w') as file:
        file.write(preview_code)

    importlib.reload(importlib.import_module('tmp_preview'))
    preview_render = getattr(importlib.import_module('tmp_preview'), 'render')

    return preview_render(page.template.data, preview_app_style)
