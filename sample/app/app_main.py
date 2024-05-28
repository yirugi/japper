"""
Main class of the app.
"""

from japper import JapperAppMain
from japper.widgets import NavigationMenuItem
from .presenters import HomePresenter, WidgetsPresenter, FeaturesPresenter
from .commons.config import Config


class AppMain(JapperAppMain):

    def __init__(self):
        """
        Create a new instance of AppMain. This is the main class of the app. It extends JapperAppMain, and it is used to
        create the navigation menu and start the app.
        """
        super().__init__(page_title=Config.APP_NAME, favicon_path=Config.ICON_PATH)

        # init presenters
        self.home_presenter = HomePresenter()
        self.widgets_presenter = WidgetsPresenter()
        self.features_presenter = FeaturesPresenter()

        # create navigation menu
        self.create_navigation_menu(mode='top',  # mode can be 'top' or 'side'
                                    title=Config.APP_NAME,
                                    logo=Config.ICON_PATH,
                                    items=[
                                        NavigationMenuItem(title='Home', icon='mdi-home',
                                                           content_presenter=self.home_presenter),
                                        NavigationMenuItem(title='Widgets', icon='mdi-widgets',
                                                           content_presenter=self.widgets_presenter),
                                        NavigationMenuItem(title='Features', icon='mdi-flash',
                                                           content_presenter=self.features_presenter),
                                    ])

    def start(self):
        """
        Start the app
        """
        super().start()
        self.nav_menu.move_to(0)  # show the first menu item
