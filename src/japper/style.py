"""
JapperStyle defines a set of styles that can be used to style throughout the application.
"""
from typing import ClassVar

from ipyvue import VueWidget
from pydantic import BaseModel, computed_field


class StyleItem(BaseModel):
    def to_style(self):
        return ';'.join(f'{k.replace("_", "-")}:{v}' for k, v in self.dict().items())


class JapperStyle(BaseModel):
    class App(StyleItem):
        pass

    app: App = App()

    class PageWrapper(StyleItem):
        _navigation_menu: ClassVar['JapperStyle.NavigationMenu']
        _nav_mode: str = 'none'
        _height: str = '100vh'
        _width: str = '100%'
        _margin: str = '0 auto'
        overflow_y: str = 'auto'

        # background_color: str = '#fafbfd'

        @computed_field
        def height(self) -> str:
            if self._nav_mode == 'top':
                return f'calc(100vh - {self._navigation_menu.top_navigation.height})'
            return self._height

        @height.setter
        def height(self, value: str):
            self._height = value

        @computed_field
        def width(self) -> str:
            if self._nav_mode == 'side':
                return f'calc(100% - {self._navigation_menu.side_navigation.width})'
            return self._width

        @width.setter
        def width(self, value: str):
            self._width = value

        @computed_field
        def margin(self) -> str:
            if self._nav_mode == 'top':
                return f'{self._navigation_menu.top_navigation.height} auto 0 auto'
            if self._nav_mode == 'side':
                return f'0 0 0 {self._navigation_menu.side_navigation.width}'
            return self._margin

        @margin.setter
        def margin(self, value: str):
            self._margin = value

    page_wrapper: PageWrapper = PageWrapper()

    class Page(StyleItem):
        height: str = '100%'
        padding: str = '30px'
        background_color: str = '#fafbfd'
        # max_width: str = '1400px'
        # margin: str = '0 auto'

    page: Page = Page()

    class PageWithTopNavigation(StyleItem):
        max_width: str = '1400px'
        margin: str = '0 auto'

    page_with_top_navigation: PageWithTopNavigation = PageWithTopNavigation()

    class PageWithSideNavigation(StyleItem):
        max_width: str = '100%'

    page_with_side_navigation: PageWithSideNavigation = PageWithSideNavigation()

    class NavigationMenu(BaseModel):
        class Icon(StyleItem):
            color: str = 'rgb(42, 53, 71)'

        icon: Icon = Icon()

        class Logo(StyleItem):
            width: str = '32px'
            height: str = '32px'

        logo: Logo = Logo()

        class Title(StyleItem):
            font_weight: str = '500'
            font_size: str = '1.4rem'
            text_wrap: str = 'wrap'

        title: Title = Title()

        class SideNavigation(StyleItem):
            width: str = '230px'
            padding: str = '10px'

        side_navigation: SideNavigation = SideNavigation()

        class TopNavigation(StyleItem):
            _page: ClassVar['JapperStyle.PageWithSideNavigation']
            height: str = '80px'
            width: str = '100%'
            position: str = 'fixed'
            z_index: str = '10'
            background_color: str = '#ffffff'
            border_bottom: str = '1px solid #e0e0e0'

            @computed_field
            def padding(self) -> str:
                return f'calc(({self.height} - 64px)/2) calc((100% - {self._page.max_width}) / 2)'

        top_navigation: TopNavigation = TopNavigation()

    navigation_menu: NavigationMenu = NavigationMenu()

    def __init__(self, **data):
        super().__init__(**data)
        self.PageWrapper._navigation_menu = self.navigation_menu
        self.navigation_menu.TopNavigation._page = self.page_with_top_navigation

    def get_nav_mode(self):
        return self.page_wrapper._nav_mode


"""
Adding util functions to VueWidget 
"""


def set_style(self, style: str):
    """
    This method is used to set or update the style of a VueWidget instance.

    Parameters:
    style (str): A string representing the style to be set or updated. The string should be in the format 'key:value;'

    Example:
    set_style('color:red; font-size:14px;')

    Note:
    If the style property already exists, its value will be updated with the new value provided. If the style property does
    not exist, it will be added to the style of the VueWidget instance.
    """
    if not self.style_ or self.style_.strip() == '':
        self.style_ = style
        return

    styles = {s.split(':')[0]: s.split(':')[1] for s in self.style_.split(';') if s.strip() != ''}
    new_styles = {s.split(':')[0]: s.split(':')[1] for s in style.split(';') if s.strip() != ''}

    styles.update(new_styles)
    self.style_ = ';'.join(f'{k}:{v}' for k, v in styles.items())


def get_style(self, key: str):
    """
    This method is used to get the value of a specific style property of a VueWidget instance.

    Parameters:
    key (str): A string representing the style property to get the value of.

    Returns:
    str: The value of the style property if it exists, otherwise None.

    Example:
    get_style('color')

    Note:
    If the style property does not exist, None will be returned.
    """
    if not self.style_ or self.style_.strip() == '':
        return None

    styles = {s.split(':')[0]: s.split(':')[1] for s in self.style_.split(';') if s.strip() != ''}
    return styles.get(key, None)


VueWidget.set_style = set_style
VueWidget.get_style = get_style
