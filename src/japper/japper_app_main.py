# to compress new Comm package issue on Sphinx https://github.com/jupyter-widgets/ipywidgets/pull/3533
# import ipykernel.ipkernel  # noqa

from IPython.display import HTML
from IPython.display import display
import ipywidgets as ipyw

from .app_main_view import AppMainView
from . import utils
from .page_controller import PageController
from .debug import is_dev, debug_view, debug
from .widgets import NavigationMenu
from .page import Page
from .style import JapperStyle
from .app_config import load_config, AppConfig


def init_js_output():  # deprecated
    """
    Initialize the output widget for JS. We need this approach to avoid blank space at the bottom of the page when
    new JS is executed.
    """
    output = ipyw.Output(layout={'display': 'none'})
    display(output)
    utils.set_js_output(output)


def inject_files():
    utils.inject_html('global.html')


class JapperAppMain:

    def __init__(self):
        self.nav_menu = None
        self.main_view = None
        self.pages = []
        self.default_page = None

        self.app_config = None

    def init_app(self,
                 app_config: AppConfig = None,
                 custom_html: str = utils.ASSETS_PATH + 'custom.html',
                 mygeohub_tool=False,
                 add_pages=True
                 ):
        """
        Initialize the app

        :param app_config: Configuration of the app
        :param custom_html: Path to the custom HTML file
        :param mygeohub_tool: Set this to True if the app is a MyGeoHub tool
        :param add_pages: Set this to False if you don't want to add pages automatically
        """

        if app_config is None:
            app_config = load_config('app/app_config.yml')
        self.app_config = app_config

        self.main_view = AppMainView(app_config.style)
        utils.set_browser_title(app_config.browser_title)
        if app_config.favicon:
            utils.set_favicon(utils.ASSETS_PATH + app_config.favicon)

        self.add_custom_html(custom_html)

        # if dev mode, show the debug view
        if is_dev():
            debug_view.display_debug_view()

        if mygeohub_tool:
            self.set_appmode()

        if app_config.navigation_menu.enabled:
            self.add_navigation_menu(app_config)

        if add_pages:
            self.add_pages()

    def add_navigation_menu(self, app_config: AppConfig):
        """
        Add the navigation menu

        :param app_config: Configuration of the app
        """

        self.nav_menu = NavigationMenu(
            style=app_config.style.navigation_menu,
            config=app_config.navigation_menu
        )

    def add_page(self,
                 name: str,
                 page_main: callable = None,
                 controller: PageController = None,
                 icon: str = None,
                 page_type: str = 'mvc',
                 default=False,
                 hide_from_menu: bool = False,
                 hide_nav_menu: bool = False,
                 always_render: bool = False):
        """
        Add a page to the app and navigation menu if available

        :param name: Name of the page
        :param controller: Controller of the page
        :param icon: Icon of the page
        :param default: Set this to True if the page is the default page that will be shown when the app starts
        :param hide_from_menu: Set this to True if the page should not be shown in the navigation menu
        :param hide_nav_menu: Set this to True if the navigation menu should be hidden when the page is shown
        :param always_render: Set this to True if the page should be re-rendered every time it is shown
        """
        page = Page(name=name, page_main=page_main, controller=controller, icon=icon, page_type=page_type,
                    hide_from_menu=hide_from_menu,
                    hide_nav_menu=hide_nav_menu, always_render=always_render)
        self.pages.append(page)
        if default:
            self.default_page = page

        if self.nav_menu:
            self.nav_menu.add_menu(page)

    def add_pages(self):
        """
        Add pages to the app based on the configuration
        """
        import importlib.util

        for page_config in self.app_config.pages:
            if (spec := importlib.util.find_spec(f'app.controllers.{page_config.name}')) is not None:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                controller = getattr(module, page_config.controller_name)()
            else:
                controller = None
            self.add_page(name=page_config.title, controller=controller, icon=page_config.icon,
                          default=page_config.default, page_type='mvc')

    def start_app(self, preload_contents=False):
        """
        Start the app
        """

        inject_files()
        if self.nav_menu:
            self.__init_navigation_menu()

        if preload_contents:
            self.__preload_contents()

        self.main_view.render()

        self.__connect_util_funcs()
        display(self.main_view)
        self.show_page(page=self.default_page)

    def show_page(self, page: int | str | Page):
        """
        Show a page by index, name, or page object
        """
        index = -1
        if isinstance(page, int):
            index = page
            self.main_view.set_page(self.pages[index])
        elif isinstance(page, str):
            page_name = page
            for i, page in enumerate(self.pages):
                if page.name == page_name:
                    self.main_view.set_page(page)
                    index = i
                    break
        elif isinstance(page, Page):
            self.main_view.set_page(page)
            index = self.pages.index(page)

        if index != -1 and self.nav_menu:
            self.nav_menu.update_nav_buttons_active_by_index(index)

    def __init_navigation_menu(self):
        self.nav_menu.render()
        self.main_view.set_nav_menu(self.nav_menu)
        self.nav_menu.connect_to_main_view(self.main_view)
        utils.set_nav_menu(self.nav_menu)

    def __preload_contents(self):
        for page in self.pages:
            page.render()

    def add_custom_html(self, filepath):
        display(HTML(filename=filepath))

    def __connect_util_funcs(self):
        """
        Connect utility functions from the main controller
        """
        utils.set_external_funcs(
            self.main_view.loading_dialog.show_loading,
            self.main_view.loading_dialog.hide_loading,
            self.main_view.toast_alert.alert,
            self.show_page,
            self.main_view.popup_alert
        )

    def set_appmode(self):
        utils.inject_html('appmode.html')
