"""
JapperStyle defines a set of styles that can be used to style throughout the application.
"""
from ipyvue import VueWidget


class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class StyleItem:
    @classmethod
    def to_dict(cls):
        styles = {}
        for base in cls.__bases__:
            if base != StyleItem:
                styles.update(base.to_dict())

        for k, v in cls.__dict__.items():
            if k.startswith('__') or callable(getattr(cls, k)):
                continue
            if isinstance(v, classproperty):
                v = v.fget(cls)
            styles[k.replace("_", "-")] = v

        return styles

    @classmethod
    def to_style(cls):
        styles = cls.to_dict()
        return ';'.join(f'{k}:{v}' for k, v in styles.items())


class JapperStyle:
    class App(StyleItem):
        pass

    class PageWrapper(StyleItem):
        pass

    class PageWrapperDefault(StyleItem):
        overflow = 'auto'
        width = '100%'
        height = '100vh'
        background_color = '#fafbfd'
        margin = '0 auto'

    page_wrapper: PageWrapper = PageWrapperDefault

    class PageWrapperTopNav(PageWrapperDefault):
        @classproperty
        def height(cls):
            return f'calc(100vh - {JapperStyle.NavigationMenu.TopNavigation.height})'

        @classproperty
        def margin(cls):
            return f'{JapperStyle.NavigationMenu.TopNavigation.height} auto 0 auto'

    page_wrapper_top_nav: PageWrapper = PageWrapperTopNav

    class PageWrapperSideNav(PageWrapperDefault):
        @classproperty
        def width(cls):
            return f'calc(100% - {JapperStyle.NavigationMenu.SideNavigation.width})'

        @classproperty
        def margin(cls):
            return f'0 0 0 {JapperStyle.NavigationMenu.SideNavigation.width}'

    page_wrapper_side_nav: PageWrapper = PageWrapperSideNav

    class Page(StyleItem):
        height = '100%'
        padding = '20px 0'
        max_width = '1400px'
        margin = '0 auto'
        background_color = '#fafbfd'

    page: Page = Page

    class NavigationMenu:
        class Icon(StyleItem):
            color = 'rgb(42, 53, 71)'

        icon: Icon = Icon

        class Logo(StyleItem):
            width = '32px'
            height = '32px'

        logo: Logo = Logo

        class Title(StyleItem):
            font_weight = '500'
            font_size = '1.4rem'
            text_wrap = 'wrap'

        title: Title = Title

        class SideNavigation(StyleItem):
            width = '230px'

        side_navigation: SideNavigation = SideNavigation

        class TopNavigation(StyleItem):
            height = '80px'
            width = '100%'
            position = 'fixed'
            z_index = '10'
            background_color = '#ffffff'
            border_bottom = '1px solid #e0e0e0'

            @classproperty
            def padding(cls):
                return f'calc(({cls.height} - 64px)/2) calc((100% - {JapperStyle.Page.max_width}) / 2)'

        top_navigation: TopNavigation = TopNavigation

    navigation_menu: NavigationMenu = NavigationMenu


"""
Styles need to be set after class definition
"""

# JapperStyle.PageWrapperTopNav.height = f'calc(100vh - {JapperStyle.NavigationMenu.TopNavigation.height})'
# JapperStyle.PageWrapperTopNav.margin = f'{JapperStyle.NavigationMenu.TopNavigation.height} auto 0 auto'

# JapperStyle.PageWrapperSideNav.width = f'calc(100% - {JapperStyle.NavigationMenu.SideNavigation.width})'
# JapperStyle.PageWrapperSideNav.margin = f'0 0 0 {JapperStyle.NavigationMenu.SideNavigation.width}'

JapperStyle.PageWrapper = JapperStyle.PageWrapperDefault

# JapperStyle.NavigationMenu.TopNavigation.padding = f'0 calc((100% - {JapperStyle.PageTopNav.width}) / 2)'
# JapperStyle.NavigationMenu.TopNavigation.padding = \
#     f'calc(({JapperStyle.NavigationMenu.TopNavigation.height} - 64px)/2) calc((100% - {JapperStyle.Page.max_width}) / 2)'

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
