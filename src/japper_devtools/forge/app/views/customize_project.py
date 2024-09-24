import ipyvuetify as v
import ipywidgets as ipyw
import copy
from japper import PageView, AppMainView, Page
from japper.debug import debug
from japper.japper_events import JapperEvents
from japper.style import JapperStyle
from japper.widgets import NavigationMenu
from japper.app_config import AppConfig

from ..commons.config import Config
from ..commons.utils import render_page_template_preview
from ..widgets import AddPageDialog
from .settings_component import create_settings_components, update_page_list, update_page_settings

from traitlets import Unicode, link


class CustomizeProjectView(PageView):
    navigation_menu_title = Unicode('').tag(sync=True)

    def __init__(self) -> None:
        super().__init__()
        self.add_page_dialog = None
        self.page_settings = None
        self.btn_save_changes = None
        self.preview_app = None
        self.preview_browser_tab = None
        self.set_style('padding:0px;max-width:100%;')

        self._japper_events = {}

        self.side_bar = None
        self.setting_panel_wrapper = None
        self.setting_panels = {}
        self.preview = ''
        self.app_preview = None

        self.selected_page = 0

        self.img_inputs = {}

    def create_settings_panel(self, setting_panels_info: list):
        for info in setting_panels_info:
            contents = [
                v.Html(tag='p', class_='mb-0', style_='font-size: 1.3em;font-weight: 500;', children=[info['title']]),
                v.Html(tag='p', style_='color:grey;', children=[info['description']]),
                v.Divider(class_="my-4")
            ]
            for components in info['components']:
                contents += create_settings_components(components, self)

            self.setting_panels[info['name']] = v.Container(
                children=contents
            )

        self.setting_panel_wrapper = v.Col(
            class_='',
            style_='min-width:250px;max-width:400px;background-color: #fafbfd; padding: 20px 20px; '
                   'border-right: 1px solid #bebebe;height: 100%;overflow-y: auto;',
            children=[])

    def update_preview_app(self, app_config: AppConfig, page_index=None):
        if page_index is None:
            page_index = self.selected_page
        else:
            self.selected_page = page_index

        app = AppMainView(app_config.style)

        # navigation menu
        # nav_menu_section = ''
        if app_config.navigation_menu.enabled:
            nav_menu = NavigationMenu(
                style=app_config.style.navigation_menu,
                config=app_config.navigation_menu,
                assets_path=Config.LINKED_ASSETS_PATH
            )
            nav_menu.logo_src = self.img_inputs[
                'navigation_menu.logo'].img_preview.src if app_config.navigation_menu.logo else None

            for page in app_config.pages:
                nav_menu.add_menu(
                    Page(name=page.title, controller=None, icon=page.icon, hide_from_menu=page.hide_from_menu))
            nav_menu.render()
            # nav_menu_section = nav_menu.view

            app.set_nav_menu(nav_menu)

        app.render()
        self.preview_app.children = [app]

        if len(app_config.pages) == 0:
            app.page_wrapper.set_style('height: 80vh;')
            return

        page_config = copy.deepcopy(app_config.pages[page_index])

        # replace image file source to src from img_input
        # pages.Home.template.data.image.file
        for component_name, img_input in self.img_inputs.items():
            name_tokens = component_name.split('.')
            if name_tokens[0] == 'pages':
                page_title = name_tokens[1]
                if page_title == page_config.title:
                    img_field_name = name_tokens[4]
                    src = ''
                    if img_input.file_info is not None:
                        src = img_input.img_preview.src
                    page_config.template.data[img_field_name]['file'] = src

        app.set_page(page_config, content=render_page_template_preview(page_config, app_config.style))
        app.page_wrapper.set_style('height: 80vh;')

    def update_preview_browser_tab(self, app_config: AppConfig):
        favicon = ''
        if app_config.favicon:
            favicon = v.Img(width='16px', height='16px', class_='mr-2',
                            src=self.img_inputs['favicon'].img_preview.src)

        self.preview_browser_tab.children = [
            favicon,
            app_config.browser_title,
        ]

    def create_preview(self):
        self.preview_app = v.Html(tag='div', children=[])

        # self.app_preview = AppMainView(AppConfig().style)
        #
        # self.app_preview.set_nav_menu(self.nav_menu)
        # self.app_preview.render()

        # self.preview = v.Content(
        #     children=[
        #         self.nav_menu.view,
        #         # v.Container(
        #         #     class_='d-flex flex-row align-center justify-center',  # todo: add left or top margin
        #         #     style_='height: 80vh;',
        #         #     children=[
        #         #         v.Html(tag='div', children=['Page Content Here...'])
        #         #     ]
        #         # )
        #     ]
        # )

        self.preview_browser_tab = v.Html(
            tag='div',
            class_="",
            style_="""
                    display: flex;
                    align-items: center;
                    position: absolute;
                    top: -35px;
                    height: 35px;
                    left: -1px;
                    padding: 5px 30px;
                    border: 1px solid #aaaaaa;
                    border-top-right-radius: 15px;
                    border-top-left-radius: 15px;
                    font-size: 1.1em;
                    font-weight: 500;
                    color: white;
                    background-color: #4f4e5f;
                """,
            children=[]
        )

        self.preview = v.Col(
            class_='',
            style_='max-width: calc(100vw - 470px);padding: 20px;background-color: #e2e2e2; ',
            children=[
                v.Container(
                    fluid=True,
                    class_='',
                    children=[
                        v.Html(tag='h2', class_='pb-3', children=['App Layout Preview']),
                        v.Content(
                            style_="""
                                        border: 1px solid #aaaaaa;
                                        height: 80vh;
                                        transform: scale(0.9);
                                        background-color: #fafbfd;
                                      """,
                            children=[
                                self.preview_browser_tab,
                                self.preview_app,
                                v.Alert(
                                    class_='mt-3',
                                    color='yellow',
                                    children=[
                                        v.Icon(left=True, children=['mdi-alert']),
                                        'This preview is rendered only based on the template and style settings, not the actual code. Your app may look different in the runtime.'
                                    ]
                                )
                            ]),
                    ]),

            ])

    def create_side_bar(self, setting_panels_info: list):
        default_menu_name = ''
        side_menu_list = []
        back_menu = {'name': 'dashboard', 'title': 'Back to Dashboard', 'icon': 'mdi-arrow-left'}

        for info in [back_menu] + setting_panels_info:
            if info.get('default', False):
                default_menu_name = info['name']
            side_menu_list.append(
                v.ListItem(value=info['name'], class_='px-0', children=[
                    v.Tooltip(color="primary", right=True, v_slots=[{
                        'name': 'activator',
                        'variable': 'tooltip',
                        'children': v.Btn(
                            on_click=(lambda name, *_: self.emit('side_menu_clicked', name), info['name']),
                            color='#535353',
                            v_on='tooltip.on',
                            class_='mx-auto',
                            style_="flex: 0 0 auto;min-width:0;height:50px;",
                            text=True,
                            children=[v.Icon(style_='font-size:20px;', children=[info['icon']])]
                        )
                    }], children=[info['title']]),
                ])
            )

        self.side_bar = v.Col(
            class_='pr-0',
            style_='max-width:70px;border-right: 1px solid silver;',
            children=[
                v.List(children=[
                    v.ListItemGroup(
                        color='#1976d2',
                        mandatory=True,
                        v_model=default_menu_name, children=side_menu_list),
                ])
            ])

        return default_menu_name

    def update_preview(self, app_config: AppConfig, page_index=None):
        self.update_preview_app(app_config, page_index=page_index)
        self.update_preview_browser_tab(app_config)

    def render(self, app_config: AppConfig, setting_panels_info: list):
        default_menu_name = self.create_side_bar(setting_panels_info)

        self.create_settings_panel(setting_panels_info)

        self.create_preview()
        self.update_preview(app_config)

        self.btn_save_changes = v.Btn(color='warning',
                                      style_='position:absolute; top:10px; right: 10px;',
                                      children=[v.Icon(left=True, children=['mdi-content-save']), 'Save Changes'],
                                      on_click=(self.emit, 'save_changes_clicked'),
                                      )
        self.btn_save_changes.disabled = True

        self.set_contents([
            v.Row(class_='',
                  style_='height: 100%;',
                  children=[
                      self.side_bar,
                      self.setting_panel_wrapper,
                      self.preview
                  ]),
            self.btn_save_changes
        ])

        self.show_settings_panel(default_menu_name)

    def show_settings_panel(self, panel_name):
        self.setting_panel_wrapper.children = [self.setting_panels[panel_name]]

    def settings_changed(self, setting_name, widget, event, data):
        self.emit('setting_changed', setting_name, widget, event, data)

    def show_app_pages_page_list(self):
        self.setting_panel_wrapper.children = [self.setting_panels['pages']]

    def update_page_settings(self, page_settings_config: dict):
        update_page_settings(page_settings_config, self)

    def update_page_list(self, pages):
        update_page_list(pages, self)

    def show_app_pages_page_setting(self, page_title):
        self.setting_panel_wrapper.children = self.page_settings[page_title]

    def open_add_page_dialog(self, page_templates: list[dict], callback: callable):
        if self.add_page_dialog is None:
            self.add_page_dialog = AddPageDialog(page_templates=page_templates, callback=callback)
            self.children = self.children + [self.add_page_dialog]

        self.add_page_dialog.reset()
        self.add_page_dialog.show()
