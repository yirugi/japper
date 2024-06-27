import ipyvuetify as v
from japper import PageView
from japper.style import JapperStyle
from japper.utils import show_page

from ..commons.config import Config
from ..widgets.prompt import PromptWidget
from ..widgets.process_status import ProcessStatusWidget


class RunProjectView(PageView):
    def __init__(self) -> None:
        super().__init__()
        self.steps = None
        self.set_style('padding:0px;')
        self.set_style('font-size: 16px;')

        self.prompts = None
        self.process_status = None

    def create_prompt(self, name, prompt):
        prompt = PromptWidget.from_dict(prompt)
        prompt.action_callback = lambda *_: self.emit('action_clicked', name)
        return prompt

    def render(self, prompts: dict, process_status: list[dict]):
        # create prompts and steps
        self.prompts = {}
        for name, prompt in prompts.items():
            self.prompts[name] = self.create_prompt(name, prompt)

        self.steps = v.TabsItems(
            style_="background-color: unset;",
            v_model=0,
            children=[
                v.TabItem(children=[
                    v.Container(
                        class_="pb-0", children=[prompt]),
                ]) for prompt in self.prompts.values()
            ]
        )

        self.prompt_steps = v.Container(class_='',
                                        style_='padding: 20px 40px;max-width:1400px; ',
                                        children=[
                                            v.Btn(class_='ma-2', color='default',
                                                  style_='margin-top: 20px;',
                                                  children=[
                                                      v.Icon(left=True, children=['mdi-arrow-left']),
                                                      'To Dashboard'],
                                                  on_click=lambda *_: show_page('home')
                                                  ),
                                            v.Container(
                                                class_='mx-auto text-center',
                                                style_="margin-top: 60px;",
                                                children=[
                                                    self.steps,
                                                    v.Btn(text=True, rounded=True, color='grey', class_='py-2 px-4',
                                                          children=['Back'],
                                                          on_click=lambda *_: self.emit('back_clicked'), )
                                                ])
                                        ])

        # create project creation view
        self.process_status = ProcessStatusWidget(process_status, console_output=True)
        self.project_creation_section = v.Container(
            class_='mx-auto',
            style_='margin-top: 50px;',
            children=[
                self.process_status
            ])
        self.project_creation_section.hide()

        # create the content
        self.set_contents([
            v.Sheet(style_="""
                        height: 100%; 
                        padding: 0px;
                        background-color: #fafbfd;
                            """,
                    class_='mx-auto',
                    children=[
                        self.prompt_steps,
                        self.project_creation_section,
                    ]),
        ])

    def show_create_project_step(self):
        self.prompt_steps.hide()
        self.project_creation_section.show()

    def reset_view(self):
        self.prompt_steps.show()
        self.steps.v_model = 0
        self.project_creation_section.hide()
        self.process_status.clear_output()
