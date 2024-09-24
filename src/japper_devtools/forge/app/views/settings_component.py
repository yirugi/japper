from functools import partial
import ipyvuetify as v
from traitlets import link, directional_link

from japper_devtools.utils import to_camel_space

from japper.debug import debug
from ..widgets import ImgInput
from ..commons.config import Config


def field_label(name):
    return v.Html(tag='div', class_='pl-0', style_="font-weight:500;font-size:1em;", children=[name])


def name_to_title(name):
    return to_camel_space(name.split('.')[-1])


def section_title(name):
    return v.Html(tag='h3', class_='mb-3', children=[name])


def switch_section_title(name):
    return v.Html(tag='h4', class_='mb-0', children=[name])


def create_hint(hint):
    return v.Html(tag='div', class_='px-2 py-1', style_='color:#00000099;font-size:12px;',
                  children=[hint if hint else ''])


def create_textfield(component, title, hint, change_event_handler):
    textfield = v.TextField(class_='v-input--denser',
                            placeholder='Enter the ' + title,
                            v_model=component['value'],
                            outlined=True, hint=hint, persistent_hint=True,
                            on_change=(change_event_handler, component['name'])
                            )
    if hint is None:
        textfield.persistent_hint = False
        textfield.hide_details = True
        textfield.class_list.add('mb-2')

    return [textfield]


def create_textarea(component, title, hint, change_event_handler):
    textarea = v.Textarea(class_='v-input--denser',
                          placeholder='Enter the ' + title,
                          v_model=component['value'],
                          outlined=True, hint=hint, persistent_hint=True,
                          on_change=(change_event_handler, component['name'])
                          )

    debug(component)
    if 'height' in component:
        textarea.height = component['height']

    if hint is None:
        textarea.persistent_hint = False
        textarea.hide_details = True
        textarea.class_list.add('mb-2')

    return [textarea]


def create_img_input(component, hint, change_event_handler):
    img_input = ImgInput(upload_path=Config.LINKED_ASSETS_PATH,
                         filename=component.get('filename', None),
                         preview=component.get('preview', False),
                         style_='border-radius: 5px; border: 1px solid #e0e0e0;',
                         on_change=partial(change_event_handler, component['name']),
                         )

    # if component['file_type'] == 'image':
    #     img_input.accept = 'image/*'

    if component.get('value', None) is not None:
        img_input.set_file(Config.LINKED_ASSETS_PATH + component['value'])
        img_input.show_uploaded_view()

    return [
        img_input,
        create_hint(hint)
    ]


def create_select(component, change_event_handler):
    return [
        v.BtnToggle(v_model=component.get('value', None), color='primary', dense=True, class_="mb-2", mandatory=True,
                    on_change=(change_event_handler, component['name']),
                    children=[
                        v.Btn(value=option['value'],
                              class_='px-4',
                              children=[
                                  v.Icon(left=True, children=[option['icon']]) if 'icon' in option else '',
                                  option['text']
                              ])
                        for option in component['options']

                    ]),
    ]


def create_page_setting(page_setting: dict, settings_view):
    contents = []
    for field in page_setting['fields']:
        contents += create_settings_components(field, settings_view)
    contents.append(v.Divider(class_="my-4"))

    # add template settings if available
    if page_setting['template_settings'] is not None:
        contents += create_settings_components(page_setting['template_settings'], settings_view)

    return [
        v.Container(class_='d-flex pa-0 align-center', children=[
            v.Btn(small=True, color='default',
                  children=[v.Icon(small=True, left=True, children=['mdi-arrow-left']), 'Back'],
                  on_click=(settings_view.emit, 'page_setting_back_to_page_list_clicked')),
            v.Spacer(),
            v.Html(tag='p', class_='mb-0', style_='font-size: 1.2em;font-weight: 500;',
                   children=[page_setting['title']]),

        ]),

        v.Divider(class_="my-2"),
        section_title('Base Page Settings'),
        *contents,

    ]


def create_page_list_buttons(page, emit):
    page_list_buttons = [
        {
            'name': 'edit',
            'icon': 'mdi-pencil-outline',
            'tooltip': 'Edit Page'
        }, {
            'name': 'default',
            'icon': 'mdi-home-circle-outline',
            'tooltip': 'Make This Default Page'
        }, {
            'name': 'delete',
            'icon': 'mdi-delete-outline',
            'tooltip': 'Delete Page'
        }
    ]

    buttons = []
    for button in page_list_buttons:
        buttons.append(
            v.Tooltip(bottom=True, v_slots=[{
                'name': 'activator',
                'variable': 'tooltip',
                'children': v.Btn(
                    color='primary' if button['name'] == 'default' and page.default else 'default',
                    on_click=(emit, 'page_list_button_clicked', button['name'], page.title),
                    icon=True, x_small=True, v_on='tooltip.on',
                    children=[v.Icon(style_='font-size:18px;', children=[button['icon']])]),
            }], children=[button['tooltip']])
        )

    return buttons


def update_page_list(page_list, settings_view):
    page_list_item = []

    for page in page_list:
        # page list
        page_list_item.append(
            v.ListItem(
                class_='pr-1',

                style_="border: 1px solid silver; border-radius: 5px; margin-bottom: 5px;",
                children=[
                    v.ListItemIcon(
                        style_='margin-right: 10px;',
                        children=[
                            v.Icon(children=[page.icon]) if page.icon else ''
                        ]),
                    v.ListItemContent(children=[
                        v.Container(class_='pa-0 d-flex align-center', children=[
                            page.title,
                            v.Spacer(),
                            *create_page_list_buttons(page, settings_view.emit)
                        ])
                    ])
                ])
        )

    settings_view.page_list_wrapper.children = page_list_item


