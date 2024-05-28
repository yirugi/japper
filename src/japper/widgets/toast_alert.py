import functools

import ipyvuetify as v

ICON_MAP = {
    'error': 'mdi-alert-circle-outline',
    'info': 'mdi-information-outline',
    'success': 'mdi-check-circle-outline',
    'warning': 'mdi-alert-outline'
}


class ToastAlert:
    def __init__(self, main_view):
        self.main_view = main_view
        self.toast = None

    def alert(self, msg, alert_type='success', icon=True):
        """
        :param msg:
        :param alert_type: success, error, info, warning

        :param icon:
        :return:
        """

        def close_alert(alert_widget, widget, event, data):
            alert_widget.v_model = False

        alert = v.Snackbar(v_model=False,
                           top=True,
                           timeout=4000 if type != 'error' else 0,
                           color=alert_type,
                           style_='font-size:16px;',
                           transition="fade-transition")

        btn_close = v.Btn(children=['Close'], text=True)
        btn_close.on_event('click', functools.partial(close_alert, alert))

        icon_widget = []
        if icon:
            icon_widget = [v.Icon(left=True, dark=True, children=[ICON_MAP[alert_type]])]
        alert.children = icon_widget + [msg, v.Spacer(), btn_close]

        self.main_view.children = self.main_view.children + [alert]
        alert.v_model = True
