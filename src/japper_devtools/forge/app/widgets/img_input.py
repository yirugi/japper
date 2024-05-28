import os
import uuid
import base64

import ipyvuetify as v
from ipyvuetify.extra import FileInput
from japper.debug import debug, debug_js
from japper.japper_events import JapperEvents
from japper.utils import run_js

from traitlets import Unicode, link, directional_link


def update_stats(self, file_index, bytes_read):
    self.stats[file_index] += bytes_read
    tot = sum(self.stats)
    percent = round((tot / self.total_size_inner) * 100)
    debug(percent, self.total_size_inner, tot, self.stats)
    if percent != self.total_progress_inner:
        self.total_progress_inner = percent
        self.total_progress = percent


def format_file_size(size):
    if size < 1024:
        return f'{size} bytes'
    elif size < 1024 * 1024:
        return f'{size / 1024:.2f} KB'
    elif size < 1024 * 1024 * 1024:
        return f'{size / 1024 / 1024:.2f} MB'
    else:
        return f'{size / 1024 / 1024 / 1024:.2f} GB'


class ImgInput(v.Container, JapperEvents):
    file_name = Unicode('')
    file_type = Unicode('')
    file_size = Unicode('')
    accept = Unicode('image/*')

    def __init__(self,
                 upload_path='./',
                 preview=False,
                 style_=None,
                 on_change: callable = None,
                 **kwargs):
        super().__init__(**kwargs)

        self.img_preview = None
        self.style_ = "padding: 0px;margin: 0px;"
        if style_:
            self.set_style(style_)
        self._japper_events = {}

        self.file_input = FileInput(multiple=False)
        # self.file_input.update_stats = update_stats
        self.file_input.observe(self.on_file_input_changed, 'file_info')
        self.file_input_id = f'file_upload_{uuid.uuid4().hex}'
        self.file_info = None
        self.upload_path = upload_path
        self.preview = preview
        self.on_change = on_change
        self.to_delete = None

        self.views = {}

        self.create_component()
        self.show_upload_view()

    def create_component(self):
        file_name = v.Html(tag='div', class_="", style_="font-size: 14px;")
        directional_link((self, 'file_name'), (file_name, 'children'), transform=(lambda x: [x]))

        file_size = v.Html(tag='div', class_="", style_="font-size: 13px;color:grey;")
        directional_link((self, 'file_size'), (file_size, 'children'), transform=(lambda x: [x]))

        self.img_preview = v.Img(class_="ml-1", style_="width:32px;aspect-ratio:1/1;")

        self.views['uploaded'] = v.Html(tag='div', class_="d-flex align-center", style_="margin: 5px;",
                                        children=[
                                            self.img_preview,
                                            v.Container(class_="d-flex flex-column",
                                                        style_="padding: 0 0 0 10px;max-width: calc(100% - 72px);",
                                                        children=[
                                                            file_name,
                                                            file_size
                                                        ]),
                                            v.Btn(icon=True, x_small=True, color='red',
                                                  children=[v.Icon(children=['mdi-trash-can-outline'])],
                                                  class_='mx-2', on_click=self.on_delete_clicked)
                                        ])

        progress = v.ProgressCircular(v_model=10, class_='ml-2', color='indigo lighten-2')
        directional_link((self.file_input, 'total_progress'), (progress, 'v_model'))

        self.views['uploading'] = v.Html(tag='div', class_="d-flex align-center", style_="margin: 5px;",
                                         children=[
                                             progress,
                                             v.Container(class_="d-flex flex-column",
                                                         style_="padding: 0 0 0 10px;max-width: calc(100% - 72px);",
                                                         children=[
                                                             file_name,
                                                             v.Html(tag='div', style_="font-size: 13px;color:grey;",
                                                                    children=['Uploading...'])
                                                         ]),
                                             # v.Btn(icon=True, x_small=True, color='red',
                                             #       children=[v.Icon(children=['mdi-cancel'])],
                                             #       class_='mx-2', on_click=self.on_cancel_uploading_clicked)
                                         ])

        link((self, 'accept'), (self.file_input, 'accept'))
        self.views['upload'] = v.Html(tag='div', class_="d-flex", style_="", children=[
            v.Html(tag='div', class_=f"file-upload-input d-none {self.file_input_id}", children=[self.file_input]),

            v.Btn(style_='height:30px;width:100%',
                  children=[v.Icon(left=True, children=['mdi-file-upload-outline']), 'Click Here to Upload File'],
                  on_click=self.on_upload_clicked),
        ])

    def show_uploaded_view(self):
        self.file_name = self.file_info['name']
        self.file_size = self.file_info['size']
        if self.preview:
            if self.file_info['cache_only']:
                encoded = base64.b64encode(self.file_info['content']).decode('utf-8')
                src = f'data:image/{self.file_info["name"].split(".")[-1]};base64,{encoded}'
            else:
                src = self.file_info['file_path']
            self.img_preview.src = src
            self.img_preview.show()
        else:
            self.img_preview.hide()

        self.children = [self.views['uploaded']]

    def show_uploading_view(self):
        self.file_name = self.file_info['name']
        self.children = [self.views['uploading']]

    def show_upload_view(self):
        self.children = [self.views['upload']]

    def on_upload_clicked(self, widget, event, data):
        run_js(f'document.querySelector(".file-upload-input.{self.file_input_id} input").click()')

    def on_delete_clicked(self, widget, event, data):
        if os.path.exists(self.file_info['file_path']):
            self.to_delete = self.file_info['file_path']

        self.file_info = None
        self.file_input.clear()

        self.show_upload_view()

        if self.on_change:
            self.on_change(self, 'deleted', None)

    def set_file(self, file_path):
        self.file_info = {
            'name': os.path.basename(file_path),
            'size': format_file_size(os.path.getsize(file_path)),
            'file_path': file_path,
            'content': None,
            'cache_only': False
        }

    def on_file_input_changed(self, change):
        file_info = change['new'][0]
        self.file_info = {
            'name': file_info['name'],
            'size': format_file_size(file_info['size']),
            'file_path': os.path.join(self.upload_path, file_info['name']),
            'content': None,
            'cache_only': True
        }

        # start uploading immediately
        self.show_uploading_view()
        self.file_info['content'] = self.file_input.get_files()[0]['file_obj'].readall()

        self.show_uploaded_view()

        if self.on_change:
            self.on_change(self, 'uploaded', self.file_info['name'])

    def save_file(self):
        if self.file_info['content'] is None:
            return

        with open(self.file_info['file_path'], 'wb') as f:
            f.write(self.file_info['content'])

        self.file_info['cache_only'] = False

    def apply_changes(self):
        if self.file_info is not None and self.file_info['cache_only']:
            self.save_file()
        if self.to_delete:
            if os.path.exists(self.to_delete):
                os.remove(self.to_delete)
            self.to_delete = None
