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

import os
import datetime
from .project_starter_constants import constants
from .file import File
from .template import Template


class PythonTemplate(Template):

    """
    Python Template Class
    """

    def __init__(self, is_gui, project_id, project_name, path, is_git, license):
        self.is_gui = is_gui
        self.project_id = project_id
        self.project_name = project_name
        self.root = path
        self.is_git = is_git
        self.project_license = license
        self.files = []
        self.lang = 'python'
        self.po_files = ['window.ui', 'main.py', 'window.py']
        self.gresource_files = ['window.ui']
        now = datetime.datetime.now()
        self.year = now.year

        ########################################################################

        self.window_name = "".join(w.capitalize() for w in self.project_name.split('-'))

        self.data = vars(self)

        ########################################################################

    def start(self):
        if self.is_gui:
            self.create_folders(self.root)
            self.populate_root_dir(self.data)
            self.populate_data_dir(self.data)
            self.populate_po_dir(self.data)
            self.populate_src_dir(self.data)
            
            if self.is_git:
                os.chdir(self.root)
                os.system('git init')

            for f in self.files:
                f.create()
                if f.filename == self.project_name + '.in':
                    f.make_executable()

    def populate_root_dir(self, data):
        path = self.root + 'build-aux/meson/'

        copying_file = self.create_copying_file(self.root, data)
        self.files.append(copying_file)

        manifest_file = self.create_manifest_file(self.root, data)
        self.files.append(manifest_file)

        post_install_file = self.create_meson_postinstall_file(path)
        self.files.append(post_install_file)

        text = (f"project('{data['project_name']}',\n",
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
                f"subdir('po')\n",
                f"\n",
                f"meson.add_install_script('build-aux/meson/postinstall.py')\n",)

        main_meson_file = File(self.root, 'meson.build', text)
        self.files.append(main_meson_file)

    def populate_data_dir(self, data):
        path = self.root + 'data/'

        meson_data_file = self.create_data_meson_file(path, data)
        self.files.append(meson_data_file)

        appdata_file = self.create_appdata_file(path, data)
        self.files.append(appdata_file)

        desktop_file = self.create_desktop_file(path, data)
        self.files.append(desktop_file)

        gschema_file = self.create_gschema_file(path, data)
        self.files.append(gschema_file)

    def populate_po_dir(self, data):
        path = self.root + 'po/'

        linguas_file = self.create_po_linguas_file(path)
        self.files.append(linguas_file)

        po_meson_file = self.create_po_meson_file(path, data)
        self.files.append(po_meson_file)

        potfiles_file = self.create_po_potfiles_file(path, data)
        self.files.append(potfiles_file)

    def populate_src_dir(self, data):
        path = self.root + 'src/'

        text = ()
        init_src_file = File(path, '__init__.py', text)
        self.files.append(init_src_file)

        text_main = (f"# main.py\n"
                     f"#\n",
                     f"# Copyright {self.year}\n",
                     f"#\n",
                     f"{self.get_gpl(self.lang)}",
                     f"\n",
                     f"import sys\n",
                     f"import gi\n",
                     f"\n",
                     f"gi.require_version('Gtk', '3.0')\n",
                     f"\n",
                     f"from gi.repository import Gtk, Gio\n",
                     f"\n",
                     f"from .window import {data['window_name']}Window\n",
                     f"\n",
                     f"\n",
                     f"class Application(Gtk.Application):\n",
                     f"    def __init__(self):\n",
                     f"        super().__init__(application_id='{data['project_id']}',\n",
                     f"                         flags=Gio.ApplicationFlags.FLAGS_NONE)\n",
                     f"\n",
                     f"    def do_activate(self):\n",
                     f"        win = self.props.active_window\n",
                     f"        if not win:\n",
                     f"            win = {data['window_name']}Window(application=self)\n",
                     f"        win.present()\n",
                     f"\n",
                     f"\n",
                     f"def main(version):\n",
                     f"    app = Application()\n",
                     f"    return app.run(sys.argv)\n",
                     f"\n",)
        main_src_file = File(path, 'main.py', text_main)
        self.files.append(main_src_file)

        text_meson = (f"pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())\n",
                      f"moduledir = join_paths(pkgdatadir, '{data['project_name'].replace('-', '_')}')\n",
                      f"gnome = import('gnome')\n",
                      f"\n",
                      f"gnome.compile_resources('{data['project_name']}',\n",
                      f"  '{data['project_name'].replace('-', '_')}.gresource.xml',\n",
                      f"  gresource_bundle: true,\n",
                      f"  install: true,\n",
                      f"  install_dir: pkgdatadir,\n",
                      f")\n",
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
                      f"  input: '{data['project_name']}.in',\n",
                      f"  output: '{data['project_name']}',\n",
                      f"  configuration: conf,\n",
                      f"  install: true,\n",
                      f"  install_dir: get_option('bindir')\n",
                      f")\n",
                      f"\n",
                      f"{data['project_name'].replace('-', '_')}_sources = [\n",
                      f"  '__init__.py',\n",
                      f"  'main.py',\n",
                      f"  'window.py',\n",
                      f"]\n",
                      f"\n",
                      f"install_data({data['project_name'].replace('-', '_')}_sources, install_dir: moduledir)\n",
                      f"\n",)
        meson_src_file = File(path, 'meson.build', text_meson)
        self.files.append(meson_src_file)

        text_id_in = (f"#!@PYTHON@\n",
                      f"#\n",
                      f"# {data['project_name']}.in\n",
                      f"#\n",
                      f"# Copyright {self.year}\n",
                      f"#\n",
                      f"{self.get_gpl(self.lang)}",
                      f"\n",
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
                      f"gettext.install('{data['project_name']}', localedir)\n",
                      f"\n",
                      f"if __name__ == '__main__':\n",
                      f"    import gi\n",
                      f"\n",
                      f"    from gi.repository import Gio\n",
                      f"    resource = Gio.Resource.load(os.path.join(pkgdatadir, '{data['project_name']}.gresource'))\n",
                      f"    resource._register()\n",
                      f"\n",
                      f"    from {data['project_name'].replace('-', '_')} import main\n",
                      f"    sys.exit(main.main(VERSION))\n",)
        in_src_file = File(path, self.project_name + '.in', text_id_in)
        self.files.append(in_src_file)

        gresource_file = self.create_gresource_file(path, data)
        self.files.append(gresource_file)

        text_window = (f"# window.py\n",
                       f"#\n",
                       f"# Copyright {self.year}\n",
                       f"#\n",
                       f"{self.get_gpl(self.lang)}",
                       f"\n",
                       f"from gi.repository import Gtk\n",
                       f"\n",
                       f"\n",
                       f"@Gtk.Template(resource_path='/{data['project_id'].replace('.', '/')}/window.ui')\n",
                       f"class {data['window_name']}Window(Gtk.ApplicationWindow):\n",
                       f"    __gtype_name__ = '{data['window_name']}Window'\n",
                       f"\n",
                       f"    label = Gtk.Template.Child()\n",
                       f"\n",
                       f"    def __init__(self, **kwargs):\n",
                       f"        super().__init__(**kwargs)\n",
                       f"\n",)
        window_file = File(path, 'window.py', text_window)
        self.files.append(window_file)

        window_ui_file = self.create_window_ui_file(path, data)
        self.files.append(window_ui_file)
