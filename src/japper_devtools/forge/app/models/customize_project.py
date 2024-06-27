from japper.app_config import AppConfig

from ..commons.utils import get_app_config, save_app_config_dict, get_page_templates, add_page, \
    fill_and_get_page_template_settings, delete_page


class CustomizeProjectModel:

    def __init__(self):
        self.app_config = None
        self.app_config_dict = None
        self.widgets_to_apply_changes = []

    def load_app_config(self):
        self.app_config, self.app_config_dict = get_app_config()
        return self.app_config

    def generate_setting_panels_info(self, app_config: AppConfig):
        setting_panels = [
            {'name': 'app_settings',
             'title': 'App Settings',
             'icon': 'mdi-application-array-outline',
             'description': 'Customize the settings of your app',
             'default': True,
             'components': [
                 {
                     'type': 'section',
                     'title': 'Browser Settings',
                     # 'description': 'Customize the browser settings of your app',
                     'fields': [
                         {
                             'name': 'browser_title',
                             'type': 'textfield',
                             'hint': 'This will be displayed on the browser tab',
                             'value': app_config.browser_title
                         }, {
                             'name': 'favicon',
                             'type': 'file',
                             'file_type': 'image',
                             'filename': 'app_favicon',
                             'preview': True,
                             'hint': 'A icon that appears in the browser tab.',
                             'value': app_config.favicon
                         }
                     ],
                 }, {
                     'type': 'switch_section',
                     'title': 'Navigation Menu',
                     'name': 'navigation_menu',
                     'enabled': app_config.navigation_menu.enabled,
                     # 'value': app_config.show_navigation_menu,
                     'fields': [
                         {
                             'name': 'navigation_menu.mode',
                             'type': 'select',
                             'hint': 'Choose the mode of the navigation menu',
                             'options': [
                                 {'text': 'Top', 'value': 'top', 'icon': 'mdi-dock-top'},
                                 {'text': 'Side', 'value': 'side', 'icon': 'mdi-dock-left'},
                             ],
                             'value': app_config.navigation_menu.mode,
                         }, {
                             'name': 'navigation_menu.logo',
                             'type': 'file',
                             'file_type': 'image',
                             'filename': 'app_logo',
                             'preview': True,
                             'hint': 'The logo image of the navigation menu',
                             'value': app_config.navigation_menu.logo
                         }, {
                             'name': 'navigation_menu.title',
                             'type': 'textfield',
                             'hint': 'The app title of the navigation menu',
                             'value': app_config.navigation_menu.title
                         },
                     ],

                 }
             ]},
            self.generate_page_setting_panels_info(app_config),
            # {'name': 'app_style',
            #  'title': 'App Base Style',
            #  'icon': 'mdi-palette',
            #  'description': 'Customize your app design',
            #  'components': [
            #      {
            #          'type': 'section',
            #          'title': 'Theme',
            #          'fields': [
            #              {
            #                  'name': 'theme',
            #                  'type': 'select',
            #                  'hint': 'Choose the theme of the app',
            #                  'options': [
            #                      {'text': 'Light', 'value': 'light', 'icon': 'mdi-white-balance-sunny'},
            #                      {'text': 'Dark', 'value': 'dark', 'icon': 'mdi-weather-night'},
            #                  ],
            #                  # 'value': app_config.theme,
            #              }
            #          ],
            #      }
            #  ]},

        ]

        return setting_panels

    def generate_page_setting_panels_info(self, app_config: AppConfig):
        return {
            'name': 'pages',
            'title': 'App Pages',
            'icon': 'mdi-note-multiple-outline',
            'description': 'Manage the pages of your app',
            'hide_save_changes': True,
            'default': False,
            'components': [
                {
                    'type': 'app_pages_setting',
                    'name': 'pages',
                    'pages': app_config.pages,
                    'page_settings': [
                        {
                            'type': 'page_setting',
                            'name': page.title,
                            'title': f'Page Settings ({page.title})',
                            'fields': [
                                {
                                    'name': {'setting_name': 'pages', 'page_title': page.title,
                                             'attribute': 'icon'},
                                    'type': 'icon_picker',
                                    'hint': 'Icon in the navigation menu. Use Material Design Icons name (e.g. mdi-home)',
                                    'value': page.icon
                                },
                                {
                                    'name': {'setting_name': 'pages', 'page_title': page.title,
                                             'attribute': 'hide_from_menu'},
                                    'type': 'switch',
                                    'value': page.hide_from_menu,
                                    'hint': 'Hide this page from the navigation menu'
                                },
                                {
                                    'name': {'setting_name': 'pages', 'page_title': page.title,
                                             'attribute': 'hide_nav_menu'},
                                    'type': 'switch',
                                    'value': page.hide_nav_menu,
                                    'hint': 'Hide the navigation menu in this page'
                                },
                                {
                                    'name': {'setting_name': 'pages', 'page_title': page.title,
                                             'attribute': 'always_render'},
                                    'type': 'switch',
                                    'value': page.always_render,
                                    'hint': 'Re-render this page every time the page is loaded'
                                },
                            ],
                            'template_settings': {
                                'type': 'section',
                                'title': 'Page Template Settings',
                                'fields': fill_and_get_page_template_settings(page.title,
                                                                              page.template.name,
                                                                              page.template.data)

                            } if page.template.name != 'blank' else None
                        }
                        for page in app_config.pages]
                }
            ]
        }

    def get_page_index_by_title(self, page_title):
        for i, page in enumerate(self.app_config.pages):
            if page.title == page_title:
                return i
        return None

    def set_config_value(self, setting_name, value):
        if isinstance(setting_name, dict):
            if setting_name['setting_name'] == 'pages':
                page_title = setting_name['page_title']
                attribute = setting_name['attribute']

                page_index = self.get_page_index_by_title(page_title)
                config = self.app_config.pages[page_index]
                config_dict = self.app_config_dict['pages'][page_index]
                attrs = attribute.split('.')
        else:
            config = self.app_config
            config_dict = self.app_config_dict
            attrs = setting_name.split('.')

        for attr in attrs[:-1]:
            config = config.setdefault(attr, {}) if isinstance(config, dict) else getattr(config, attr)
            config_dict = config_dict.setdefault(attr, {})

        final_attr = attrs[-1]

        if isinstance(config, dict):
            config[final_attr] = value
        else:
            setattr(config, final_attr, value)

        config_dict[final_attr] = value

    def save_app_config(self):
        save_app_config_dict(self.app_config_dict)

    def set_default_page(self, page_title):
        for i, page in enumerate(self.app_config.pages):
            is_default = page.title == page_title
            page.default = is_default
            self.app_config_dict['pages'][i]['default'] = is_default

    def check_and_set_default_page(self):
        if len(self.app_config.pages) > 0 and not any([page.default for page in self.app_config.pages]):
            self.app_config.pages[0].default = True
            self.app_config_dict['pages'][0]['default'] = True
            self.save_app_config()

    def get_page_templates(self):
        return get_page_templates()

    def add_page(self, page_title, template_name):
        new_page_config_dict = add_page(page_title, template_name)
        new_page_config = AppConfig.Page(**new_page_config_dict)

        self.app_config.pages.append(new_page_config)
        self.app_config_dict['pages'].append(new_page_config_dict)

        # self.load_app_config()

        self.check_and_set_default_page()

    def delete_page(self, page_title):
        delete_page(page_title)
        # self.load_app_config()

        to_remove = []
        for i, widget in enumerate(self.widgets_to_apply_changes):
            if isinstance(widget['setting_name'], dict) and widget['setting_name'].get('page_title',
                                                                                       None) == page_title:
                to_remove.append(i)

        for i in to_remove:
            del self.widgets_to_apply_changes[i]

        # remove the page from the app_config and app_config_dict
        for i, page in enumerate(self.app_config.pages):
            if page.title == page_title:
                del self.app_config.pages[i]
                del self.app_config_dict['pages'][i]
                break

        self.check_and_set_default_page()
