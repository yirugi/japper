from ..widgets.prompt import PromptWidgetTypes


class BuildProjectModel:

    def __init__(self) -> None:
        self.prompts = {
            'build_mode': {
                'prompt_text': 'Choose the build mode',
                'description': "The build mode determines how the project will be built. The 'docker' mode will build the project using a docker container. Currently, only the 'docker' mode is supported.",
                'prompt_type': PromptWidgetTypes.SELECT,
                'choices': ['docker'],
                'default_value': 'docker',
                'action_text': 'Build Project',
            },
        }

        self.process_status = [
            {
                'status': 'loading',
                'icon': 'loading',
                'title': 'Building Project...',
                'description': 'Please wait while we build the project.',
            },
            {
                'status': 'success',
                'icon': 'success',
                'title': 'Project Built Successfully',
                'description': 'The project has been built successfully.',
                'actions': [
                    {

                        'icon': 'mdi-arrow-left',
                        'text': 'Back to Dashboard',
                        'color': 'primary',
                        'action': 'back_dashboard',
                    },
                ]
            },
            {
                'status': 'error',
                'icon': 'error',
                'title': 'Failed to Build Project',
                'description': 'An error occurred while building the project. Please check the console logs for more information.',
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
