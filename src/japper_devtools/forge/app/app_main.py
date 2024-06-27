from japper import JapperAppMain
from .controllers import HomeController, NewProjectController, CustomizeProjectController
from .commons.config import Config
from japper.utils import show_page

from .commons.utils import get_japper_config, link_working_dir


def add_pages(app_main):
    """This method is automatically generated by Japper. It is used to add pages to the app."""
    app_main.add_page(name='home', controller=HomeController(), default=True, hide_from_menu=True,
                      always_render=True)
    app_main.add_page(name='new project', controller=NewProjectController(), hide_from_menu=True)
    app_main.add_page(name='customize project', controller=CustomizeProjectController(), hide_from_menu=True,
                      hide_nav_menu=True, always_render=True)


class AppMain(JapperAppMain):
    def __init__(self):
        super().__init__()
        link_working_dir()

    def start(self):
        self.init_app()

        add_pages(self)

        self.start_app(preload_contents=False)
        # show_page('new project')
        # show_page('customize project')


"""
export JAPPER_APP_DEV=1 && export JAPPER_WORKING_DIR=/Users/yirugi/mycloud/rcac/japper/workspace/japper/test/toto && voila app.ipynb --port=8890 --debug --show_tracebacks=True
"""
