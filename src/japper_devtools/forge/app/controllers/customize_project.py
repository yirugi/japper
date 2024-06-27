from japper import PageController
from japper.debug import debug
from japper.utils import show_page, toast_alert, popup_confirm

from ..widgets.img_input import ImgInput
from ..views import CustomizeProjectView
from ..models import CustomizeProjectModel


class CustomizeProjectController(PageController):
    def __init__(self) -> None:
        super().__init__()
        self.view = CustomizeProjectView()
        self.model = CustomizeProjectModel()

        self.on('before_display', self.on_before_display)

    def render(self):
        app_config = self.model.load_app_config()

        self.view.render(
            # side_menu_items=self.model.side_menu_items,
            app_config=app_config,
            setting_panels_info=self.model.generate_setting_panels_info(app_config)
        )

        self.view.on('side_menu_clicked', self.side_menu_clicked)
        self.view.on('setting_changed', self.setting_changed)
        self.view.on('save_changes_clicked', self.save_changes_clicked)
        self.view.on('page_list_button_clicked', self.page_list_button_clicked)
        self.view.on('page_list_changed', self.page_list_changed)
        self.view.on('page_setting_back_to_page_list_clicked', self.page_setting_back_to_page_list_clicked)
        self.view.on('page_delete_clicked', self.page_delete_clicked)
        self.view.on('add_page_clicked', self.add_page_clicked)

    def on_before_display(self):
        pass

    def side_menu_clicked(self, menu_name):
        if menu_name == 'dashboard':
            if not self.view.btn_save_changes.disabled:
                popup_confirm("You have unsaved changes. Are you sure you want to leave?", title='Unsaved Changes?',
                              confirm_callback=lambda: show_page('home'))
            # show_page('home')
        else:
            self.view.show_settings_panel(menu_name)

    def setting_changed(self, setting_name, widget, event, data):
        debug(f"Setting changed: {setting_name} = {widget.v_model}, {data}")
        value = widget.v_model
        if isinstance(widget, ImgInput):
            value = data
            self.model.widgets_to_apply_changes.append({'widget': widget, 'setting_name': setting_name})

        self.model.set_config_value(setting_name, value)

        self.view.btn_save_changes.disabled = False
        self.view.update_preview(self.model.app_config)

    def save_changes_clicked(self, *_):
        debug(f"Save changes clicked")
        for widget in self.model.widgets_to_apply_changes:
            widget['widget'].apply_changes()

        # self.model.app_config.save()
        self.model.save_app_config()

        self.view.btn_save_changes.disabled = True
        self.model.widgets_to_apply_changes = []

        toast_alert('Changes saved', 'success')

    def page_list_button_clicked(self, btn_name, page_title, *args):
        debug(f"Page list button clicked: {btn_name}, {page_title}")
        if btn_name == 'edit':
            self.view.show_app_pages_page_setting(page_title)
        elif btn_name == 'delete':
            self.page_delete_clicked(page_title)
        elif btn_name == 'default':
            self.model.set_default_page(page_title)
            self.refresh_app_pages_setting(page_list_only=True)
            self.view.show_app_pages_page_list()
            self.view.btn_save_changes.disabled = False

    def page_setting_back_to_page_list_clicked(self, *args):
        debug(f"Back to page list clicked")
        self.refresh_app_pages_setting(page_list_only=True)
        self.view.show_app_pages_page_list()

    def page_delete_clicked(self, page_title, *args):
        def delete_page():
            self.model.delete_page(page_title)
            self.refresh_app_pages_setting(page_list_only=True, forced_page_index=0)
            toast_alert(f"Page '{page_title}' deleted", 'success')

        # TODO: remove all changes related to this page

        debug(f"Page delete clicked: {page_title}")
        popup_confirm(f"Are you sure you want to delete page '{page_title}'?", title='Delete Page?',
                      confirm_callback=delete_page)

    def add_page_clicked(self, *args):
        debug(f"Add page clicked")
        self.view.open_add_page_dialog(self.model.get_page_templates(), self.add_page)

    def add_page(self, page_title, template_name):
        debug(f"Add page: {page_title}, {template_name}")
        try:
            self.model.add_page(page_title, template_name)
        except Exception as e:
            toast_alert('Adding page failed: ' + str(e), 'error')
            raise e
            return

        self.refresh_app_pages_setting(forced_page_index=len(self.model.app_config.pages) - 1)
        # self.view.btn_save_changes.disabled = False
        toast_alert(f"Page '{page_title}' added", 'success')

    def refresh_app_pages_setting(self, page_list_only=False, forced_page_index=None):
        self.view.update_page_list(self.model.app_config.pages)
        self.view.update_preview(self.model.app_config, page_index=forced_page_index)

        if page_list_only:
            return

        page_setting_panels_info = self.model.generate_page_setting_panels_info(self.model.app_config)
        self.view.update_page_settings(page_setting_panels_info['components'][0]['page_settings'])

    def page_list_changed(self, widget, *args):
        debug(f"Page list button changed {widget.v_model}")
        self.view.update_preview_app(self.model.app_config, page_index=widget.v_model)
