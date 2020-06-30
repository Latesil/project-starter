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

from gi.repository import Gtk


@Gtk.Template(resource_path='/org/github/Latesil/project-starter/window.ui')
class ProjectStarterWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ProjectStarterWindow'

    switch_btn = Gtk.Template.Child()
    second_btn = Gtk.Template.Child()
    main_view = Gtk.Template.Child()
    choose_app_btn = Gtk.Template.Child()
    lang_btn = Gtk.Template.Child()
    template_btn = Gtk.Template.Child()
    lang_btn_box = Gtk.Template.Child()
    template_btn_box = Gtk.Template.Child()
    lang_revealer = Gtk.Template.Child()
    template_revealer = Gtk.Template.Child()
    project_name_entry = Gtk.Template.Child()
    project_name_revealer = Gtk.Template.Child()
    project_id_entry = Gtk.Template.Child()
    project_id_revealer = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """@Gtk.Template.Callback()
    def on_switch_btn_map(self, w):
        pass #page0 page1

    @Gtk.Template.Callback()
    def on_second_btn_map(self, w):
        pass"""

    @Gtk.Template.Callback()
    def on_switch_btn_clicked(self, w):
        self.main_view.set_visible_child_name('page1')

    @Gtk.Template.Callback()
    def on_second_btn_clicked(self, w):
        self.close() #self.main_view.set_visible_child_name('page0')

    @Gtk.Template.Callback()
    def on_change_path_btn_clicked(self, btn):
        pass

    @Gtk.Template.Callback()
    def on_choose_app_btn_changed(self, w):
        app = self.choose_app_btn.get_app_info()
        app.refresh()

    @Gtk.Template.Callback()
    def on_lang_btn_clicked(self, btn):
        if self.template_revealer.get_reveal_child():
            self.template_revealer.set_reveal_child(False)

        if self.lang_revealer.get_reveal_child():
            self.lang_revealer.set_reveal_child(False)
        else:
            self.lang_revealer.set_reveal_child(True)

    @Gtk.Template.Callback()
    def on_template_btn_clicked(self, btn):
        if self.lang_revealer.get_reveal_child():
            self.lang_revealer.set_reveal_child(False)

        if self.template_revealer.get_reveal_child():
            self.template_revealer.set_reveal_child(False)
        else:
            self.template_revealer.set_reveal_child(True)

    @Gtk.Template.Callback()
    def on_project_name_entry_focus_in_event(self, e, w):
        self.project_name_revealer.set_reveal_child(True)

    @Gtk.Template.Callback()
    def on_project_name_entry_focus_out_event(self, e, w):
        self.project_name_revealer.set_reveal_child(False)

    @Gtk.Template.Callback()
    def on_project_id_entry_focus_in_event(self, e, w):
        self.project_id_revealer.set_reveal_child(True)

    @Gtk.Template.Callback()
    def on_project_id_entry_focus_out_event(self, e, w):
        self.project_id_revealer.set_reveal_child(False)
        
