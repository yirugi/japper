import os, yaml
from .style import JapperStyle

from pydantic import BaseModel, Field, computed_field


class AppConfig(BaseModel):
    _config_path: str | None = None
    favicon: str | None = Field(None, title='Favicon',
                                description="Favicon filename in assets folder. Only PNG format is supported")
    browser_title: str | None = Field(None, title='Browser Title', description="Title of the browser tab")
    # show_navigation_menu: bool = Field(True, title='Show Navigation Menu',
    #                                    description="Show or hide the navigation menu")
    mygeohub_tool: bool = Field(False, title='MyGeoHub Tool',
                                description="Enable MyGeoHub tool mode")

    class NavigationMenu(BaseModel):
        _style: JapperStyle
        enabled: bool = True
        logo: str | None = Field(None, title='Logo', description="Logo filename in assets folder")
        title: str | None = Field(None, title='Title', description="Title of the navigation menu")
        _mode: str = 'top'

        @computed_field
        def mode(self) -> str:
            return self._mode

        @mode.setter
        def mode(self, value):
            self._mode = value
            self._style.page_wrapper._nav_mode = value

    navigation_menu: NavigationMenu = NavigationMenu()

    class Page(BaseModel):
        class Template(BaseModel):
            name: str = 'blank'
            data: dict | None = {}

        name: str = ''
        controller_name: str | None = None
        title: str
        icon: str = ''
        default: bool = False
        hide_from_menu: bool = False
        hide_nav_menu: bool = False
        always_render: bool = False
        template: Template = Template()

    pages: list[Page] = []

    style: JapperStyle = JapperStyle()

    def __init__(self, config_path=None, **data):
        super().__init__(**data)
        self._config_path = config_path

        self.navigation_menu._style = self.style
        if 'navigation_menu' in data and 'mode' in data['navigation_menu']:
            # since the mode setter is not called by pydantic
            self.navigation_menu.mode = data['navigation_menu']['mode']

    def save(self, path: str = None):
        if path is None:
            if self._config_path is None:
                raise ValueError("Config path is not set")
            path = self._config_path

        with open(path, 'w') as file:
            yaml.dump(self.dict(), file)

    @classmethod
    def from_yaml(cls, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(path, 'r') as file:
            data = yaml.safe_load(file)

        return cls(config_path=path, **data)


config = None


def load_config(yaml_config_path: str):
    global config
    config = AppConfig.from_yaml(yaml_config_path)
    return config


def set_config(app_config: AppConfig):
    global config
    config = app_config


def app_config():
    return config


def app_style():
    return app_config().style


def get_page_template_config(page_title: str):
    for page in app_config().pages:
        if page.title == page_title:
            return page.template.data

    return {}

# yaml_config = """
# app_name: 'Japper App'
# favicon_path: 'favicon.ico'
# show_navigation_menu: true
#
# navigation_menu:
#     mode: 'top'
#     logo_file: 'logo.png'
#     title: 'Japper App'
#
# style:
#     page_wrapper:
#         background_color: 'red'
#         # navigation_menu:
#         #     icon:
#         #         color: 'black'
#         #     logo:
#         #         width: '64px'
# """
#
# # config = AppConfig()
#
# config = AppConfig.parse_obj(yaml.safe_load(io.StringIO(yaml_config)))
# print(app_config().style.page_wrapper.to_style())
