import os
from japper import PageController
from japper.debug import debug
from japper.utils import show_page, toast_alert, popup_confirm
from japper_devtools.utils import chdir, build_docker_image, load_config

from ..commons import Config
from ..views import BuildProjectView
from ..models import BuildProjectModel


class BuildProjectController(PageController):
    def __init__(self) -> None:
        super().__init__()
        self.project_config = None
        self.view = BuildProjectView()
        self.model = BuildProjectModel()

        self.on('before_display', self.on_before_display)
        self.view.on('action_clicked', self.action_clicked)
        self.view.on('back_clicked', self.back_clicked)

    def render(self):
        self.view.render(
            prompts=self.model.prompts,
            process_status=self.model.process_status
        )

        # process_status event handlers
        self.view.process_status.on('action_clicked', self.process_status_action_clicked)

        with chdir(Config.JAPPER_WORKING_DIR):
            self.config = load_config()

        # self.create_project()

    def reset_values(self):
        for prompt_name, prompt in self.view.prompts.items():
            prompt.value = self.model.prompts[prompt_name]['default_value']
            prompt.set_error_msg('')

        self.view.reset_view()

    def on_before_display(self):
        self.reset_values()

    def back_clicked(self):
        if self.view.steps.v_model == 0:
            self.goto_dashboard()
        else:
            self.view.steps.v_model -= 1

    def goto_dashboard(self):
        show_page('home')

    def action_clicked(self, prompt_name):
        prompts = self.view.prompts
        prompt = prompts[prompt_name]

        if prompt_name == 'build_mode':
            if self.config['dev_env'] == 'local':
                popup_confirm(
                    "The project is set to run in local environment. Do you want to build the production Docker image?",
                    title='Continue?',
                    confirm_callback=lambda: self.run(), cancel_callback=lambda: self.goto_dashboard())
            else:
                self.run()

    def show_next_step(self, prompt_name=None):
        if prompt_name:
            self.view.steps.v_model = list(self.view.prompts.keys()).index(prompt_name)
        else:
            self.view.steps.v_model += 1

    # def set_prompt_action_btn_to_create_project(self, prompt):
    #     prompt.set_action_text('Create Project')
    #     # prompt.set_action_color('red lighten-3')
    #     prompt.set_action_color('success')

    def process_status_action_clicked(self, action):
        if action == 'back_dashboard':
            self.goto_dashboard()
        elif action == 'retry':
            self.view.reset_view()

    def run(self):
        self.view.process_status.set_status('loading')
        self.view.show_run_process_step()

        with self.view.process_status, chdir(Config.JAPPER_WORKING_DIR):
            try:
                build_docker_image('prod')

                self.view.process_status.set_status('success')

            except SystemExit as e:
                self.view.process_status.set_status('error')
                return
