"""
This is a sample view for the home page.
"""
import ipyvuetify as v
from japper import BaseView
from japper.utils import get_nav_menu


class HomeView(BaseView):
    def __init__(self) -> None:
        """
        Create a new instance of HomeView. This is the view for the home page.
        """
        super().__init__()

    def render(self):
        """
        Render the view. This method is called by the framework to render the view.
        """

        btn_start = v.Btn(color='primary', children=['GET STARTED'], class_='mt-10', large=True)
        btn_start.on_event('click', lambda *_: get_nav_menu().move_to(1))

        self.children = [
            v.Row(class_='align-center justify-center', style_='width:1200px;height:60vh;margin:50px auto;',
                  children=[
                      v.Col(cols=7, children=[
                          v.Html(tag='div', children=[
                              v.Html(tag='p',
                                     class_='display-2 font-weight-bold',  # we can specify class directly
                                     children=['Welcome to Japper Sample App!']),
                              v.Html(tag='p', style_='font-size:1.2em;',  # we can also specify class style
                                     children=["""
                                     This is a sample app to demonstrate how to use Japper for building
                                      Jupyter-based web apps. It provides various useful features and custom
                                      widgets for easier and faster app development.
                                     """]),
                              btn_start
                          ]),
                      ]),
                      v.Col(cols=4, children=[
                          v.Img(src='/app/assets/logo.png', style_='width: 80%;')
                      ]),
                  ]),
        ]
