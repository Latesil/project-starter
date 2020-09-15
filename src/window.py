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
import os.path
from os import path
from locale import gettext as _
from .about_window import AboutWindow
from .keyboard_shortcuts import KeyboardShortcutsWindow


@Gtk.Template(resource_path='/com/github/Latesil/project-starter/window.ui')
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
    license_combo_box = Gtk.Template.Child()
    js_btn = Gtk.Template.Child()
    gnome_extension_btn = Gtk.Template.Child()
    gnome_ext_revealer = Gtk.Template.Child()
    license_revealer = Gtk.Template.Child()
    gnome_ext_entry = Gtk.Template.Child()
    gnome_ext_description_entry = Gtk.Template.Child()
    gnome_ext_uuid_entry = Gtk.Template.Child()
    path_exists_revealer = Gtk.Template.Child()
    close_path_exists_btn = Gtk.Template.Child()
    about_btn = Gtk.Template.Child()
    keyboard_shortcuts_btn = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        ##########################

        accel = Gtk.AccelGroup()
        accel.connect(Gdk.keyval_from_name('p'), Gdk.ModifierType.CONTROL_MASK, 0, self.python_set)
        accel.connect(Gdk.keyval_from_name('j'), Gdk.ModifierType.CONTROL_MASK, 0, self.js_set)
        accel.connect(Gdk.keyval_from_name('c'), Gdk.ModifierType.CONTROL_MASK, 0, self.c_set)
        accel.connect(Gdk.keyval_from_name('r'), Gdk.ModifierType.CONTROL_MASK, 0, self.rust_set)
        accel.connect(Gdk.keyval_from_name('g'), Gdk.ModifierType.CONTROL_MASK, 0, self.gui_set)
        accel.connect(Gdk.keyval_from_name('t'), Gdk.ModifierType.CONTROL_MASK, 0, self.cli_set)
        accel.connect(Gdk.keyval_from_name('e'), Gdk.ModifierType.CONTROL_MASK, 0, self.extension_set)
        self.add_accel_group(accel)

        ##########################

        self.main_path = ""
        self.project_full_path = ""
        self.switch_btn.props.sensitive = False
        self.project_name_ready = False
        self.project_id_ready = False
        self.ext_name_ready = False
        self.ext_uuid_ready = False
        self.ext_description_ready = False
        self.project_name = ""
        self.project_id = ""
        self.ext_name = ""
        self.ext_uuid = ""
        self.ext_description = ""
        self.is_git = True
        self.language = self.lang_btn.get_label()
        self.template = self.template_btn.get_label()
        self.license = self.license_combo_box.get_active_text()

        self.gui = ['GTK GUI Application']
        self.cli = ['GTK CLI Application', 'GNOME Extension']

    @Gtk.Template.Callback()
    def on_switch_btn_clicked(self, w):
        self.main_path = self.path_entry.props.text
        if self.main_path[:-1] == '/':
            self.main_path = self.main_path[:-1]
        if self.main_path[0] == '~':
            self.main_path = GLib.get_home_dir() + self.main_path[1:] + '/'
        else:
            self.main_path = self.main_path + '/'
        if not os.path.exists(self.main_path):
            os.makedirs(self.main_path)

        is_gui = self.check_gui(self.template)
        self.project_full_path = self.main_path + self.project_name + '/'

        # Create template class on main button click and call start() function

        if self.language == 'Python':
            from .python_template import PythonTemplate
            self.complete_template = PythonTemplate(is_gui, self.project_id, self.project_name,
                                                    self.project_full_path, self.is_git, self.license)
        elif self.language == 'Rust':
            from .rust_template import RustTemplate
            self.complete_template = RustTemplate(is_gui, self.project_id, self.project_name,
                                                  self.project_full_path, self.is_git, self.license)
        elif self.language == 'C':
            from .c_template import CTemplate
            self.complete_template = CTemplate(is_gui, self.project_id, self.project_name,
                                               self.project_full_path, self.is_git, self.license)
        elif self.language == 'JS':
            if self.template == 'GNOME Extension':
                from .gnome_extension_template import GnomeExtensionTemplate
                self.complete_template = GnomeExtensionTemplate(self.ext_name, self.ext_uuid, self.ext_description,
                                                                self.is_git)
                self.project_full_path = GLib.get_home_dir() + '/.local/share/gnome-shell/extensions/' + self.ext_uuid
            else:
                from .js_template import JsTemplate
                self.complete_template = JsTemplate(is_gui, self.project_id, self.project_name,
                                                    self.project_full_path, self.is_git, self.license)

        if path.exists(self.project_full_path):
            self.path_exists_revealer.props.reveal_child = True
            return
        else:
            if self.path_exists_revealer.props.reveal_child:
                self.path_exists_revealer.props.reveal_child = False

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
    def on_gnome_ext_entry_changed(self, e):
        if self.check_entry(e, self.check_ext_name):
            self.ext_name = e.props.text
            self.ext_name_ready = True
            self.ext_ready_check()

    @Gtk.Template.Callback()
    def on_gnome_ext_uuid_entry_changed(self, e):
        if self.check_entry(e, self.check_ext_uuid):
            self.ext_uuid = e.props.text
            self.ext_uuid_ready = True
            self.ext_ready_check()

    @Gtk.Template.Callback()
    def on_gnome_ext_description_entry_changed(self, e):
        self.ext_description = e.get_text()
        self.ext_description_ready = True if self.ext_description else False

    @Gtk.Template.Callback()
    def on_git_enable_btn_toggled(self, b):
        if not b.props.active:
            self.is_git = False

    @Gtk.Template.Callback()
    def on_close_path_exists_btn_clicked(self, b):
        self.path_exists_revealer.props.reveal_child = False

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
    def on_gnome_extension_btn_toggled(self, b):
        self.button_toggled(b, 'template')

    @Gtk.Template.Callback()
    def on_license_combo_box_changed(self, cb):
        self.license = cb.get_active_text()

    @Gtk.Template.Callback()
    def on_about_btn_clicked(self, b):
        about = AboutWindow(self)
        about.set_logo_icon_name('com.github.Latesil.project-starter')
        about.run()
        about.destroy()

    @Gtk.Template.Callback()
    def on_keyboard_shortcuts_btn_clicked(self, b):
        k_s = KeyboardShortcutsWindow()
        k_s.show()

    ##########################################################################

    def button_toggled(self, b, category):
        if category == 'lang':
            self.lang_btn.set_label(b.get_label())
            self.language = self.lang_btn.get_label()
            self.cli_gtk_btn.props.visible = False if self.language == 'Python' or self.language == 'JS' else True
            self.gnome_extension_btn.props.visible = True if self.language == 'JS' else False

            if self.lang_btn.get_label() != 'JS' and self.template_btn.get_label() == 'GNOME Extension':
                self.template_btn.set_label('GTK GUI Application')
                self.template = self.template_btn.get_label()
                self.gui_gtk_btn.props.active = True
                self.gnome_ext_revealer.props.reveal_child = False

            if self.lang_btn.get_label() != 'JS' and self.template_btn.get_label() == 'GTK CLI Application':
                self.template_btn.set_label('GTK GUI Application')
                self.template = self.template_btn.get_label()

            if self.lang_btn.get_label() != 'Python' and self.template_btn.get_label() == 'GTK CLI Application':
                self.template_btn.set_label('GTK GUI Application')
                self.template = self.template_btn.get_label()

            self.lang_revealer.props.reveal_child = False
        elif category == 'template':
            self.template_btn.set_label(b.get_label())
            self.template = self.template_btn.get_label()
            self.template_revealer.props.reveal_child = False
            if self.template == 'GNOME Extension':
                self.gnome_ext_revealer.props.reveal_child = True
                self.license_revealer.props.reveal_child = False
                self.project_name_entry.props.sensitive = False
                self.project_id_entry.props.sensitive = False
                self.path_entry.props.sensitive = False
                self.change_path_btn.props.sensitive = False
            else:
                self.gnome_ext_revealer.props.reveal_child = False
                self.license_revealer.props.reveal_child = True
                self.project_name_entry.props.sensitive = True
                self.project_id_entry.props.sensitive = True
                self.path_entry.props.sensitive = True
                self.change_path_btn.props.sensitive = True
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
            return False if text[0].isdigit() or re.search('\s', text) or re.search('\.', text) or not text.islower() else True

    def check_project_id(self, text):
        if text:
            return True if re.match('[a-zA-Z]+\.[a-zA-Z]+', text) else False

    def check_ext_name(self, text):
        if text:
            return False if text[0].isdigit() or re.search('\s', text) else True

    def check_ext_uuid(self, text):
        if text:
            return True if re.match('[a-zA-Z]+\@[a-zA-Z]+\.[a-zA-Z]+', text) else False

    def ready_check(self):
        self.switch_btn.props.sensitive = True if self.project_name_ready and self.project_id_ready else False

    def ext_ready_check(self):
        self.switch_btn.props.sensitive = True if self.ext_name_ready and self.ext_uuid_ready and self.ext_description_ready else False

    def check_gui(self, t):
        return t in self.gui

    ##########################

    def python_set(self, *args):
        self.language = 'Python'
        self.lang_btn.set_label('Python')
        self.python_btn.props.active = True
        self.gnome_extension_btn.props.visible = False
        self.cli_gtk_btn.props.visible = False

        if self.template_btn.get_label() == 'GTK CLI Application' or self.template_btn.get_label() == 'GNOME Extension':
            self.gnome_ext_revealer.props.reveal_child = False
            self.license_revealer.props.reveal_child = True
            self.project_name_entry.props.sensitive = True
            self.project_id_entry.props.sensitive = True
            self.path_entry.props.sensitive = True
            self.change_path_btn.props.sensitive = True
            self.gui_gtk_btn.props.active = True
            self.python_btn.props.active = True
            self.template_btn.set_label('GTK GUI Application')

        if self.template_revealer.props.reveal_child:
            self.template_revealer.props.reveal_child = False

        if self.gnome_ext_revealer.props.reveal_child:
            self.gnome_ext_revealer.props.reveal_child = False

        if self.lang_revealer.props.reveal_child:
            self.lang_revealer.props.reveal_child = False

    def c_set(self, *args):
        self.language = 'C'
        self.lang_btn.set_label('C')
        self.c_btn.props.active = True
        self.gnome_extension_btn.props.visible = False
        self.gnome_ext_revealer.props.reveal_child = False
        self.license_revealer.props.reveal_child = True
        self.project_name_entry.props.sensitive = True
        self.project_id_entry.props.sensitive = True
        self.path_entry.props.sensitive = True
        self.change_path_btn.props.sensitive = True
        self.cli_gtk_btn.props.visible = True

        if self.template_btn.get_label() == 'GNOME Extension':
            self.gui_gtk_btn.props.active = True
            self.c_btn.props.active = True
            self.template_btn.set_label('GTK GUI Application')

        if self.template_revealer.props.reveal_child:
            self.template_revealer.props.reveal_child = False

        if self.gnome_ext_revealer.props.reveal_child:
            self.gnome_ext_revealer.props.reveal_child = False

        if self.lang_revealer.props.reveal_child:
            self.lang_revealer.props.reveal_child = False

    def js_set(self, *args):
        self.language = 'JS'
        self.lang_btn.set_label('JS')
        self.js_btn.props.active = True
        self.gnome_extension_btn.props.visible = True
        self.cli_gtk_btn.props.visible = False

        if self.template_btn.get_label() == 'GTK CLI Application':
            self.cli_gtk_btn.props.visible = False
            self.gui_gtk_btn.props.active = True
            self.js_btn.props.active = True
            self.template_btn.set_label('GTK GUI Application')

        if self.template_revealer.props.reveal_child:
            self.gnome_ext_revealer.props.reveal_child = False
            self.license_revealer.props.reveal_child = True
            self.project_name_entry.props.sensitive = True
            self.project_id_entry.props.sensitive = True
            self.path_entry.props.sensitive = True
            self.change_path_btn.props.sensitive = True

        if self.template_btn.get_label() == 'GNOME Extension':
            self.gnome_ext_revealer.props.reveal_child = True

        if self.lang_revealer.props.reveal_child:
            self.lang_revealer.props.reveal_child = False

    def rust_set(self, *args):
        self.language = 'Rust'
        self.lang_btn.set_label('Rust')
        self.rust_btn.props.active = True
        self.gnome_ext_revealer.props.reveal_child = False
        self.license_revealer.props.reveal_child = True
        self.project_name_entry.props.sensitive = True
        self.project_id_entry.props.sensitive = True
        self.path_entry.props.sensitive = True
        self.change_path_btn.props.sensitive = True
        self.cli_gtk_btn.props.visible = True

        if self.template_btn.get_label() == 'GNOME Extension':
            self.gui_gtk_btn.props.active = True
            self.rust_btn.props.active = True
            self.template_btn.set_label('GTK GUI Application')

        if self.template_revealer.props.reveal_child:
            self.template_revealer.props.reveal_child = False

        if self.gnome_ext_revealer.props.reveal_child:
            self.gnome_ext_revealer.props.reveal_child = False

        if self.lang_revealer.props.reveal_child:
            self.lang_revealer.props.reveal_child = False

    def gui_set(self, *args):
        if self.template_btn.get_label() == 'GTK CLI Application' or self.template_btn.get_label() == 'GNOME Extension':
            self.gnome_ext_revealer.props.reveal_child = False
            if self.language == 'JS':
                self.gnome_extension_btn.props.visible = True
            self.license_revealer.props.reveal_child = True
            self.project_name_entry.props.sensitive = True
            self.project_id_entry.props.sensitive = True
            self.path_entry.props.sensitive = True
            self.change_path_btn.props.sensitive = True
        self.gui_gtk_btn.props.active = True
        self.template_btn.set_label('GTK GUI Application')

    def cli_set(self, *args):
        not_cli = ['Python', 'JS']
        if self.language in not_cli:
            return
        else:
            if self.template_btn.get_label() == 'GTK GUI Application' or self.template_btn.get_label() == 'GNOME Extension':
                self.gnome_extension_btn.props.visible = False
                self.cli_gtk_btn.props.active = True
                self.template_btn.set_label('GTK CLI Application')

    def extension_set(self, *args):
        if self.language != "JS":
            self.language = 'JS'
            self.js_btn.props.active = True
            self.lang_btn.set_label('JS')
        self.template_btn.set_label('GNOME Extension')
        self.gnome_extension_btn.props.active = True
        self.gnome_ext_revealer.props.reveal_child = True
        self.license_revealer.props.reveal_child = False
        self.project_name_entry.props.sensitive = False
        self.project_id_entry.props.sensitive = False
        self.path_entry.props.sensitive = False
        self.change_path_btn.props.sensitive = False
        self.cli_gtk_btn.props.visible = False
