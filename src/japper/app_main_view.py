import ipyvuetify as v

from .widgets import LoadingDialog, ToastAlert
from .style import JapperStyle, set_style
from .debug import is_dev, debug


class AppMainView(v.App):
    set_style = set_style  # just to suppress the warning

    def __init__(self, app_style: JapperStyle, **kwargs):
        super().__init__(**kwargs)
        self.toast_alert = None
        self.loading_dialog = None
        self.page_wrapper = None
        self.nav_menu = None
        self.app_style = app_style
        self.style_ = app_style.app.to_style()

    def set_nav_menu(self, nav_menu):
        self.nav_menu = nav_menu
        self.children = [self.nav_menu.view] + self.children

    def render(self):
        self.page_wrapper = self.make_page_wrapper()
        self.loading_dialog = LoadingDialog()
        self.toast_alert = ToastAlert(self)

        self.children = [
            self.nav_menu.view if self.nav_menu is not None else '',
            self.page_wrapper,
            self.loading_dialog
        ]

        # if is_dev():
        #     self.style_ += 'padding-bottom: 60px;'

    def make_page_wrapper(self):
        page_wrapper = v.Html(
            tag='div',
            children=[])
        page_wrapper.style_ = self.app_style.page_wrapper.to_style()
        return page_wrapper

    def set_page(self, page):
        if page.hide_nav_menu:
            self.nav_menu.view.hide()
            self.app_style.page_wrapper._nav_mode = 'none'
        else:
            self.nav_menu.view.show()
            self.app_style.page_wrapper._nav_mode = self.nav_menu.mode
        self.page_wrapper.style_ = self.app_style.page_wrapper.to_style()

        content = page.content()
        bg_color = content.get_style('background-color')
        if bg_color is not None:
            self.page_wrapper.set_style(f'background-color: {bg_color};')

        # self.page_wrapper.set_style
        self.page_wrapper.children = [content]
