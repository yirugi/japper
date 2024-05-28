"""
This is a sample view for the home page.
"""
import ipyvuetify as v
from japper import PageView
from japper.app_config import AppConfig
from japper.debug import debug
from japper.utils import show_page
from ..commons.config import Config
from japper.style import JapperStyle


class HomeView(PageView):
    def __init__(self) -> None:
        """
        Create a new instance of HomeView. This is the view for the home page.
        """
        super().__init__()
        self.app_config = None
        self.japper_config = None
        self.action_cards = None
        self.set_style('padding:0px;max-width:100%;')

    def render(self, action_cards_data: list[dict]):
        """
        Render the view. This method is called by the framework to render the view.
        """

        # create action cards
        action_cards = []
        for card_data in action_cards_data:
            card = v.Card(
                link=True,
                disabled=card_data['disabled'],
                style_='min-width: 200px; max-width: 320px;height:320px;margin: 20px;border-radius: 20px;',
                class_="hover-grow pa-3",
                children=[
                    v.Img(src=card_data['image'], height=170, class_='mx-auto'),
                    v.CardTitle(class_="pb-1", style_="font-size:1.4em;color:#002a7e;", children=[card_data['title']]),
                    v.CardText(children=[
                        v.Html(tag='p', children=[card_data['description']]),
                    ]),
                ])

            action_cards.append(card)

        self.set_contents([
            v.Sheet(style_="""height: 100%; padding: 0px;background-color: #fafbfd;
                            """,
                    class_='mx-auto',
                    children=[
                        v.Container(
                            fluid=True,
                            class_='toolbar',
                            children=[
                                v.Container(
                                    style_="""
                                        padding: 20px 80px;
                                        """,
                                    class_='',
                                    children=[
                                        v.Html(tag='div',
                                               style_="""
                                                   font-size: 3.5em;
                                                   letter-spacing: 0.1rem;
                                                   margin-bottom: 20px;
                                                   color:#002a7e;""",
                                               children=['Manage your Japper project']),
                                        v.Html(tag='p', style_='font-size: 1.2em; color: #9ea8bb;max-width:800px;',
                                               children=[
                                                   'Japper Forge is a tool to manage your Japper projects. ' +
                                                   'You can create, build, run, deploy and document your projects.' +
                                                   ' You can also customize your application.']),
                                    ]
                                ),
                            ]
                        ),

                        v.Container(
                            fluid=True,
                            # style_='background-color: #f5f5f5;',
                            children=[
                                v.Container(
                                    class_='d-flex flex-wrap justify-center',
                                    style_='padding: 20px;max-width:1200px;',
                                    children=action_cards
                                )]
                        ),

                        v.Container(
                            fluid=True,
                            class_='d-flex justify-center',
                            style_='padding: 20px;max-width:1200px;',
                            children=[
                                v.Html(tag='p', style_='font-size: 1.2em; color: #9ea8bb;max-width:800px;',
                                       children=[
                                           'More features are coming soon. Stay tuned!']),
                            ]
                        ),

                    ]
                    )

        ])

        self.action_cards = action_cards
