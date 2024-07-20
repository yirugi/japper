from ..commons import Config


class GenerateDocModel:
    def __init__(self) -> None:
        self.process_status = [
            {
                'status': 'loading',
                'icon': 'loading',
                'title': 'Generating Document...',
                'description': 'Please wait while we generate the document.',
            },
            {
                'status': 'success',
                'icon': 'success',
                'title': 'Document Generated',
                'description': 'Documentation generated at docs/app/index.html.',
                # 'description': f'Documentation generated at <a href="file:///{Config.JAPPER_WORKING_DIR}/docs/app/index.html" target="_blank">docs/app/index.html</a>.',
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
                'title': 'Failed to Generate Document',
                'description': 'An error occurred while generating the document. Please check the console logs for more information.',
                'actions': [
                    {

                        'icon': 'mdi-arrow-left',
                        'text': 'Back to Dashboard',
                        'color': 'primary',
                        'action': 'back_dashboard',
                    }
                ]
            }
        ]
