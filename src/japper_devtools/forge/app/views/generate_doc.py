import ipyvuetify as v
from japper import PageView

from ..commons.config import Config
from ..widgets.process_status import ProcessStatusWidget


class GenerateDocView(PageView):
    def __init__(self) -> None:
        super().__init__()
        self.steps = None
        self.set_style('padding:0px;')
        self.set_style('font-size: 16px;')

        self.process_status = None

    def render(self, process_status: list[dict]):
        self.process_status = ProcessStatusWidget(process_status, console_output=True)
        self.process_run_section = v.Container(
            class_='mx-auto',
            style_='margin-top: 50px;',
            children=[
                self.process_status
            ])

        # create the content
        self.set_contents([
            v.Sheet(style_="""
                                height: 100%; 
                                padding: 0px;
                                background-color: #fafbfd;
                                    """,
                    class_='mx-auto',
                    children=[
                        self.process_run_section,
                    ]),
        ])

    def reset_view(self):
        self.process_status.clear_output()
