import ipywidgets as ipyw
import os

from japper.debug import debug, debug_output
from japper.utils import run_js, run_js_with_wait
from japper_devtools.utils import set_devtool_interface

CONSOLE_HELPER_CLASS = 'console-output'
CONSOLE_HELPER_SELECTOR = '.' + CONSOLE_HELPER_CLASS

set_devtool_interface('forge')


class ConsoleHelperWidget(ipyw.Output):
    def __init__(self, working_dir=None, **kwargs):
        super().__init__(**kwargs)
        self.add_class(CONSOLE_HELPER_CLASS)

        self.working_dir = working_dir
        self._original_dir = os.getcwd()

        # for automatic scrolling
        run_js_with_wait("""
                let output_div = document.querySelector('%s');
                let observer = new MutationObserver((mutations) => {
                    mutations.forEach((mutation) => {
                        if (mutation.type === 'childList') {
                            output_div.scrollTo({top:output_div.scrollHeight, behavior: 'smooth'});
                        }
                    });
                });
                observer.observe(output_div, { childList: true, subtree: true });
            """ % CONSOLE_HELPER_SELECTOR, CONSOLE_HELPER_SELECTOR)

    def __enter__(self):

        super().__enter__()
        if self.working_dir is not None:
            os.chdir(self.working_dir)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.working_dir is not None:
            os.chdir(self._original_dir)
        super().__exit__(exc_type, exc_value, traceback)
