from japper import PageController
from japper.debug import debug
from japper.utils import show_page, toast_alert
from japper_devtools.utils import to_camel_space, chdir, run_command

from ..commons import Config
from ..views import GenerateDocView
from ..models import GenerateDocModel


class GenerateDocController(PageController):
    def __init__(self) -> None:
        super().__init__()
        self.view = GenerateDocView()
        self.model = GenerateDocModel()

        self.on('before_display', self.on_before_display)
        self.view.on('back_clicked', lambda *_: self.goto_dashboard())

    def render(self):
        self.view.render(
            process_status=self.model.process_status
        )

        # process_status event handers
        self.view.process_status.on('action_clicked', self.process_status_action_clicked)

        # self.create_project()

    def on_before_display(self):
        self.view.reset_view()
        self.run()

    def goto_dashboard(self):
        show_page('home')

    def process_status_action_clicked(self, action):
        if action == 'back_dashboard':
            self.goto_dashboard()

    def run(self):
        self.view.process_status.set_status('loading')
        with self.view.process_status, chdir(Config.JAPPER_WORKING_DIR):
            try:
                run_command('pdoc --html --config show_source_code=False -o docs --force app ',
                            'Failed to generate documentation')

                self.view.process_status.set_status('success')

            except SystemExit as e:
                self.view.process_status.set_status('error')
                return
