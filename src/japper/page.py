from enum import Enum

from .page_controller import PageController


class PageType(str, Enum):
    MVC = 'mvc'
    SIMPLE = 'simple'
    CONVENTIONAL = 'conventional'


class Page:
    def __init__(self, name: str,
                 page_main: callable = None,
                 controller: PageController | None = None,
                 icon: str | None = None,
                 page_type: PageType = PageType.MVC,
                 hide_from_menu: bool = False,
                 hide_nav_menu: bool = False,
                 always_render: bool = False):

        # if page_main is None and controller is None:
        #     raise ValueError("Either page_main or controller must be provided")

        self.name = name
        self.page_main = page_main
        self.controller = controller
        self.icon = icon
        self.rendered = False
        self.page_type = page_type
        self.always_render = always_render
        self.hide_from_menu = hide_from_menu
        self.hide_nav_menu = hide_nav_menu

        self.simple_page_view = None
        self.simple_page_output = None

    def render(self):
        if self.rendered and not self.always_render:
            return

        if self.page_type == PageType.MVC:
            self.controller.view.clear_contents()
            self.controller.render()

        elif self.page_type == PageType.CONVENTIONAL:
            import ipywidgets as ipyw
            from japper import PageView

            self.always_render = True

            if self.simple_page_view is None:
                self.simple_page_view = PageView()
                self.simple_page_output = ipyw.Output()
                self.simple_page_view.set_contents(self.simple_page_output)
            else:
                self.simple_page_output.clear_output()

            with self.simple_page_output:
                self.page_main()
        elif self.page_type == PageType.SIMPLE:
            from japper import PageView

            if self.simple_page_view is None:
                self.simple_page_view = PageView()
            else:
                self.simple_page_view.clear_contents()

            self.page_main(self.simple_page_view.add_contents)

        self.rendered = True

    def content(self):
        self.render()

        if self.page_type == 'mvc':
            return self.controller.get_content()
        elif self.page_type == 'simple':
            return self.simple_page_view
