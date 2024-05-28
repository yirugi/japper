"""
global configurations
"""
import os


class Config:
    APP_NAME = 'Japper Forge'
    #: path to the icon. This will be used as the favicon and the navigation menu logo.
    ICON_PATH = 'app/assets/icon.png'
    #: path to the logo image. This will be used as the logo in the home page.
    LOGO_PATH = 'app/assets/logo.png'
    LOADING_ICON = 'app/assets/console_loading.gif'
    SUCCESS_ICON = 'app/assets/success.png'
    ERROR_ICON = 'app/assets/error.png'

    PAGE_TEMPLATES_PATH: str = './page_templates'

    JAPPER_WORKING_DIR = os.getenv('JAPPER_WORKING_DIR')
    LINKED_WORKING_DIR = 'linked_working_dir'
    LINKED_ASSETS_PATH = LINKED_WORKING_DIR + '/app/assets/'
