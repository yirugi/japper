import ipywidgets as ipyw
import ipyvuetify as v
import os

from japper.japper_events import JapperEvents
from japper.utils import run_js, run_js_with_wait
from japper_devtools.utils import set_devtool_interface

from ..commons import Config

OUTPUT_CLASS = 'process-status-output'
OUTPUT_SELECTOR = '.' + OUTPUT_CLASS

set_devtool_interface('forge')

ICONS = {
    'loading': Config.LOADING_ICON,
    'success': Config.SUCCESS_ICON,
    'error': Config.ERROR_ICON
}


class ProcessStatusItem:
    def __init__(self, status, title, description='', actions=None, icon=None):
        self.status = status
        self.title = title
        self.description = description
        self.actions = actions
        self.icon = icon

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class ProcessStatusWidget(v.Card, JapperEvents):
    def __init__(self, items: list[dict], console_output: bool, **kwargs):
        super().__init__(**kwargs)

        self.status_info_components = None
        self._japper_events = {}

        self.console_output = console_output
        self.items = {
            item['status']: ProcessStatusItem.from_dict(item) for item in items
        }

        self.output = None

        self.set_style('margin:0 auto;max-width:800px;border-radius: 30px;')

        self.create_components()

    def create_components(self):
        # info section
        self.status_info_components = {}
        for status, item in self.items.items():
            self.status_info_components[status] = {
                'title': v.Html(tag='h2', class_='text-center', style_='color: #002a7e;', children=[item.title]),
                'description': v.Html(tag='p', class_='text-center', style_='margin-bottom: 50px;color: #9e9e9e;',
                                      children=[item.description]),
                'icon': v.Img(src=ICONS[item.icon], width=120, class_='mx-auto',
                              style_='margin: 50px auto;') if item.icon in ICONS else '',
                'actions': v.Container(class_='text-center', style_='margin-top: 20px;', children=[
                    v.Btn(class_='ma-2', rounded=True, large=True, color=action['color'],
                          children=[
                              v.Icon(left=True, children=[action['icon']]) if 'icon' in action else '',
                              action['text']
                          ],
                          value=action['action'],
                          on_click=lambda w, e, d: self.emit('action_clicked', w.value)
                          )
                    for action in item.actions
                ]) if item.actions else ''
            }

        # output
        self.output = ipyw.Output()
        self.output.add_class(OUTPUT_CLASS)
        if self.console_output:
            self.output.add_class('console-output')

        # for automatic scrolling
        run_js_with_wait("""
            let output_div = document.querySelector('%s');
            let observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    if (mutation.type === 'childList') {
                        output_div.scrollTo({top:output_div.scrollHeight, behavior: 'smooth'});
                    }
                });
            });
            observer.observe(output_div, { childList: true, subtree: true });
        """ % OUTPUT_SELECTOR, OUTPUT_SELECTOR)

        self.status_container = v.Container(class_='',
                                            style_="padding: 50px;",
                                            children=[])

        self.children = [
            self.status_container
        ]

    def set_status(self, status: str):
        if status not in self.status_info_components:
            return

        components = self.status_info_components[status]
        self.status_container.children = [
            components['icon'],
            components['title'],
            components['description'],
            self.output,
            components['actions']
        ]

        # scroll to bottom when status changes since the output div is refreshed
        run_js_with_wait("""
            let output_div = document.querySelector('%s');
            output_div.scrollTo({top:output_div.scrollHeight});
        """ % OUTPUT_SELECTOR, OUTPUT_SELECTOR)

    def __enter__(self):
        self.output.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        self.output.__exit__(exc_type, exc_value, traceback)

    def clear_output(self):
        self.output.clear_output()
