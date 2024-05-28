import ipyvuetify as v
from japper import utils as jnvutils
from japper import BaseView


# from japper.widgets import FileUpload


class FeaturesView(BaseView):
    def __init__(self) -> None:
        super().__init__(style_='padding-bottom: 60px;')

    def render(self):
        self.children = [
            v.Html(tag='div', class_='content-title', children=['Japper Utility Functions']),
        ]

    def create_toast_alert_cases(self, cases):
        btns_show_toast = []
        for case in cases:
            btn_show_toast = v.Btn(class_='mr-3', color=case['type'], children=[case['type']], value=case)
            btns_show_toast.append(btn_show_toast)

        toast_alert_case = v.Container(fluid=True, children=[
            v.Card(children=[
                v.CardTitle(children=['Toast Alert']),
                v.CardText(children=btns_show_toast),
            ]),
        ])

        self.children = self.children + [toast_alert_case]

        return btns_show_toast

    def create_debug_case(self):
        btn_debug = v.Btn(class_='mr-3', color='primary',
                          children=['Print Debug Message on the bottom Debug Panel'])
        btn_debug_js = v.Btn(class_='mr-3', color='orange',
                             children=['Print Debug Message on JS Console'])
        btn_debug_error = v.Btn(class_='mr-3', color='error',
                                children=['Catch and Print Error Message'])

        debug_case = v.Container(fluid=True, children=[
            v.Card(children=[
                v.CardTitle(children=['Debug']),
                v.CardText(children=[btn_debug, btn_debug_js, btn_debug_error]),
            ]),
        ])

        self.children = self.children + [debug_case]

        return btn_debug, btn_debug_js, btn_debug_error

    def create_loading_case(self):
        btn_show_loading = v.Btn(class_='mr-3', color='primary',
                                 children=['Show Loading'])
        loading_case = v.Container(fluid=True, children=[
            v.Card(children=[
                v.CardTitle(children=['Loading']),
                v.CardText(children=[btn_show_loading]),
            ]),
        ])

        self.children = self.children + [loading_case]
        return btn_show_loading

    def create_file_download_case(self):
        btn_download = v.Btn(class_='mr-3', color='primary',
                             children=['Download Logo Image'])
        download_case = v.Container(fluid=True, children=[
            v.Card(children=[
                v.CardTitle(children=['File Downloader']),
                v.CardText(children=[btn_download]),
            ]),
        ])

        self.children = self.children + [download_case]
        return btn_download

    def create_logger_case(self):
        btn_logger = v.Btn(class_='mr-3', color='primary',
                           children=['Show Logger'])
        logger_case = v.Container(fluid=True, children=[
            v.Card(children=[
                v.CardTitle(children=['Logger']),
                v.CardText(children=[btn_logger]),
            ]),
        ])

        self.children = self.children + [logger_case]
        return btn_logger

    # TODO: implement file upload case
    # def create_file_upload_case(self):
    #     fileupload = FileUpload()
    #     upload_case = v.Container(fluid=True, children=[
    #         v.Card(children=[
    #             v.CardTitle(children=['File Uploader']),
    #             v.CardText(children=[
    #                 v.Row(children=[
    #                     v.Col(children=[
    #                         '1. Upload a file: ',
    #                         fileupload
    #                     ]),
    #                     v.Col(children=[
    #                         '2. Check the uploaded file: ',
    #                         v.Btn(color='primary', children=['Check'])
    #                     ]),
    #                 ]),
    #             ]),
    #         ]),
    #     ])
    #
    #     self.children = self.children + [upload_case]
    #     return fileupload
