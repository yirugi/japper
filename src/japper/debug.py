from IPython import get_ipython
from IPython.display import display
import ipywidgets as ipyw
import ipyvue
import ipyvuetify as v
import os

from .utils import run_js, run_js_with_wait


def is_dev():
    """
    Check if the app is running in dev mode. This is used to determine if we should show the debug view.
    JN_APP_DEV environment variable is set by the docker-compose file for the dev environment.
    """
    return os.getenv('JAPPER_APP_DEV', '0') == '1'


"""
The debug view is used to display debug messages. It is hidden by default.
"""
debug_output = None


class DebugView:
    def __init__(self):
        self.debug_view_inited = False
        self.debug_output = None
        self.debug_view_box = self.create_debug_view_box()

        self.debug_view_inited = True
        global debug_output
        debug_output = self.debug_output

    def display_debug_view(self):
        # jupyter-widgets-output-area output_wrapper
        display(self.debug_view_box)
        run_js_with_wait("""
                            document.body.appendChild(document.querySelector('.debug-view'));
                            document.querySelector('.debug-view .debug-output').style.display = 'none';
                        """, '.debug-view')

    def hide_debug_view(self, _=None):
        run_js("""
            document.querySelector('.debug-view').style.height = '50px';
            document.querySelector('.debug-view .debug-output').style.display = 'none';
            let btns = document.querySelectorAll('.debug-view button');
            btns[0].style.display = 'block';
            btns[1].style.display = 'none';
            btns[2].style.display = 'none';
        """)

    def show_debug_view(self, _=None):
        run_js("""
            document.querySelector('.debug-view').style.height = '270px';
            document.querySelector('.debug-view .debug-output').style.display = 'block';
            let btns = document.querySelectorAll('.debug-view button');
            btns[0].style.display = 'none';
            btns[1].style.display = 'block';
            btns[2].style.display = 'block';
        """)

    def create_debug_view_box(self):
        if self.debug_view_inited:
            return
        debug_output = ipyw.Output(layout={'width': '100%'})
        debug_output.add_class('debug-output')
        btn_hide = ipyw.Button(description="HIDE", layout={'width': '80px', 'display': 'none'})
        btn_hide.on_click(self.hide_debug_view)
        btn_clear = ipyw.Button(description="CLEAR", layout={'width': '80px', 'display': 'none'})
        btn_clear.on_click(lambda _: debug_output.clear_output())

        btn_show = ipyw.Button(description="SHOW DEBUG PANEL", layout={'width': 'fit-content'})
        btn_show.on_click(self.show_debug_view)

        debug_view_box = ipyw.VBox(children=[
            ipyw.HBox(children=[
                btn_show,
                btn_hide,
                btn_clear,
            ], layout={'height': '40px', 'overflow': 'hidden'}),
            ipyw.HBox(children=[
                debug_output,
            ])
        ], layout={'height': '50px'}
        )

        debug_view_box.add_class('debug-view')

        self.debug_output = debug_output
        return debug_view_box


debug_view = DebugView()


def debug_js(*msgs):
    """
    Print to the JS console
    @param msgs:
    """
    out = ' '.join([str(x) for x in msgs])
    run_js(f'console.log("%cJAPPER","background: #222; color: #bada55", "{out}");')


def debug(*msgs, forced_show=False):
    """
    Print to the debug view
    @param msgs:
    @return:
    """
    if not is_dev():
        return
    out = ' '.join([str(x) for x in msgs])
    with debug_output:
        print(out)
        run_js("""
            setTimeout(()=>{
                let output_div = document.querySelector('.debug-view .debug-output');
                output_div.scrollTo({top:output_div.scrollHeight, behavior: 'smooth'});
            }, 100);
        """)

        if forced_show:
            debug_view.show_debug_view()


# hook functions for capturing exceptions ======================================
@debug_output.capture()
def __call__(self, *args, **kwargs):
    """Call all the registered callbacks."""
    value = None
    for callback in self.callbacks:
        try:
            local_value = callback(*args, **kwargs)
        except Exception as e:
            # custom handler here
            debug('Exception:', e, forced_show=True)

            ip = get_ipython()
            if ip is None:
                self.log.warning("Exception in callback %s: %s", callback, e, exc_info=True)
            else:
                with debug_output:
                    ip.showtraceback()


        else:
            value = local_value if local_value is not None else value
    return value


@debug_output.capture()
def notify_change(self, change):
    try:
        ipyw.Widget.notify_change(self, change)
    except Exception as e:
        debug('Exception:', e, forced_show=True)
        ip = get_ipython()
        ip.showtraceback()


ipyw.CallbackDispatcher.__call__ = __call__

v.VuetifyTemplate.notify_change = notify_change
ipyvue.VueWidget.notify_change = notify_change

# =============================================================================
