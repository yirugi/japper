from ..commons.config import Config


class HomeModel:
    action_cards = [
        {
            'title': 'Create a new Project',
            'description': 'Create a new Japper project from scratch.',
            'image': '/app/assets/card_project.jpg',
            'page': 'new project',
            'disabled': False
        },
        {
            'title': 'Customize the App',
            'description': 'Customize your application. Change the layout, add pages, and more.',
            'image': '/app/assets/card_customize.jpg',
            'page': 'customize project',
            'disabled': False
        },
        # {
        #     'title': 'Run the Project',
        #     'description': 'Run your project on your local machine for development or production preview.',
        #     'image': '/app/assets/card_run.jpg',
        #     'page': 'run project',
        #     'disabled': False
        # },
        {
            'title': 'Build the Project',
            'description': 'Build your project to a Docker image for production deployment.',
            'image': '/app/assets/card_build.jpg',
            'page': 'build project',
            'disabled': False
        },
        # {
        #     'title': 'Deploy the Project',
        #     'description': 'Deploy your project. You can deploy to Docker Hub, or a custom docker registry.',
        #     'image': '/app/assets/card_deploy.jpg',
        #     'page': 'deploy project',
        #     'disabled': False
        # },
        {
            'title': 'Generate Documentation',
            'description': 'Generate documentation automatically for your project.',
            'image': '/app/assets/card_docs.jpg',
            'page': 'generate doc',
            'disabled': False
        }
    ]

    def __init__(self) -> None:
        pass
