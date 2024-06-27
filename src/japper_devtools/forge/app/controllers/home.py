"""
Home Controller
"""
from functools import partial

from japper import PageController
from japper.debug import debug
from japper.utils import show_page, popup_confirm

from ..views import HomeView
from ..models import HomeModel
from ..commons.utils import get_japper_config


class HomeController(PageController):
    def __init__(self) -> None:
        super().__init__()
        self.app_config = None
        self.japper_config = None
        self.view = HomeView()
        self.model = HomeModel()

    def render(self):
        # get configs
        self.japper_config = get_japper_config()

        action_cards_data = self.model.action_cards.copy()

        for card in action_cards_data:
            card['disabled'] = (card['page'] != 'new project') if self.japper_config is None else (
                    card['page'] == 'new project')

        self.view.render(
            action_cards_data=action_cards_data
        )

        for i, action_card in enumerate(self.view.action_cards):
            page_name = self.model.action_cards[i]['page']
            action_card.on_event('click', partial(self.on_action_card_click, page_name))

    def on_action_card_click(self, page_name, widget, event, data):
        """
        Handle action card click event.
        """
        show_page(page_name)
