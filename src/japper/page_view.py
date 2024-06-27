import ipyvuetify as v
import ipywidgets as ipyw

from .style import set_style
from .japper_events import JapperEvents
from .app_config import app_style


class PageView(v.Content, JapperEvents):
    set_style = set_style  # just to suppress the warning

    def __init__(self, custom_app_style=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._japper_events = {}
        _app_style = custom_app_style if custom_app_style is not None else app_style()

        self.set_style(_app_style.page.to_style())
        if _app_style.get_nav_mode() == 'top':
            self.set_style(_app_style.page_with_top_navigation.to_style())
        elif _app_style.get_nav_mode() == 'side':
            self.set_style(_app_style.page_with_side_navigation.to_style())

    def render(self, **kwargs):
        assert False, 'render method is Not implemented'

    def clear_contents(self):
        self.children = []

    def set_contents(self, content: v.VuetifyWidget | ipyw.Widget | str | list[v.VuetifyWidget | ipyw.Widget | str]):
        self.children = content if isinstance(content, list) else [content]

    def add_contents(self, content: v.VuetifyWidget | ipyw.Widget | str | list[v.VuetifyWidget | ipyw.Widget | str]):
        self.children = self.children + content if isinstance(content, list) else [content]
