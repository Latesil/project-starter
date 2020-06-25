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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @Gtk.Template.Callback()
    def on_switch_btn_map(self, w):
        print(dir(self.main_view)) #page0 page1

    @Gtk.Template.Callback()
    def on_second_btn_map(self, w):
        pass #print('second_btn_map')

    @Gtk.Template.Callback()
    def on_switch_btn_clicked(self, w):
        self.main_view.set_visible_child_name('page1')

    @Gtk.Template.Callback()
    def on_second_btn_clicked(self, w):
        self.main_view.set_visible_child_name('page0')
        
