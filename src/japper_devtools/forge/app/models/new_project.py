from japper_devtools.utils import get_conda_env_list

from ..widgets.prompt import PromptWidgetTypes


def name_validator(value):
    if not value.isascii():
        return 'Only ASCII characters are allowed.'
    if ' ' in value:
        return 'Spaces are not allowed.'
    if any(char in value for char in '!@#$%^&*()+={}[]|\\:;"\'<>,.?/'):
        return 'Special characters are not allowed.'


class NewProjectModel:
    DEFAULT_CONFIG = {
        'project_name': '',
        'project_title': '',
        'dev_env': 'docker',
    }

    def __init__(self) -> None:
        self.prompts = {
            'project_name': {
                'prompt_text': 'Enter the Project Name',
                'description': "The project name will be used throughout the codebase of the application. It should be in lowercase and without spaces (e.g. japper_app).",
                'prompt_type': PromptWidgetTypes.TEXT,
                'default_value': '',
                'validator': name_validator,
            },
            # 'project_title': {
            #     'prompt_text': 'Enter the Project Title',
            #     'description': "The project title will be displayed in the header of the application. It can have spaces and special characters (e.g. Japper App).",
            #     'prompt_type': PromptWidgetTypes.TEXT,
            #     'default_value': '',
            # },
            'dev_env': {
                'prompt_text': 'Choose the Development Environment',
                'description': "Select the development environment for the project. The development environment will be used to set up the project dependencies and runtime environment.",
                'prompt_type': PromptWidgetTypes.SELECT,
                # 'choices': ['docker', 'conda', 'manual'],
                'choices': ['docker', 'local'],  # todo: add descriptions for each choices
                'default_value': 'docker',
            },
            'conda_env_name': {
                'prompt_text': 'Enter the new conda environment name',
                'description': 'The conda environment name will be used to create a new conda environment for the project.',
                'prompt_type': PromptWidgetTypes.TEXT,
                'default_value': '',
            },
        }

        self.process_status = [
            {
                'status': 'loading',
                'icon': 'loading',
                'title': 'Creating Project...',
                'description': 'Please wait while we create the project.',
            },
            {
                'status': 'success',
                'icon': 'success',
                'title': 'Project Created',
                'description': 'The project has been created successfully.',
                'actions': [
                    {
                        'text': 'Customize the App',
                        'color': 'primary',
                        'action': 'customize_project',
                    },
                    {
                        'text': 'Use Default Configuration',
                        'color': 'default',
                        'action': 'use_default_config',
                    },
                ]
            },
            {
                'status': 'error',
                'icon': 'error',
                'title': 'Failed to Create Project',
                'description': 'An error occurred while creating the project. Please check the console logs for more information.',
                'actions': [
                    {

                        'icon': 'mdi-arrow-left',
                        'text': 'Back to Dashboard',
                        'color': 'default',
                        'action': 'back_dashboard',
                    },
                    {
                        'text': 'Retry',
                        'color': 'error',
                        'action': 'retry',
                    },
                ]
            }
        ]

        self.conda_env_list = None

    def get_conda_env_list(self):
        if self.conda_env_list is None:
            self.conda_env_list = get_conda_env_list()

    def check_conda_env_name(self, conda_env_name):
        self.get_conda_env_list()
        return conda_env_name not in self.conda_env_list
