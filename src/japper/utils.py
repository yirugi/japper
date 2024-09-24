from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

import os
from IPython.display import display, HTML, Javascript
import base64
import hashlib

if TYPE_CHECKING:
    from .page import Page

js_output = None  # deprecated

ASSETS_PATH = 'app/assets/'


class ExternalFuncs:
    show_loading = None
    hide_loading = None
    toast_alert = None
    show_page = None
    popup_alert = None


_nav_menu = None


def get_nav_menu():
    return _nav_menu


def set_nav_menu(value):
    global _nav_menu
    _nav_menu = value


def set_browser_title(title):
    """
    Set the browser title using JS
    """
    display(HTML(f'<script>document.title = "{title}";</script>'))


def set_favicon(filepath):
    """
    Set the favicon using JS
    """
    display(HTML(f"""<script>
        var link = document.querySelector("link[rel*='icon']") || document.createElement('link');
        link.type = 'image/png';
        link.rel = 'shortcut icon';
        link.href = '{filepath}';
        document.getElementsByTagName('head')[0].appendChild(link);
        </script>
    """))


def set_external_funcs(show_loading_func, hide_loading_func, toast_alert_func, show_page_func, popup_alert_func):
    """
    The actual components and methods are implemented in the AppMainView class
    The connection is performed in the AppMainController class
    """
    ExternalFuncs.show_loading = show_loading_func
    ExternalFuncs.hide_loading = hide_loading_func
    ExternalFuncs.toast_alert = toast_alert_func
    ExternalFuncs.show_page = show_page_func
    ExternalFuncs.popup_alert = popup_alert_func


def show_page(page: int | str | Page):
    """
    Show a page by index, name, or page object
    """
    if ExternalFuncs.show_page is not None:
        ExternalFuncs.show_page(page)


def show_loading(msg='Loading...'):
    """
    Show loading dialog
    """
    if ExternalFuncs.show_loading is not None:
        ExternalFuncs.show_loading(msg)


def hide_loading():
    """
    Hide loading dialog
    """
    if ExternalFuncs.hide_loading is not None:
        ExternalFuncs.hide_loading()


def toast_alert(msg, alert_type='info', icon=True):
    """
    Show alert
    """
    if ExternalFuncs.toast_alert is not None:
        ExternalFuncs.toast_alert(msg, alert_type, icon)


def popup_confirm(msg, **kwargs):
    """
    Show popup alert
    """
    if ExternalFuncs.popup_alert is not None:
        ExternalFuncs.popup_alert.confirm(msg, **kwargs)


def set_js_output(output):  # deprecated
    global js_output
    js_output = output


def run_js(js):
    """
    Run JS code using the dedicated output widget
    This is a hack to fix the issue of the blank space at the bottom of the page when new JS is executed.
    @param js:
    @return:
    """
    if js_output is not None:
        js_output.append_display_data(Javascript(js))
        js_output.clear_output()
    else:
        display(Javascript(js))


def run_js_with_wait(js, selector):
    """
    Run JS code with a wait for a selector
    :param js:
    :param selector:
    :return:
    """
    run_js("""
        function waitForElement(selector, callBack){
          window.setTimeout(function(){
            var element = document.querySelector(selector);
            if(element){
              callBack(selector, element);
            }else{
              waitForElement(selector, callBack);
            }
          },500)
        }

        waitForElement('%s',function(selector, element){
            %s
        });
    """ % (selector, js))


def download_data(contents, filename, type):
    """
    Download data as a file
    """
    if type(contents) is str:
        contents = bytes(contents, 'utf-8')

    b64 = base64.b64encode(contents)
    payload = b64.decode()
    digest = hashlib.md5(contents).hexdigest()  # bypass browser cache
    id = f'dl_{digest}'

    # download via js script
    run_js(f"""
            const a = document.createElement('a');
            a.id = '{id}';
            a.style = 'display: none';
            a.href = 'data:application/octet-stream;base64,{payload}';
            a.download = '{filename}.{type}';
            document.body.appendChild(a);
            a.click();
            a.remove();
            """)


def download_file(filepath):
    with js_output:
        display(
            HTML(f"""
            <a id="tmp_download" download="{os.path.basename(filepath)}" href="{filepath}"></a>
            <script>
                (function download() {{
                    let elem = document.getElementById('tmp_download');
                    elem.click();
                    elem.remove();
                }})();
            </script>
        """))

    js_output.clear_output()


def inject_html(filepath):
    base_dir = os.path.dirname(__file__)
    display(HTML(filename=base_dir + '/' + filepath))


def inject_css(filepath):
    base_dir = os.path.dirname(__file__)
    with open(base_dir + '/' + filepath, 'r') as f:
        css = f.read()
        display(HTML(f"""
            <style>
                {css}
            </style>
        """))
