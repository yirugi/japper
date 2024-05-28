"""
Logger helper for logging to Vue widgets
Any logger created with this class will be able to attach and detach widgets to it, so that the log messages will be
displayed in the widgets using v_model variable.

Usage:
    logger = VueWidgetLogger.get_logger()
    VueWidgetLogger.attach_widget_to_logger(txt_log_widget)
    logger.info('Hello, world! This is general log message')

    VueWidgetLogger.DATA_PROCESS = 'data_process'
    logger_data_process = VueWidgetLogger.get_logger(VueWidgetLogger.DATA_PROCESS)
    VueWidgetLogger.attach_widget_to_logger(txt_log_widget, VueWidgetLogger.DATA_PROCESS)
    logger_data_process.info('Hello, world! This is data process log message')
"""

import logging
from logging import StreamHandler
from .debug import debug


class VueWidgetLogger:
    GENERAL = 'general'
    pool = {}

    @staticmethod
    def get_logger(name: str = GENERAL):
        if name in VueWidgetLogger.pool:
            return VueWidgetLogger.pool[name]['logger']

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(VueWidgetLogger.DebugLogHandler())
        VueWidgetLogger.pool[name] = {'logger': logger, 'attached_widgets': []}

        return logger

    @staticmethod
    def attach_widget_to_logger(widget, name: str = GENERAL):
        if name not in VueWidgetLogger.pool:
            VueWidgetLogger.get_logger(name)

        VueWidgetLogger.pool[name]['attached_widgets'].append(widget)
        VueWidgetLogger.pool[name]['logger'].addHandler(VueWidgetLogger.WidgetLogHandler(widget))

    @staticmethod
    def detach_widget_from_logger(widget, name: str = GENERAL):
        if name not in VueWidgetLogger.pool:
            return

        VueWidgetLogger.pool[name]['attached_widgets'].remove(widget)
        VueWidgetLogger.pool[name]['logger'].removeHandler(VueWidgetLogger.WidgetLogHandler(widget))

    @staticmethod
    def detach_all_widgets_from_logger(name: str = GENERAL):
        if name not in VueWidgetLogger.pool:
            return

        for widget in VueWidgetLogger.pool[name]['attached_widgets']:
            VueWidgetLogger.pool[name]['logger'].removeHandler(VueWidgetLogger.WidgetLogHandler(widget))

        VueWidgetLogger.pool[name]['attached_widgets'] = []

    @staticmethod
    def set_terminator(terminator: str, logger: logging.Logger):
        for handler in logger.handlers:
            handler.terminator = terminator

    class DebugLogHandler(StreamHandler):
        def emit(self, record):
            msg = self.format(record)
            debug.debug(msg)

    class WidgetLogHandler(StreamHandler):
        def __init__(self, widget):
            super().__init__()
            self.widget = widget

        def emit(self, record):
            msg = self.format(record)
            self.widget.v_model = self.widget.v_model + msg + self.terminator

            debug.run_js("""
                setTimeout(()=>{
                    let elem = document.querySelector('#%s');
                    elem.scrollTo({top:elem.scrollHeight});
                }, 100);
            """ % self.widget.id)
