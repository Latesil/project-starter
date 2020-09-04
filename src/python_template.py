# python_template.py
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

import sys
import os
import stat
from gi.repository import GLib
from .project_starter_constants import constants
from .common_files import File
from .template import Template
from .helpers import *

class PythonTemplate(Template):

    def __init__(self, is_gui, project_id, project_name, path, is_git, license):
        self.is_gui = is_gui
        self.project_id = project_id
        self.project_name = project_name
        self.path = path
        self.is_git = is_git
        self.lang = 'python'
        self.license = license
        self.file = File()
        self.gpl_text = self.file.get_gpl()

        ########################################################################

        self.project_full_name = self.project_id + '.' + self.project_name
        self.project_path = self.project_id.replace('.', '/')
        self.project_id_reverse = self.project_path + '/' + self.project_name + '/'
        self.class_name = "".join(w.capitalize() for w in self.project_name.split('-'))
        self.project_name_underscore = self.project_name.replace('-', '_')

        ########################################################################

    def start(self):
        if self.is_gui:
            self.create_basic_gui_structure(self.project_id, self.project_name, self.path)
            self.populate_data_folder(self.project_id, self.project_name)
            self.populate_po_dir(self.project_id, self.project_name)
            self.populate_src_dir(self.project_id, self.project_name)
            if self.is_git:
                os.chdir(self.path)
                os.system('git init')

    def create_basic_gui_structure(self, project_id, project_name, path):

        os.makedirs(path + '/build-aux/meson')
        os.makedirs(path + '/data')
        os.makedirs(path + '/po')
        os.makedirs(path + '/src')

        path = self.path + '/'

        self.file.create_copying_file(path, self.license)
        self.file.create_manifest_file(path, self.project_full_name, self.project_name, self.project_name, self.lang)
        self.file.create_meson_postinstall_file(path)

        text = (f"project('{self.project_name}',\n",
                f"          version: '0.1.0',\n",
                f"    meson_version: '>= {constants['MESON_VERSION']}',\n",
                f"  default_options: [ 'warning_level=2',\n",
                f"                   ],\n",
                f")\n",
                f"\n",
                f"i18n = import('i18n')\n",
                f"\n",
                f"\n",
                f"subdir('data')\n",
                f"subdir('src')\n",
                f"subdir('po')",
                f"\n",
                f"meson.add_install_script('build-aux/meson/postinstall.py')\n",)

        create_file(path, 'meson.build', text)

    def populate_data_folder(self, project_id, project_name):
        path = self.path + '/data/'
        self.file.create_data_meson_file(path, self.project_full_name)
        self.file.create_appdata_file(path, self.project_full_name, self.license)
        self.file.create_desktop_file(path, self.project_full_name, self.project_name, self.project_id)
        self.file.create_gschema_file(path, self.project_full_name, self.project_name, self.project_path)

    def populate_po_dir(self, project_id, project_name):
        files = ['window.ui', 'main.py', 'window.py']
        path = self.path + '/po/'
        self.file.create_po_linguas_file(path)
        self.file.create_po_meson_file(path, self.project_name)
        self.file.create_po_potfiles_file(path, self.project_id, files)

    def populate_src_dir(self, project_id, project_name):
        text = ()

        create_file(path + '/src/', '__init__.py', text, empty=True)

        text_main = (f"# main.py\n"
                f"#\n",
                f"# Copyright 2020\n",
                f"#\n",
                f"{self.gpl_text}",
                f"\n",
                f"import sys\n",
                f"import gi\n",
                f"\n",
                f"gi.require_version('Gtk', '3.0')\n",
                f"\n",
                f"from gi.repository import Gtk, Gio\n",
                f"\n",
                f"from .window import {self.class_name}Window\n"",
                f"\n",
                f"\n",
                f"class Application(Gtk.Application):\n",
                f"    def __init__(self):\n",
                f"        super().__init__(application_id='{self.project_id}',\n"",
                f"                         flags=Gio.ApplicationFlags.FLAGS_NONE)\n",
                f"\n",
                f"    def do_activate(self):\n",
                f"        win = self.props.active_window\n",
                f"        if not win:\n",
                f"            win = {self.class_name}Window(application=self)\n",
                f"        win.present()\n",
                f"\n",
                f"\n",
                f"def main(version):\n",
                f"    app = Application()\n",
                f"    return app.run(sys.argv)\n",
                f"\n",)

        create_file(path + '/src/', 'main.py', text_main)

        text_meson = (f"pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())\n",
                f"moduledir = join_paths(pkgdatadir, '{self.project_name_underscore}')\n",
                f"gnome = import('gnome')\n",
                f"\n",
                f"gnome.compile_resources('{self.project_name}',\n",
                f"  '{self.project_name_underscore}.gresource.xml',\n",
                f"  gresource_bundle: true,\n",
                f"  install: true,\n",
                f"  install_dir: pkgdatadir,\n",
                f")\n",
                f"\n",
                f"desktop_utils = find_program('desktop-file-validate', required: false)\n",
                f"if desktop_utils.found()\n",
                f"  test('Validate desktop file', desktop_utils,\n",
                f"    args: [desktop_file]\n",
                f"  )\n",
                f"endif\n",
                f"\n",
                f"python = import('python')\n",
                f"\n",
                f"conf = configuration_data()\n",
                f"conf.set('PYTHON', python.find_installation('python3').path())\n",
                f"conf.set('VERSION', meson.project_version())\n",
                f"conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))\n",
                f"conf.set('pkgdatadir', pkgdatadir)\n",
                f"\n",
                f"configure_file(\n",
                f"  input: '{self.project_name}.in',\n",
                f"  output: '{self.project_name}',\n",
                f"  configuration: conf,\n",
                f"  install: true,\n",
                f"  install_dir: get_option('bindir')\n",
                f")\n",
                f"\n",
                f"{self.project_name_underscore}_sources = [\n",
                f"  '__init__.py',\n",
                f"  'main.py',\n",
                f"  'window.py',\n",
                f"]\n",
                f"\n",
                f"install_data(%{self.project_name_underscore}_sources, install_dir: moduledir)\n",
                f"\n",)

        create_file(path + '/src/', 'meson.build', text_meson)

        text_id_in = (f"#!@PYTHON@\n"",
                f"#\n",
                f"# {self.project_name}.in\n",
                f"#\n",
                f"# Copyright 2020\n",
                f"#\n",
                f"{self.gpl_text}",
                f"import os\n",
                f"import sys\n",
                f"import signal\n",
                f"import gettext\n",
                f"\n",
                f"VERSION = '@VERSION@'\n",
                f"pkgdatadir = '@pkgdatadir@'\n",
                f"localedir = '@localedir@'\n",
                f"\n",
                f"sys.path.insert(1, pkgdatadir)\n",
                f"signal.signal(signal.SIGINT, signal.SIG_DFL)\n",
                f"gettext.install('{self.project_name}', localedir)\n",
                f"\n",
                f"if __name__ == '__main__':\n",
                f"    import gi\n",
                f"\n",
                f"    from gi.repository import Gio\n",
                f"    resource = Gio.Resource.load(os.path.join(pkgdatadir, '{self.project_name}.gresource'))\n",
                f"    resource._register()\n"",
                f"\n",
                f"    from {self.project_name_underscore} import main\n",
                f"    sys.exit(main.main(VERSION))\n",)

        create_file(path + '/src/', self.project_name + '.in', text_id_in)
        make_executable(path + '/src/', self.project_name + '.in')

        files = ['window.ui']
        self.file.create_gresource_file(self.path, self.project_name_underscore, self.project_id_reverse, files)

        text_window = (f"# window.py\n",
                f"#\n",
                f"# Copyright 2020\n",
                f"#\n",
                f"{self.gpl_text}",
                f"\n",
                f"from gi.repository import Gtk\n",
                f"\n",
                f"\n",
                f"@Gtk.Template(resource_path='/{self.project_id_reverse}window.ui')\n",
                f"class {self.class_name}Window(Gtk.ApplicationWindow):\n",
                f"    __gtype_name__ = '{self.class_name}Window'\n",
                f"\n",
                f"    label = Gtk.Template.Child()\n",
                f"\n",
                f"    def __init__(self, **kwargs):\n",
                f"        super().__init__(**kwargs)\n",
                f"\n",)

        create_file(path + '/src/', 'window.py', text_window)

        self.file.create_window_ui_file(self.path, self.class_name)
    
