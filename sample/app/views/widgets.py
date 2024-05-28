import ipyvuetify as v
from japper.debug import debug
import ipywidgets as ipyw
from japper import BaseView


class WidgetsView(BaseView):
    def __init__(self) -> None:
        super().__init__(style_='padding-bottom: 60px;')

    def render(self):
        self.children = [

            v.Html(tag='div', class_='content-title mb-0', children=['Vuetify 2 Widget Examples']),
            v.Html(tag='div', class_='d-flex align-center', children=[
                'Full list of Vuetify 2 widgets can be found here: ',
                v.Btn(text=True, style_='color: green',
                      children=[v.Icon(children=['mdi-link']), 'Vuetify 2 documentation page'],
                      href='https://v2.vuetifyjs.com/en/', target='_blank'),
            ]),
            self.create_ipyvuetify_widget_cases(),
            self.create_dialog_case(),
        ]

    def create_ipyvuetify_widget_cases(self):
        return v.Container(fluid=True, children=[
            # Buttons
            v.Card(class_='my-5', children=[
                v.CardTitle(children=['Buttons']),
                v.CardText(children=[
                    v.Btn(color='primary', children=['PRIMARY']),
                    v.Btn(class_='ml-5', color='success', children=[v.Icon(children=['mdi-check']), 'SUCCESS']),
                    v.Btn(class_='ml-5', fab=True, dark=True, small=True, color='pink',
                          children=[v.Icon(children=['mdi-heart'])]),
                    v.Btn(class_='ml-5', icon=True, color='deep-orange', children=[v.Icon(children=['mdi-thumb-up'])]),
                    v.Btn(class_='ml-5', outlined=True, color='indigo', children=['OUTLINED']),
                    v.Btn(class_='ml-5', rounded=True, color='warning', children=['ROUNDED BUTTON']),
                    v.Btn(class_='ml-5', x_large=True, color='secondary', children=['EXTRA LARGE']),

                ]),
            ]),
            # Selects
            v.Card(class_='my-5', children=[
                v.CardTitle(children=['Selects']),
                v.CardText(children=[
                    v.Row(children=[
                        v.Col(cols=6, children=[
                            v.Select(label='Select', items=['Option 1', 'Option 2', 'Option 3']),
                            v.Select(label='Select multiple', multiple=True,
                                     items=['Option 1', 'Option 2', 'Option 3']),
                            v.Select(label='Select with chips', chips=True, multiple=True,
                                     items=['Option 1', 'Option 2', 'Option 3']),
                        ]),
                        v.Col(cols=6, children=[
                            v.Select(label='Outlined', items=['Option 1', 'Option 2', 'Option 3'], outlined=True),
                            v.Select(label='Filled', items=['Option 1', 'Option 2', 'Option 3'], filled=True),
                            v.Select(label='Dense', items=['Option 1', 'Option 2', 'Option 3'], dense=True),
                        ]),
                    ]),

                ]),
            ]),
            # Text fields
            v.Card(class_='my-5', children=[
                v.CardTitle(children=['Text fields']),
                v.CardText(children=[
                    v.Row(children=[
                        v.Col(cols=6, children=[
                            v.TextField(label='Standard'),
                            v.TextField(label='Outlined', outlined=True),
                            v.TextField(label='Filled', filled=True),
                            v.TextField(label='Dense', dense=True),
                        ]),
                        v.Col(cols=6, children=[
                            v.TextField(label='Disabled', disabled=True),
                            v.TextField(label='Readonly', readonly=True),
                            v.TextField(label='Counter', counter=True, max=10),
                            v.TextField(label='Hint text', placeholder='Hint text'),
                        ]),
                    ]),
                ]),
            ]),
            # Textareas
            v.Card(class_='my-5', children=[
                v.CardTitle(children=['Textareas']),
                v.CardText(children=[
                    v.Row(children=[
                        v.Col(cols=6, children=[
                            v.Textarea(label='Standard'),
                            v.Textarea(label='Outlined', outlined=True),
                        ]),
                        v.Col(cols=6, children=[
                            v.Textarea(label='Disabled', disabled=True),
                            v.Textarea(label='Counter', counter=True, max=10),
                        ]),
                    ]),
                ]),
            ]),
            v.Row(children=[
                v.Col(cols=4, children=[
                    # Checkboxes
                    v.Card(children=[
                        v.CardTitle(children=['Checkboxes']),
                        v.CardText(children=[
                            v.Checkbox(label='Standard'),
                            v.Checkbox(label='Disabled', disabled=True),
                            v.Checkbox(label='Readonly', readonly=True),
                            v.Checkbox(label='Indeterminate', indeterminate=True),
                        ]),
                    ]),
                ]),
                v.Col(cols=4, children=[
                    # Radio buttons
                    v.Card(children=[
                        v.CardTitle(children=['Radio buttons']),
                        v.CardText(children=[
                            v.RadioGroup(v_model='radio', children=[
                                v.Radio(label='Standard', value='radio'),
                                v.Radio(label='Disabled', value='radio', disabled=True),
                                v.Radio(label='Readonly', value='radio', readonly=True),
                                v.Radio(label='Red', value='radio', color='red'),
                            ]),
                        ]),
                    ]),
                ]),
                v.Col(cols=4, children=[
                    # Switches
                    v.Card(children=[
                        v.CardTitle(children=['Switches']),
                        v.CardText(children=[
                            v.Switch(label='Standard'),
                            v.Switch(label='Disabled', disabled=True),
                            v.Switch(label='Readonly', readonly=True),
                        ]),
                    ]),
                ]),
            ]),
            v.Row(children=[
                v.Col(cols=6, children=[
                    # Range sliders
                    v.Card(children=[
                        v.CardTitle(children=['Range sliders']),
                        v.CardText(children=[
                            v.RangeSlider(v_model=[25, 75]),
                        ]),
                    ]),
                ]),
                v.Col(cols=6, children=[
                    # Sliders
                    v.Card(children=[
                        v.CardTitle(children=['Sliders']),
                        v.CardText(children=[
                            v.Slider(v_model=50),
                        ]),
                    ]),
                ]),
            ]),
            v.Row(children=[
                v.Col(cols=6, children=[
                    # Progress circular
                    v.Card(children=[
                        v.CardTitle(children=['Progress circular']),
                        v.CardText(children=[
                            v.ProgressCircular(value=75),
                            v.ProgressCircular(class_='ml-5', value=25, color='red'),
                            v.ProgressCircular(class_='ml-5', value=55, size='70', children=['55%'], color='green'),
                            v.ProgressCircular(class_='ml-5', indeterminate=True),

                        ]),
                    ]),
                ]),
                v.Col(cols=6, children=[
                    # Progress linear
                    v.Card(children=[
                        v.CardTitle(children=['Progress linear']),
                        v.CardText(children=[
                            v.ProgressLinear(value=75),
                            v.ProgressLinear(class_='mt-2', buffer_value=75, stream=True, color='green'),
                            v.ProgressLinear(class_='mt-2', indeterminate=True, color='red'),
                            v.ProgressLinear(class_='mt-2', value=75, striped=True, height='10', color='orange'),
                        ]),
                    ]),
                ]),
            ]),

            # Data tables
            v.Card(class_='my-5', children=[
                v.CardTitle(children=['Data tables']),
                v.CardText(children=[
                    v.DataTable(
                        headers=[
                            {'text': 'Name', 'value': 'name'},
                            {'text': 'Category', 'value': 'category'},
                            {'text': 'Subcategory', 'value': 'subcategory'},
                        ],
                        items=[
                            {'name': 'Item 1', 'category': 'Category 1', 'subcategory': 'Subcategory 1'},
                            {'name': 'Item 2', 'category': 'Category 2', 'subcategory': 'Subcategory 2'},
                            {'name': 'Item 3', 'category': 'Category 3', 'subcategory': 'Subcategory 3'},
                            {'name': 'Item 4', 'category': 'Category 4', 'subcategory': 'Subcategory 4'},
                        ],
                    ),
                ]),
            ]),
            # Chips
            v.Card(class_='my-5', children=[
                v.CardTitle(children=['Chips']),
                v.CardText(children=[
                    v.Row(children=[
                        v.Col(cols=6, children=[
                            v.Chip(children=['Default']),
                            v.Chip(class_='ml-5', label=True, children=['Label']),
                            v.Chip(class_='ml-5', outlined=True, children=['Outlined']),
                            v.Chip(class_='ml-5', small=True, children=['Small']),
                            v.Chip(class_='ml-5', disabled=True, children=['Disabled']),
                            v.Chip(class_='ml-5', close=True, children=['Close']),
                        ]),
                        v.Col(cols=6, children=[
                            v.Chip(class_='ml-5', color='red', children=['Red']),
                            v.Chip(class_='ml-5', color='green', children=['Green']),
                            v.Chip(class_='ml-5', color='blue', children=['Blue']),
                            v.Chip(class_='ml-5', color='orange', children=['Orange']),
                            v.Chip(class_='ml-5', color='purple', children=['Purple']),
                            v.Chip(class_='ml-5', color='pink', children=['Pink']),
                        ]),
                    ]),
                ]),
            ]),
            # Alerts
            v.Card(class_='my-5', children=[
                v.CardTitle(children=['Alerts']),
                v.CardText(children=[
                    v.Alert(children=['Default']),
                    v.Alert(class_='mt-5', color='success', children=['Success']),
                    v.Alert(class_='mt-5', color='info', children=['Info']),
                    v.Alert(class_='mt-5', color='warning', children=['Warning']),
                    v.Alert(class_='mt-5', color='error', children=['Error']),
                ]),
            ]),

            # Expansion panels
            v.Card(class_='my-5', children=[
                v.CardTitle(children=['Expansion panels']),
                v.CardText(children=[
                    v.ExpansionPanels(children=[
                        v.ExpansionPanel(children=[
                            v.ExpansionPanelHeader(children=['Item 1']),
                            v.ExpansionPanelContent(children=['Item 1 content']),
                        ]),
                        v.ExpansionPanel(children=[
                            v.ExpansionPanelHeader(children=['Item 2']),
                            v.ExpansionPanelContent(children=['Item 2 content']),
                        ]),
                        v.ExpansionPanel(children=[
                            v.ExpansionPanelHeader(children=['Item 3']),
                            v.ExpansionPanelContent(children=['Item 3 content']),
                        ]),
                    ]),
                ]),
            ]),
            v.Row(children=[
                v.Col(cols=4, children=[
                    # Color pickers
                    v.Card(height='100%', children=[
                        v.CardTitle(children=['Color pickers']),
                        v.CardText(class_='d-flex justify-center', children=[
                            v.ColorPicker(v_model='red'),
                        ]),
                    ]),
                ]),
                v.Col(cols=4, children=[
                    # Date pickers
                    v.Card(height='100%', children=[
                        v.CardTitle(children=['Date pickers']),
                        v.CardText(class_='d-flex justify-center', children=[
                            v.DatePicker(v_model='2020-01-01'),
                        ]),
                    ]),
                ]),
                v.Col(cols=4, children=[
                    # Time pickers
                    v.Card(height='100%', children=[
                        v.CardTitle(children=['Time pickers']),
                        v.CardText(class_='d-flex justify-center', children=[
                            v.TimePicker(v_model='07:30'),
                        ]),
                    ]),
                ]),
            ]),

            v.Row(children=[
                # Card Example
                v.Col(cols=5, children=[
                    v.Card(children=[
                        v.Img(src="https://cdn.vuetifyjs.com/images/cards/cooking.png", height='250px'),
                        v.CardTitle(children=['Cafe Badilico']),
                        v.CardText(children=[
                            v.Row(align='center', class_='mx-0', children=[
                                v.Rating(v_model=4.5, dense=True, color='amber', readonly=True, half_increments=True,
                                         size=14),
                                v.Html(tag='div', class_='grey--text ms-4', children=['4.5 (413)']),
                            ]),
                            v.Html(tag='div', class_='my-4 text-subtitle-1', children=['$ • Italian, Cafe']),
                            v.Html(tag='div', children=[
                                'Small plates, salads & sandwiches - an intimate setting with 12 indoor seats plus patio seating.']),
                        ]),
                        v.Divider(class_='mx-4'),
                        v.CardTitle(children=['Tonight\'s availability']),
                        v.CardText(children=[
                            v.ChipGroup(active_class="deep-purple accent-4 white--text", column=True, children=[
                                v.Chip(children=['5:00 PM']),
                                v.Chip(children=['6:00 PM']),
                                v.Chip(children=['7:00 PM']),
                                v.Chip(children=['8:00 PM']),
                            ]),
                        ]),
                        v.CardActions(children=[
                            v.Btn(color='deep-purple lighten-2', text=True, children=['Reserve']),
                        ]),
                    ])
                ]),
                v.Col(children=[
                    self.create_stepper_case()
                ])
            ]),

        ])

    def create_stepper_case(self):
        stepper = v.Stepper(v_model=1)

        def next_step(widget, event, data):
            stepper_model = stepper.v_model
            stepper_model += 1
            if stepper_model > 3:
                stepper_model = 1
            stepper.v_model = stepper_model

        def prev_step(widget, event, data):
            stepper_model = stepper.v_model
            stepper_model -= 1
            if stepper_model < 1:
                stepper_model = 3
            stepper.v_model = stepper_model

        def check_complete(step):
            return stepper.v_model > step

        next_btn = v.Btn(color='primary', children=['Next'])
        next_btn.on_event('click', next_step)

        prev_btn = v.Btn(color='warning', children=['Prev'], class_='mr-3')
        prev_btn.on_event('click', prev_step)

        stepper.children = [
            v.StepperHeader(children=[
                v.StepperStep(complete=check_complete(1), step='1', children=['Step 1']),
                v.Divider(),
                v.StepperStep(complete=check_complete(2), step='2', children=['Step 2']),
                v.Divider(),
                v.StepperStep(complete=check_complete(3), step='3', children=['Step 3']),
            ]),
            v.StepperItems(children=[
                v.StepperContent(step='1', children=[
                    v.Card(class_='mb-12', color='grey lighten-1', height='200px'),
                    prev_btn,
                    next_btn
                ]),
                v.StepperContent(step='2', children=[
                    v.Card(class_='mb-12', color='grey lighten-1', height='200px'),
                    prev_btn,
                    next_btn
                ]),
                v.StepperContent(step='3', children=[
                    v.Card(class_='mb-12', color='grey lighten-1', height='200px'),
                    prev_btn,
                    next_btn
                ]),
            ]),
        ]

        return v.Card(children=[stepper])

    def create_dialog_case(self):
        btn_open_dialog = v.Btn(color='primary', children=['OPEN DIALOG'])
        btn_open_dialog.on_event('click', lambda *_: setattr(dialog, 'v_model', True))
        btn_close_dialog = v.Btn(color='secondary', children=['CLOSE'])
        btn_close_dialog.on_event('click', lambda *_: setattr(dialog, 'v_model', False))
        dialog = v.Dialog(v_model=False, width='500px', children=[
            v.Card(children=[
                v.CardTitle(children=['Dialog']),
                v.CardText(children=['This is a dialog.']),
                v.CardActions(children=[
                    v.Spacer(),
                    btn_close_dialog,
                ]),
            ]),
        ])

        # full screen dialog
        btn_open_full_screen_dialog = v.Btn(class_='ml-5', color='success', children=['FULLSCREEN DIALOG'])
        btn_open_full_screen_dialog.on_event('click', lambda *_: setattr(full_screen_dialog, 'v_model', True))
        btn_close_full_screen_dialog = v.Btn(icon=True, dark=True, children=[v.Icon(children=['mdi-close'])])
        btn_close_full_screen_dialog.on_event('click', lambda *_: setattr(full_screen_dialog, 'v_model', False))
        full_screen_dialog = v.Dialog(v_model=False, fullscreen=True, transition="dialog-bottom-transition",
                                      hide_overlay=True,
                                      children=[
                                          v.Card(children=[
                                              v.Toolbar(dark=True, color='primary', children=[
                                                  btn_close_full_screen_dialog,
                                                  v.ToolbarTitle(children=['Full screen dialog']),

                                              ]),
                                              v.CardTitle(children=['Full screen dialog']),
                                              v.CardText(children=['This is a full screen dialog.']),
                                          ]),
                                      ])

        return v.Card(class_='ml-3', children=[
            v.CardTitle(children=['Dialog']),
            v.CardText(children=[
                btn_open_dialog,
                dialog,
                btn_open_full_screen_dialog,
                full_screen_dialog,
            ]),
        ])
