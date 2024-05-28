import ipyvuetify as v
from functools import partial
from traitlets import TraitType, link
from ipyvuetify import generated

"""
General widget overrides
"""


def add_event_handler(self, event, value):
    """
    Adds a custom event handler to the widget
    """
    if callable(value):  # when only handler function is passed
        self.on_event(event, value)
    elif isinstance(value,
                    (tuple, dict)):  # when handler function and args are passed or when params are passed as a dict
        args = value.get('args', value[1:]) if isinstance(value, dict) else value[1:]
        handler = value.get('handler', value[0]) if isinstance(value, dict) else value[0]
        self.on_event(event, partial(handler, *args))
    else:
        raise ValueError(f"Invalid value for {event}")


def override_widget(widget_name, widget):
    """
    Overrides a widget to add features:
    - Adds custom event handlers. If an argument starts with 'on_', it is considered as an event and its value is added
    as an event handler. Arguments can be a callable or a tuple or a dict containing the handler function and its arguments
      - Example: {'on_click': my_handler} will add my_handler as a click event handler
      - Example: {'on_click': (my_handler, arg1, arg2)} will add my_handler(arg1, arg2) as a click event handler
      - Example: {'on_click': {'handler': my_handler, 'args': (arg1, arg2)}} will add my_handler(arg1, arg2) as a click event handler
    - Links the v_model trait with the v_model attribute if it is a TraitType

    Parameters:
    widget_name (str): The name of the widget to override
    widget (object): The original widget object
    """

    class CustomWidget(widget):
        def __init__(self, **kwargs):
            """
            Initializes the custom widget.
            """
            super().__init__(**kwargs)
            for key, value in kwargs.items():
                if key.startswith('on_'):
                    add_event_handler(self, key[3:], value)

            if 'v_model_link' in kwargs:
                link((kwargs['v_model_link'][0], kwargs['v_model_link'][1]), (self, 'v_model'))

    setattr(v, widget_name, CustomWidget)


# Get all widget names from the generated module of ipyvuetify
vuetify_widget_names = [x for x in dir(generated) if not x.startswith('__')]

# Override each widget with a custom widget
for widget_name in vuetify_widget_names:
    override_widget(widget_name, getattr(generated, widget_name))

"""
TextField overrides
TODO: Fix it by handling multiple events of vuetify widget

- Fixes the rules attribute to work
- Added 'rule_event' parameter to specify the event to listen to
"""

# class CustomTextField(v.TextField):
#
#     def __init__(self, rules: list[callable] = None, rule_event: str = 'change', **kwargs):
#         super().__init__(**kwargs)
#
#         if rules is None:
#             rules = []
#         elif not isinstance(rules, list):
#             rules = [rules]
#
#         self.__rules: list[callable] = rules
#         self.on_event(rule_event, self.on_value_changed)
#
#     def on_value_changed(self, widget, event, data):
#         self.rules = [rule(self.v_model) for rule in self.__rules]
#         self.error = any([False if rule is False else True for rule in self.rules])
#
#
# v.TextField = CustomTextField
