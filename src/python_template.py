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

        self.file.create_copying_file(path, self.license)
        self.file.create_manifest_file(path, self.project_full_name, self.project_name, self.lang)
        self.file.create_meson_postinstall_file(path)

        with open(path + '/' + "meson.build", 'a') as file_meson_build:
            file_meson_build.write("project('%s',\n" % self.project_name)
            file_meson_build.write("          version: '0.1.0',\n")
            file_meson_build.write("    meson_version: '>= %s',\n" % constants['MESON_VERSION'])
            file_meson_build.write("  default_options: [ 'warning_level=2',\n")
            file_meson_build.write("                   ],\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("i18n = import('i18n')\n")
            file_meson_build.write("\n")
            file_meson_build.write("\n")
            file_meson_build.write("subdir('data')\n")
            file_meson_build.write("subdir('src')\n")
            file_meson_build.write("subdir('po')\n")
            file_meson_build.write("\n")
            file_meson_build.write("meson.add_install_script('build-aux/meson/postinstall.py')\n")

    def populate_data_folder(self, project_id, project_name):
        path = self.path + '/data/'
        self.file.create_data_meson_file(path, self.project_full_name)
        self.file.create_appdata_file(path, self.project_full_name, self.license)
        self.file.create_desktop_file(path, self.project_full_name, self.project_name, self.project_id)
        self.file.create_gschema_file(path, self.project_full_name, self.project_name, self.project_path)

    def populate_po_dir(self, project_id, project_name):
        files = ['window.ui', 'main.py', 'window.py']
        self.file.create_po_linguas_file(self.path)
        self.file.create_po_meson_file(self.path, self.project_name)
        self.file.create_po_potfiles_file(self.path, self.project_id, files)

    def populate_src_dir(self, project_id, project_name):
        #TODO maybe there is another way to create an empty file?
        with open(self.path + '/src/__init__.py', 'a') as file_py_init:
            file_py_init.close()

        with open(self.path + '/src/main.py', 'a') as file_py_main:
            file_py_main.write("# main.py\n")
            file_py_main.write("#\n")
            file_py_main.write("# Copyright 2020\n")
            file_py_main.write("#\n")
            file_py_main.write(self.gpl_text)
            file_py_main.write("\n")
            file_py_main.write("import sys\n")
            file_py_main.write("import gi\n")
            file_py_main.write("\n")
            file_py_main.write("gi.require_version('Gtk', '3.0')\n")
            file_py_main.write("\n")
            file_py_main.write("from gi.repository import Gtk, Gio\n")
            file_py_main.write("\n")
            file_py_main.write("from .window import %sWindow\n" % self.class_name)
            file_py_main.write("\n")
            file_py_main.write("\n")
            file_py_main.write("class Application(Gtk.Application):\n")
            file_py_main.write("    def __init__(self):\n")
            file_py_main.write("        super().__init__(application_id='%s',\n" % self.project_id)
            file_py_main.write("                         flags=Gio.ApplicationFlags.FLAGS_NONE)\n")
            file_py_main.write("\n")
            file_py_main.write("    def do_activate(self):\n")
            file_py_main.write("        win = self.props.active_window\n")
            file_py_main.write("        if not win:\n")
            file_py_main.write("            win = %sWindow(application=self)\n" % self.class_name)
            file_py_main.write("        win.present()\n")
            file_py_main.write("\n")
            file_py_main.write("\n")
            file_py_main.write("def main(version):\n")
            file_py_main.write("    app = Application()\n")
            file_py_main.write("    return app.run(sys.argv)\n")
            file_py_main.write("\n")

        with open(self.path + '/src/meson.build', 'a') as file_meson_build:
            file_meson_build.write("pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())\n")
            file_meson_build.write("moduledir = join_paths(pkgdatadir, '%s')\n" % self.project_name_underscore)
            file_meson_build.write("gnome = import('gnome')\n")
            file_meson_build.write("\n")
            file_meson_build.write("gnome.compile_resources('%s',\n" % self.project_name)
            file_meson_build.write("  '%s.gresource.xml',\n" % self.project_name_underscore)
            file_meson_build.write("  gresource_bundle: true,\n")
            file_meson_build.write("  install: true,\n")
            file_meson_build.write("  install_dir: pkgdatadir,\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("desktop_utils = find_program('desktop-file-validate', required: false)\n")
            file_meson_build.write("if desktop_utils.found()\n")
            file_meson_build.write("  test('Validate desktop file', desktop_utils,\n")
            file_meson_build.write("    args: [desktop_file]\n")
            file_meson_build.write("  )\n")
            file_meson_build.write("endif\n")
            file_meson_build.write("\n")
            file_meson_build.write("python = import('python')\n")
            file_meson_build.write("\n")
            file_meson_build.write("conf = configuration_data()\n")
            file_meson_build.write("conf.set('PYTHON', python.find_installation('python3').path())\n")
            file_meson_build.write("conf.set('VERSION', meson.project_version())\n")
            file_meson_build.write("conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))\n")
            file_meson_build.write("conf.set('pkgdatadir', pkgdatadir)\n")
            file_meson_build.write("\n")
            file_meson_build.write("configure_file(\n")
            file_meson_build.write("  input: '%s.in',\n" % self.project_name)
            file_meson_build.write("  output: '%s',\n" % self.project_name)
            file_meson_build.write("  configuration: conf,\n")
            file_meson_build.write("  install: true,\n")
            file_meson_build.write("  install_dir: get_option('bindir')\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("%s_sources = [\n" % self.project_name_underscore)
            file_meson_build.write("  '__init__.py',\n")
            file_meson_build.write("  'main.py',\n")
            file_meson_build.write("  'window.py',\n")
            file_meson_build.write("]\n")
            file_meson_build.write("\n")
            file_meson_build.write("install_data(%s_sources, install_dir: moduledir)\n" % self.project_name_underscore)
            file_meson_build.write("\n")

        with open(self.path + '/src/' + self.project_name + '.in', 'a') as file_exec:
            file_exec.write("#!@PYTHON@\n")
            file_exec.write("#\n")
            file_exec.write("# %s.in\n" % self.project_name)
            file_exec.write("#\n")
            file_exec.write("# Copyright 2020\n")
            file_exec.write("#\n")
            file_exec.write(self.gpl_text)
            file_exec.write("\n")
            file_exec.write("import os\n")
            file_exec.write("import sys\n")
            file_exec.write("import signal\n")
            file_exec.write("import gettext\n")
            file_exec.write("\n")
            file_exec.write("VERSION = '@VERSION@'\n")
            file_exec.write("pkgdatadir = '@pkgdatadir@'\n")
            file_exec.write("localedir = '@localedir@'\n")
            file_exec.write("\n")
            file_exec.write("sys.path.insert(1, pkgdatadir)\n")
            file_exec.write("signal.signal(signal.SIGINT, signal.SIG_DFL)\n")
            file_exec.write("gettext.install('%s', localedir)\n" % self.project_name)
            file_exec.write("\n")
            file_exec.write("if __name__ == '__main__':\n")
            file_exec.write("    import gi\n")
            file_exec.write("\n")
            file_exec.write("    from gi.repository import Gio\n")
            file_exec.write("    resource = Gio.Resource.load(os.path.join(pkgdatadir, '%s.gresource'))\n" % self.project_name)
            file_exec.write("    resource._register()\n")
            file_exec.write("\n")
            file_exec.write("    from %s import main\n" % self.project_name_underscore)
            file_exec.write("    sys.exit(main.main(VERSION))\n")

        st = os.stat(self.path + '/src/' + self.project_name + '.in')
        os.chmod(self.path + '/src/' + self.project_name + '.in', st.st_mode | stat.S_IEXEC)

        files = ['window.ui']
        self.file.create_gresource_file(self.path, self.project_name_underscore, self.project_id_reverse, files)

        with open(self.path + '/src/window.py', 'a') as file_py_window:
            file_py_window.write("# window.py\n")
            file_py_window.write("#\n")
            file_py_window.write("# Copyright 2020\n")
            file_py_window.write("#\n")
            file_py_window.write(self.gpl_text)
            file_py_window.write("\n")
            file_py_window.write("from gi.repository import Gtk\n")
            file_py_window.write("\n")
            file_py_window.write("\n")
            file_py_window.write("@Gtk.Template(resource_path='/%swindow.ui')\n" % self.project_id_reverse)
            file_py_window.write("class %sWindow(Gtk.ApplicationWindow):\n" % self.class_name)
            file_py_window.write("    __gtype_name__ = '%sWindow'\n" % self.class_name)
            file_py_window.write("\n")
            file_py_window.write("    label = Gtk.Template.Child()\n")
            file_py_window.write("\n")
            file_py_window.write("    def __init__(self, **kwargs):\n")
            file_py_window.write("        super().__init__(**kwargs)\n")
            file_py_window.write("\n")

        self.file.create_window_ui_file(self.path, self.class_name)
    
