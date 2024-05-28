
"""
Home Presenter
"""
from japper import BasePresenter
from ..views import HomeView


class HomePresenter(BasePresenter):
    def __init__(self) -> None:
        """
        Create a new instance of HomePresenter. This class is used to manage the home page of the app.
        """
        super().__init__()
        self.view = HomeView()
        
