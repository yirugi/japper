from ..widgets.prompt import PromptWidgetTypes


class RunProjectModel:

    def __init__(self) -> None:
        self.prompts = {
            'dev_env': {
                'prompt_text': 'Choose the Runtime Mode',
                'description': "Select the runtime mode for the project. The runtime mode will be used to set up the project dependencies and runtime environment.",
                'prompt_type': PromptWidgetTypes.SELECT,
                'choices': ['development', 'production preview', 'production'],
                'default_value': 'development',
            }
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
