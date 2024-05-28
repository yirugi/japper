from .japper_events import JapperEvents


class PageController(JapperEvents):
    def __init__(self) -> None:
        super().__init__()
        self.view = None
        self.model = None

    def render(self):
        self.view.render()

    def get_content(self):
        self.emit('before_display')
        return self.view
