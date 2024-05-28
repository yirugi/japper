from enum import Enum

import ipyvuetify as v
from japper.debug import debug
from japper.japper_events import JapperEvents
from traitlets import link, directional_link, Any


class PromptWidgetTypes(Enum):
    TEXT = 'text'
    CONFIRM = 'confirm'
    SELECT = 'select'


class PromptWidget(v.Container, JapperEvents):
    value = Any("", allow_none=True).tag(sync=True)

    def __init__(self, prompt_text: str, description: str = None,
                 action_text: str = 'Continue',
                 action_color: str = 'primary',
                 action_callback: callable = None,
                 prompt_type: PromptWidgetTypes = PromptWidgetTypes.TEXT,
                 choices: list = None,
                 optional: bool = False, default_value: str | bool = None, validator: callable = None):
        super().__init__()
        self._japper_events = {}
        self.prompt_text = prompt_text
        self.description = description
        self.action_text = action_text
        self.action_color = action_color
        self.action_callback = action_callback
        self.prompt_type = prompt_type
        self.choices = choices if choices else []
        self.optional = optional
        self.default_value = default_value
        self.validator = validator

        self.__create_widget()

        self.style_ = """

        """
        self.class_ = "mx-auto text-center"

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __create_widget(self):
        # prompt text
        prompt_text = v.Container(
            style_='margin: 20px 0;',
            children=[
                v.Html(
                    tag='p',
                    class_="py-2 mb-0",
                    style_="font-size: 2.5em; font-weight: 500;color: #002a7e;",
                    children=[self.prompt_text]),
                v.Html(
                    tag='p',
                    class_="mx-auto",
                    style_="color: #9e9e9e;max-width: 70%;",
                    children=[self.description] if self.description else []),
            ]
        )

        # input
        prompt_input = ''
        if self.prompt_type == PromptWidgetTypes.TEXT:
            prompt_input = v.TextField(
                class_='prompt-textfield',
                v_model=self.default_value,
                style_='max-width: 400px; font-size: 1.5em;',
            )

            prompt_input.on_event('keyup', self.on_textfield_keyup)

        elif self.prompt_type == PromptWidgetTypes.SELECT:
            prompt_input = v.BtnToggle(
                group=True,
                class_='prompt-choice',
                color='success',
                v_model=self.default_value,
                children=[
                    v.Btn(
                        class_='prompt-choice-btn',
                        children=[choice],
                        value=choice,
                    ) for choice in self.choices
                ]
            )
        elif self.prompt_type == PromptWidgetTypes.CONFIRM:
            prompt_input = v.BtnToggle(
                group=True,
                class_='prompt-choice',
                v_model=self.default_value,
                children=[
                    v.Btn(
                        class_='prompt-choice-btn',
                        children=['Yes'],
                        value=True,
                        style_='color:green;'
                    ),
                    v.Btn(
                        class_='prompt-choice-btn',
                        children=['No'],
                        value=False,
                        style_='color:red;'
                    )
                ]
            )

        link((prompt_input, 'v_model'), (self, 'value'))

        prompt_input.on_event('change', self.on_prompt_change)

        self.validator_msg = v.Html(tag='p', style_="color: red; font-size: 1.1em;")

        self.btn_action = v.Btn(
            style_="min-width:150px;",
            color=self.action_color,
            large=True,
            rounded=True,
            children=[self.action_text],
            on_click=self.on_action_click,
        )

        actions = v.Container(
            style_='margin-top: 80px;',
            children=[
                self.btn_action
            ]
        )

        self.children = [
            prompt_text,
            v.Container(
                class_='d-flex justify-center',
                children=[prompt_input],
            ),
            self.validator_msg,
            actions,
        ]

    def on_action_click(self, widget, event, data):
        self.value = self.value.strip() if isinstance(self.value, str) else self.value
        if not self.optional and not self.value:
            self.validator_msg.children = ['This field is required']
            return

        if not self.validate(self.value):
            return

        if self.action_callback:
            self.action_callback(self.value)

    def validate(self, value):
        if self.validator:
            if (result := self.validator(value)) not in [True, None]:
                self.validator_msg.color = 'error'
                self.validator_msg.children = [result]
                return False
            else:
                self.validator_msg.children = []
        return True

    def on_prompt_change(self, widget, event, data):
        self.emit('change', data)

    def on_textfield_keyup(self, widget, event, data):
        self.emit('keyup', data['key'])
        if data['key'] == 'Enter':
            self.on_action_click(widget, event, data)
        else:
            self.validate(self.value)

    def set_error_msg(self, error_msg):
        self.validator_msg.color = 'error'
        self.validator_msg.children = [error_msg]

    def set_info_msg(self, info_msg):
        self.validator_msg.color = 'info'
        self.validator_msg.children = [info_msg]

    def set_action_text(self, action_text):
        self.action_text = action_text
        self.btn_action.children = [action_text]

    def set_action_color(self, action_color):
        self.action_color = action_color
        self.btn_action.color = action_color
