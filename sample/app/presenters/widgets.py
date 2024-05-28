from japper import BasePresenter
from ..views import WidgetsView


class WidgetsPresenter(BasePresenter):
    def __init__(self) -> None:
        super().__init__()
        self.view = WidgetsView()
