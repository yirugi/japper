from japper import BasePresenter
from ..views import FeaturesView
from ..models import FeaturesModel
from japper import utils as jnvutils
from japper.debug import debug, debug_js


class FeaturesPresenter(BasePresenter):
    def __init__(self) -> None:
        super().__init__()
        self.view = FeaturesView()
        self.model = FeaturesModel()

    def render(self):
        self.view.render()
        self.create_toast_alert_cases()
        self.create_debug_case()
        self.create_loading_case()
        self.create_download_case()

        return self.view

    def create_toast_alert_cases(self):
        def on_btn_show_toast_click(widget, event, data):
            jnvutils.toast_alert(widget.value['msg'], type=widget.value['type'])

        btns_show_toast = self.view.create_toast_alert_cases(self.model.toast_alert_cases)
        for btn in btns_show_toast:
            btn.on_event('click', on_btn_show_toast_click)

    def create_debug_case(self):
        def on_btn_debug_click(widget, event, data):
            debug('This is a debug message', forced_show=True)

        def on_btn_debug_js_click(widget, event, data):
            debug_js('This is a debug message')

        def on_btn_debug_error_click(widget, event, data):
            raise Exception('This is from an exception')

        btn_debug, btn_debug_js, btn_debug_error = self.view.create_debug_case()
        btn_debug.on_event('click', on_btn_debug_click)
        btn_debug_js.on_event('click', on_btn_debug_js_click)
        btn_debug_error.on_event('click', on_btn_debug_error_click)

    def create_loading_case(self):
        def on_btn_show_loading_click(widget, event, data):
            jnvutils.show_loading('Loading... (will be closed in 3 seconds)')

            from threading import Timer
            r = Timer(3.0, jnvutils.hide_loading)
            r.start()

        btn_show_loading = self.view.create_loading_case()
        btn_show_loading.on_event('click', on_btn_show_loading_click)

    def create_download_case(self):
        def on_btn_download_click(widget, event, data):
            jnvutils.download_file('/app/assets/logo.png')

        btn_download = self.view.create_file_download_case()
        btn_download.on_event('click', on_btn_download_click)
