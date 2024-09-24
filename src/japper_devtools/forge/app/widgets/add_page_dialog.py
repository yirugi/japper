import ipyvuetify as v
import os

from japper.japper_events import JapperEvents
from japper_devtools.utils import has_special_chars
from ..commons.utils import check_page_file_exists, get_page_template_path

from japper.debug import debug


class AddPageDialog(v.Dialog, JapperEvents):
    def __init__(self, page_templates: list[dict], callback: callable, **kwargs):
        super().__init__(**kwargs)
        self.max_width = '900px'

        self._japper_events = {}

        self.page_templates = page_templates
        self.callback = callback
        self.v_model = False

        self.page_title = None
        self.template = None

        self.render()

    def render(self):
        templates = []
        for page_template in self.page_templates:
            # template = v.Card(
            #
            #     link=True,
            #     elevation=0,
            #     class_='hover-grow',
            #     style_='background-color:transparent;flex: 1 1 auto;max-width:350px;padding:20px;',
            #
            # )
            template_path = get_page_template_path(page_template['name'])
            templates.append(
                v.ListItem(
                    on_click=(self.template_selected, page_template['name']),
                    class_='d-flex flex-column align-center',
                    style_='max-width:350px;padding:20px;',
                    children=[
                        v.Img(style_='border:1px solid silver;height:160px;',
                              src=os.path.join(template_path,
                                               page_template['thumbnail'])) if 'thumbnail' in page_template else
                        v.Html(tag='div',  # TODO: change this to image
                               style_='background-color:white;min-width:300px;height:160px;border:1px solid silver;padding-top:25%;text-align:center;',
                               children=[v.Icon(children=['mdi-plus'])]),

                        v.Html(tag='div', class_='pl-2 pt-2', style_='font-size:1.1em;',
                               children=[page_template['title']]),
                        v.Html(tag='div', class_='pl-2 text-center', style_='color:grey;',
                               children=[page_template['description']]),
                    ]
                )
            )

        templates_wrapper = v.List(
            children=[
                v.ListItemGroup(
                    color='primary',
                    class_='d-flex justify-center flex-wrap',
                    children=templates,
                )
            ]

        )

        self.btn_add = v.Btn(color='primary', children=[v.Icon(left=True, children=['mdi-plus-circle']), 'Add Page'],
                             on_click=self.on_add_clicked, disabled=True)

        self.txt_page_title = v.TextField(
            placeholder='Enter page title',
            v_model='', outlined=True, dense=True,
            hint='This will be shown in the navigation menu. e.g. Home, Tools, About Us',
            persistent_hint=True,
            on_keyup=self.on_pagetitle_changed,
        )

        self.children = [  # todo: fix flex wrap
            v.Sheet(
                style_='padding:20px 40px;',
                children=[
                    v.Html(tag='div', style_='font-size:1.4em;font-weight:600;padding:10px 0 0 0;',
                           children=['Add New Page']),
                    v.Html(tag='div', style_='font-size:1em;padding:5px 0;color:grey;',
                           children=[
                               'Create a new page for your app. You can choose a template to start with or create a blank page.']),
                    v.Divider(class_='mb-4'),
                    v.Container(
                        class_='pa-0',
                        children=[
                            v.Html(tag='div', class_='mb-2', style_='font-size:1.1em;font-weight:500;',
                                   children=['Page Title']),
                            self.txt_page_title

                        ]
                    ),
                    v.Container(
                        class_='pa-0',
                        children=[
                            v.Html(tag='div', style_='font-size:1.1em;font-weight:500;padding:10px 0 0 0;',
                                   children=['Select a template']),
                            v.Html(tag='div', style_='font-size:1em;padding:5px 0;color:grey;',
                                   children=[
                                       'Choose a template to start with. More templates will be available soon.']),
                            templates_wrapper,
                            # v.Html(
                            #     tag="div",
                            #     class_='d-flex flex-wrap justify-center',
                            #     style_='gap:30px;margin-top:30px;',
                            #
                            #     children=templates_wrapper
                            # ),
                        ]
                    ),

                    v.Divider(),

                    v.Container(
                        class_='d-flex px-0',
                        # style_='margin-top:20px;',
                        children=[
                            v.Html(tag='div', style_='font-size:1em;padding:5px 0;color:grey;',
                                   children=['This change will be applied to your app immediately.']),
                            v.Spacer(),
                            self.btn_add,
                            v.Btn(class_='ml-3', color='default', children=['Close'],
                                  on_click=self.close)
                        ])
                ]
            )
        ]

    def close(self, *args):
        self.v_model = False

    def show(self):
        self.v_model = True

    def template_selected(self, template_name, *args):
        self.template = template_name
        self.validate()

    def on_pagetitle_changed(self, widget, event, data):
        self.page_title = widget.v_model
        self.validate()

    def validate(self):
        self.txt_page_title.rules = []
        self.btn_add.disabled = True

        if self.page_title and (self.page_title[0] == ' ' or self.page_title[0].isdigit()):
            self.txt_page_title.rules = ['Page title cannot start with a number or space']
            return

        if has_special_chars(self.page_title, allow_spaces=True):
            self.txt_page_title.rules = ['Page title cannot contain special characters']
            return

        page_file_exists, msg = check_page_file_exists(self.page_title)
        if page_file_exists:
            self.txt_page_title.rules = [f'Page with this name already exists ({msg})']
            return

        if self.template is None or self.page_title.strip() == '':
            return

        self.btn_add.disabled = False

    def on_add_clicked(self, *args):
        self.callback(self.page_title, self.template)
        self.v_model = False

    def reset(self):
        self.page_title = ''
        self.template = None
        self.btn_add.disabled = True
