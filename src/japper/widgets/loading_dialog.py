import ipyvuetify as v


class LoadingDialog(v.Dialog):
    def __init__(self, **kwargs):
        super().__init__(width='500px',
                         persistent=True,
                         v_model=False, **kwargs)

        self.msg = v.Html(tag='div', style_='font-size:1.1em;', class_='my-5', children=['Loading...'])
        self.children = [
            v.Card(outlined=True, style_='text-align:center;padding:20px;',
                   children=[
                       v.ProgressCircular(size=50, class_='mt-5', indeterminate=True, color="primary"),
                       self.msg
                   ])
        ]

    def show_loading(self, msg='Loading...'):
        self.msg.children = [msg]
        self.v_model = True

    def hide_loading(self):
        self.v_model = False