def update_page_settings(page_settings_config, settings_view):
    # page settings
    page_settings = {}
    for page_setting in page_settings_config:
        page_settings[page_setting['name']] = create_page_setting(page_setting, settings_view)

    # make some vars to global for later access
    settings_view.page_settings = page_settings


def create_app_pages_setting(component, settings_view):
    settings_view.page_list_wrapper = v.ListItemGroup(
        color='primary',
        mandatory=True,
        v_model=None,
        on_change=(settings_view.emit, 'page_list_changed'),
        children=[]
    )

    update_page_list(component['pages'], settings_view)
    update_page_settings(component['page_settings'], settings_view)

    return [
        v.List(dense=True,
               style_="background-color:transparent;",
               children=[
                   settings_view.page_list_wrapper
               ]),
        v.Container(class_='d-flex justify-end pa-0', children=[
            v.Btn(color='primary', children=[v.Icon(left=True, children=['mdi-plus-circle']), 'Add Page'],
                  on_click=(settings_view.emit, 'add_page_clicked'),
                  class_='mt-2')
        ])
    ]


def create_switch(component, title, hint, change_event_handler):
    return [
        v.Container(class_='d-flex align-center pa-0', children=[
            v.Html(tag='p', class_='mb-0', style_='font-size: 1em;font-weight: 500;',
                   children=[title]),
            v.Spacer(),
            v.Switch(class_='ma-0',
                     style_='margin-top:-2px !important;',
                     v_model=component['value'], dense=True, inset=True,
                     hide_details=True,
                     on_change=(change_event_handler, component['name'])),

        ]),
        create_hint(hint)
    ]


def create_icon_picker(component, title, hint, change_event_handler):
    # TODO: implement icon picker
    textfield = v.TextField(class_='v-input--denser',
                            placeholder='Enter the icon name',
                            v_model=component['value'],
                            outlined=True, hide_details=True,
                            on_change=(change_event_handler, component['name'])
                            )
    icon = v.Icon(class_='mr-2', style_='width: 32px;height:32px;border:1px solid silver;border-radius:5px;')
    directional_link((textfield, 'v_model'), (icon, 'children'),
                     transform=(lambda x: [x]))

    return [
        v.Container(class_='d-flex align-center pa-0', children=[
            icon,
            textfield,
            v.Btn(icon=True, href='https://pictogrammers.github.io/@mdi/font/7.4.47/', target='_blank', class_='ma-0',
                  children=[v.Icon(children=['mdi-magnify'])])
        ]),
        create_hint(hint)
    ]


def create_settings_components(component: dict, settings_view) -> list:
    contents = []

    title = component.get('title', None)
    if title is None:
        name = component['name'] if isinstance(component['name'], str) else component['name']['attribute']
        title = name_to_title(name)
    # section
    if component['type'] in ['section', 'switch_section']:
        for field in component['fields']:
            contents += create_settings_components(field, settings_view)

        if component['type'] == 'switch_section':
            if isinstance(component['name'], str):
                component_var_path = component['name'] + '.enabled'
            else:
                component_var_path = component['name'].copy()
                component_var_path['attribute'] += '.enabled'

            title_switch = v.Switch(class_='ma-0',
                                    style_='margin-top:-2px !important;',
                                    v_model=component['enabled'], dense=True, inset=False,
                                    hide_details=True,
                                    on_change=(settings_view.settings_changed, component_var_path))
            section_content = v.Card(
                disabled=not component['enabled'],
                class_='pa-1',
                style_='background-color:transparent;',
                elevation=0,
                children=[
                    *contents
                ])
            contents = [
                v.Html(tag='div', class_='',
                       style_="margin:10px -5px;border:1px solid #0000001f;border-radius:5px;padding:5px 10px;",
                       children=[
                           v.Container(class_='pa-0 d-flex', children=[
                               switch_section_title(title),
                               v.Spacer(),
                               title_switch
                           ]),
                           v.Divider(class_='mb-2'),
                           section_content
                       ])
            ]

            # link switch's v_model to card disabled
            link((title_switch, 'v_model'), (section_content, 'disabled'),
                 transform=((lambda x: not x), (lambda x: x)))

        else:
            contents = [

                section_title(component['title']),
                *contents
            ]

        return [*contents,
                # v.Divider(class_="my-4")
                ]

    # not section
    hint = component.get('hint', None)

    contents = [field_label(title) if component['type'] != 'switch' else '']
    if component['type'] == 'textfield':
        contents += create_textfield(component, title, hint, settings_view.settings_changed)
    elif component['type'] == 'textarea':
        contents += create_textarea(component, title, hint, settings_view.settings_changed)
    elif component['type'] == 'file':
        if component['file_type'] == 'image':
            img_input = create_img_input(component, hint, settings_view.settings_changed)
            contents += img_input
            component_name = component['name']
            if isinstance(component_name, dict) and 'page_title' in component_name:
                component_name = f"{component_name['setting_name']}.{component_name['page_title']}.{component_name['attribute']}"
            settings_view.img_inputs[component_name] = img_input[0]
    elif component['type'] == 'select':
        contents += create_select(component, settings_view.settings_changed)
    elif component['type'] == 'app_pages_setting':
        contents += create_app_pages_setting(component, settings_view)
    elif component['type'] == 'switch':
        contents += create_switch(component, title, hint, settings_view.settings_changed)
    elif component['type'] == 'icon_picker':
        contents += create_icon_picker(component, title, hint, settings_view.settings_changed)

    contents += [v.Spacer(style_="height:.5em;")]
    return contents
