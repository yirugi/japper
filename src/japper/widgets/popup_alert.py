import functools

import ipyvuetify as v

ICON_MAP = {
    'error': 'mdi-alert-circle-outline',
    'info': 'mdi-information-outline',
    'success': 'mdi-check-circle-outline',
    'warning': 'mdi-alert-outline'
}


class PopupAlert:
    def __init__(self, main_view):
        self.main_view = main_view

    def confirm(self,
                msg: str,
                title: str = None,
                confirm_button_text='Confirm',
                cancel_button_text='Cancel',
                confirm_callback=None,
                cancel_callback=None):
        def close_alert(alert_widget, callback, widget, event, data):
            alert_widget.v_model = False
            if callback:
                callback()

        alert_dialog = v.Dialog(v_model=False,
                                max_width='400px',
                                scrollable=True,
                                )

        btn_cancel = v.Btn(class_='px-7', color='normal', rounded=True, children=[cancel_button_text])
        btn_cancel.on_event('click', functools.partial(close_alert, alert_dialog, cancel_callback))
        btn_confirm = v.Btn(class_='px-7', color='error', rounded=True, children=[confirm_button_text])
        btn_confirm.on_event('click', functools.partial(close_alert, alert_dialog, confirm_callback))

        alert_dialog.children = [
            v.Card(
                class_='text-center',
                style_="border-radius: 30px;padding:20px;",
                children=[
                    v.CardTitle(
                        class_='justify-center',
                        style_="font-size:1.5rem;font-weight:600;margin-bottom:10px;",
                        children=[title]),
                    v.CardText(style_="font-size:1.1rem;padding:10px 24px 30px;", children=[msg]),
                    v.CardActions(
                        class_='justify-center',
                        children=[

                            btn_confirm,
                            btn_cancel,

                        ])
                ])
        ]

        self.main_view.children = self.main_view.children + [alert_dialog]
        alert_dialog.v_model = True

    # def alert(self, msg, alert_type='success', icon=True):
    #     """
    #     :param msg:
    #     :param alert_type: success, error, info, warning
    #
    #     :param icon:
    #     :return:
    #     """
    #
    #     def close_alert(alert_widget, widget, event, data):
    #         alert_widget.v_model = False
    #
    #     alert = v.Snackbar(v_model=False,
    #                        top=True,
    #                        timeout=4000 if type != 'error' else 0,
    #                        color=alert_type,
    #                        style_='font-size:16px;',
    #                        transition="fade-transition")
    #
    #     btn_close = v.Btn(children=['Close'], text=True)
    #     btn_close.on_event('click', functools.partial(close_alert, alert))
    #
    #     icon_widget = []
    #     if icon:
    #         icon_widget = [v.Icon(left=True, dark=True, children=[ICON_MAP[alert_type]])]
    #     alert.children = icon_widget + [msg, v.Spacer(), btn_close]
    #
    #     self.main_view.children = self.main_view.children + [alert]
    #     alert.v_model = True
