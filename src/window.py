# window.py
#
# Copyright 2020 Latesil
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, GLib, Gio, Gdk
import re
import os

@Gtk.Template(resource_path='/org/github/Latesil/project-starter/window.ui')
class ProjectStarterWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ProjectStarterWindow'

    switch_btn = Gtk.Template.Child()
    second_btn = Gtk.Template.Child()
    change_path_btn = Gtk.Template.Child()
    main_view = Gtk.Template.Child()
    lang_btn = Gtk.Template.Child()
    template_btn = Gtk.Template.Child()
    lang_btn_box = Gtk.Template.Child()
    template_btn_box = Gtk.Template.Child()
    lang_revealer = Gtk.Template.Child()
    template_revealer = Gtk.Template.Child()
    project_name_entry = Gtk.Template.Child()
    project_id_entry = Gtk.Template.Child()
    path_entry = Gtk.Template.Child()
    python_btn = Gtk.Template.Child()
    rust_btn = Gtk.Template.Child()
    c_btn = Gtk.Template.Child()
    gui_gtk_btn = Gtk.Template.Child()
    cli_gtk_btn = Gtk.Template.Child()
    test_btn = Gtk.Template.Child()
    license_combo_box = Gtk.Template.Child()
    js_btn = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_path = ""
        self.switch_btn.props.sensitive = False
        self.project_name_ready = False
        self.project_id_ready = False
        self.project_name = ""
        self.project_id = ""
        self.is_git = True
        self.language = self.lang_btn.get_label()
        self.template = self.template_btn.get_label()
        self.license = self.license_combo_box.get_active_text()

        self.gui = ['GTK GUI Application']
        self.cli = ['GTK CLI Application']

    @Gtk.Template.Callback()
    def on_switch_btn_clicked(self, w):
        self.main_path = self.path_entry.props.text
        if self.main_path[:-1] == '/':
            self.main_path = self.main_path[:-1]
        if self.main_path[0] == '~':
            self.main_path = GLib.get_home_dir() + self.main_path[1:] + '/' + self.project_name
        else:
            self.main_path = self.main_path + '/' + self.project_name
        if not os.path.exists(self.main_path):
            os.makedirs(self.main_path)

        is_gui = self.check_gui(self.template)

        if self.language == 'Python':
            from .python_template import PythonTemplate
            self.complete_template = PythonTemplate(is_gui, self.project_id, self.project_name,
                                                    self.main_path, self.is_git, self.license)
        elif self.language == 'Rust':
            from .rust_template import RustTemplate
            self.complete_template = RustTemplate(is_gui, self.project_id, self.project_name,
                                                    self.main_path, self.is_git, self.license)
        elif self.language == 'C':
            from .c_template import CTemplate
            self.complete_template = CTemplate(is_gui, self.project_id, self.project_name,
                                                    self.main_path, self.is_git, self.license)
        elif self.language == 'JS':
            from .js_template import JsTemplate
            self.complete_template = JsTemplate(is_gui, self.project_id, self.project_name,
                                                    self.main_path, self.is_git, self.license)

        self.complete_template.start()

        self.main_view.set_visible_child_name('page1')

    @Gtk.Template.Callback()
    def on_second_btn_clicked(self, w):
        GLib.spawn_async(['/usr/bin/xdg-open', self.main_path])
        self.close()

    @Gtk.Template.Callback()
    def on_change_path_btn_clicked(self, btn):
        dialog = Gtk.FileChooserDialog(_("Choose a folder"), None, Gtk.FileChooserAction.SELECT_FOLDER,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.path_entry.props.text = dialog.get_filename()
        dialog.destroy()


    @Gtk.Template.Callback()
    def on_lang_btn_clicked(self, btn):
        if self.template_revealer.props.reveal_child:
            self.template_revealer.props.reveal_child = False

        self.lang_revealer.props.reveal_child = not self.lang_revealer.props.reveal_child

    @Gtk.Template.Callback()
    def on_template_btn_clicked(self, btn):
        if self.lang_revealer.props.reveal_child:
            self.lang_revealer.props.reveal_child = False

        self.template_revealer.props.reveal_child = not self.template_revealer.props.reveal_child

    @Gtk.Template.Callback()
    def on_project_name_entry_changed(self, e):
        if self.check_entry(e, self.check_project_name):
            self.project_name = e.props.text
            self.project_name_ready = True
            self.ready_check()


    @Gtk.Template.Callback()
    def on_project_id_entry_changed(self, e):
        if self.check_entry(e, self.check_project_id):
            self.project_id = e.props.text
            self.project_id_ready = True
            self.ready_check()

    @Gtk.Template.Callback()
    def on_git_enable_btn_toggled(self, b):
        if not b.props.active:
            self.is_git = False

    @Gtk.Template.Callback()
    def on_python_btn_toggled(self, b):
        self.button_toggled(b, 'lang')

    @Gtk.Template.Callback()
    def on_rust_btn_toggled(self, b):
        self.button_toggled(b, 'lang')

    @Gtk.Template.Callback()
    def on_c_btn_toggled(self, b):
        self.button_toggled(b, 'lang')

    @Gtk.Template.Callback()
    def on_js_btn_toggled(self, b):
        self.button_toggled(b, 'lang')

    @Gtk.Template.Callback()
    def on_gui_gtk_btn_toggled(self, b):
        self.button_toggled(b, 'template')

    @Gtk.Template.Callback()
    def on_cli_gtk_btn_toggled(self, b):
        self.button_toggled(b, 'template')

    @Gtk.Template.Callback()
    def on_license_combo_box_changed(self, cb):
        print(cb.get_active_text())

    @Gtk.Template.Callback()
    def on_test_btn_clicked(self, b):
        GLib.spawn_async(['/usr/bin/xdg-open', self.main_path])



    ##########################################################################

    def button_toggled(self, b, category):
        if category == 'lang':
            self.lang_btn.set_label(b.get_label())
            self.language = self.lang_btn.get_label()
            self.cli_gtk_btn.props.visible = False if self.language == 'Python' else True
            self.lang_revealer.props.reveal_child = False
        elif category == 'template':
            self.template_btn.set_label(b.get_label())
            self.template = self.template_btn.get_label()
            self.template_revealer.props.reveal_child = False
        else:
            print('there is no such category')

    def check_entry(self, e, func):
        text = e.props.text
        e.props.secondary_icon_name = ''
        if text:
            if not func(text):
                e.props.secondary_icon_name = 'dialog-warning-symbolic'
                return False
            else:
                e.props.secondary_icon_name = ''
                return True

    def check_project_name(self, text):
        if text:
            return False if text[0].isdigit() or re.search('\s', text) or not text.islower() else True

    def check_project_id(self, text):
        if text:
            return True if re.match('[a-zA-Z]+\.[a-zA-Z]+\.[a-zA-Z]+', text) else False

    def ready_check(self):
        self.switch_btn.props.sensitive = True if self.project_name_ready and self.project_id_ready else False

    def check_gui(self, t):
        return t in self.gui
        
