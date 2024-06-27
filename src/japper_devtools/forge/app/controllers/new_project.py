import os
from japper import PageController
from japper.debug import debug
from japper.utils import show_page, toast_alert
from japper_devtools.project_init import init_project
from japper_devtools.utils import to_camel_space, chdir

from ..commons import Config
from ..views import NewProjectView
from ..models import NewProjectModel
from ..commons.utils import link_working_dir, add_page, get_app_config, save_app_config_dict


class NewProjectController(PageController):
    def __init__(self) -> None:
        super().__init__()
        self.project_config = None
        self.view = NewProjectView()
        self.model = NewProjectModel()

        self.on('before_display', self.on_before_display)
        self.view.on('action_clicked', self.action_clicked)
        self.view.on('back_clicked', self.back_clicked)

    def render(self):
        self.view.render(
            prompts=self.model.prompts,
            process_status=self.model.process_status
        )

        # prompt event handlers
        self.view.prompts['conda_env_name'].on('keyup', self.on_conda_env_name_keyup)
        self.view.prompts['dev_env'].on('change', self.on_dev_env_prompt_change)

        # process_status event handers
        self.view.process_status.on('action_clicked', self.process_status_action_clicked)

        # self.create_project()

    def reset_values(self):
        self.project_config = self.model.DEFAULT_CONFIG.copy()

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

        # project_title removed
        # if prompt_name == 'project_name':
        #     prompts['project_title'].value = to_camel_space(prompt.value)
        #     self.project_config['project_name'] = prompt.value
        #     self.show_next_step('project_title')
        #
        # elif prompt_name == 'project_title':
        #     self.project_config['project_title'] = prompt.value
        #     self.show_next_step('dev_env')

        if prompt_name == 'project_name':
            self.project_config['project_name'] = prompt.value
            self.project_config['project_title'] = to_camel_space(prompt.value)
            self.show_next_step('dev_env')

        elif prompt_name == 'dev_env':
            self.project_config['dev_env'] = prompt.value
            if prompt.value == 'conda':
                if prompts['conda_env_name'].value == '':
                    prompts['conda_env_name'].value = prompts['project_name'].value
                self.show_next_step('conda_env_name')
                self.model.get_conda_env_list()
            else:
                self.create_project()

        elif prompt_name == 'conda_env_name':
            self.project_config['conda'] = {'env_name': prompt.value,
                                            'use_existing_env': prompt.action_text == 'Use Anyway'}
            self.create_project()

    def show_next_step(self, prompt_name=None):
        if prompt_name:
            if prompt_name == 'dev_env':
                self.on_dev_env_prompt_change()
            elif prompt_name == 'conda_env_name':
                self.on_conda_env_name_keyup()

            self.view.steps.v_model = list(self.view.prompts.keys()).index(prompt_name)
        else:
            self.view.steps.v_model += 1

    def on_conda_env_name_keyup(self, key=None):
        prompt = self.view.prompts['conda_env_name']
        if self.model.check_conda_env_name(prompt.value):
            prompt.set_error_msg('')
            self.set_prompt_action_btn_to_create_project(prompt)
        else:
            prompt.set_error_msg(
                'Environment name already exists. Click "Use Anyway" if you want to use it instead of creating a new one. Otherwise, enter a different name.')
            prompt.set_action_text('Use Anyway')
            prompt.set_action_color('warning')

    def on_dev_env_prompt_change(self, data=None):
        prompt = self.view.prompts['dev_env']
        if prompt.value == 'conda':
            prompt.set_action_text('Continue')
            prompt.set_action_color('primary')
        else:
            self.set_prompt_action_btn_to_create_project(prompt)

    def set_prompt_action_btn_to_create_project(self, prompt):
        prompt.set_action_text('Create Project')
        # prompt.set_action_color('red lighten-3')
        prompt.set_action_color('success')

    def create_project(self):
        # self.project_config = {
        #     'project_name': 'jojo',
        #     'project_title': 'Jojo Rabbit',
        #     'dev_env': 'conda',
        #     'conda': {'env_name': 'jojo', 'use_existing_env': False},
        # }
        self.set_create_status('loading')
        self.view.show_create_project_step()

        with self.view.process_status, chdir(Config.JAPPER_WORKING_DIR):
            try:
                init_project(self.project_config)
                self.set_create_status('success')
                toast_alert('Project created successfully!', 'success')

            except SystemExit as e:
                self.set_create_status('error')
                return

        Config.JAPPER_WORKING_DIR = os.path.join(Config.JAPPER_WORKING_DIR, self.project_config['project_name'])
        link_working_dir()

    def set_create_status(self, status: str):
        self.view.process_status.set_status(status)

    def process_status_action_clicked(self, action):
        if action == 'back_dashboard':
            self.goto_dashboard()
        elif action == 'retry':
            self.view.reset_view()
        elif action == 'customize_project':
            show_page('customize project')
        elif action == 'use_default_config':
            add_page('Home', 'landing01', icon='mdi-home', default=True)
            add_page('Tool', 'blank', icon='mdi-wrench')

            _, app_config_dict = get_app_config()
            app_config_dict['pages'][0]['template']['data']['start_button']['link'] = 'Tool'
            save_app_config_dict(app_config_dict)
            self.goto_dashboard()
