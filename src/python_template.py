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
from .project_starter_constants import constants
from .common_files import File

class PythonTemplate():

    def __init__(self, is_gui, project_id, project_name, path, is_git, license):
        self.is_gui = is_gui
        self.project_id = project_id
        self.project_name = project_name
        self.path = path
        self.is_git = is_git
        self.license = license
        self.file = File()
        self.gpl_text = self.file.get_gpl()

    def start(self):
        if self.is_gui:
            self.create_basic_gui_structure(self.project_id, self.project_name, self.path)
            self.populate_data_folder(self.project_id, self.project_name)
            self.populate_po_dir(self.project_id, self.project_name)
            self.populate_src_dir(self.project_id, self.project_name)
            if self.is_git:
                os.chdir(self.path)
                os.system('git init')

    def create_basic_gui_structure(self, p_id, p_name, path):
        p_full_name = p_id + '.' + p_name

        os.makedirs(path + '/build-aux/meson')
        os.makedirs(path + '/' + 'data')
        os.makedirs(path + '/' + 'po')
        os.makedirs(path + '/' + 'src')

        with open(path + '/' + "COPYING", 'a') as file_license:
            if self.license == 'GPL 3':
                from .gpl import Gpl
                license = Gpl('3')
            elif self.license == 'GPL 2':
                from .gpl import Gpl
                license = Gpl('2')
            elif self.license == 'AGPL 3':
                from .agpl import Agpl
                license = Agpl()
            elif self.license == 'Apache 2':
                from .apache import Apache
                license = Apache()
            elif self.license == 'LGPL 3':
                from .lgpl import Lgpl
                license = Lgpl('3')
            elif self.license == 'LGPL 2':
                from .lgpl import Lgpl
                license = Lgpl('2')
            elif self.license == 'MIT/X11':
                from .mit import Mit
                license = Mit()
            file_license.write(license.get_text())

        with open(path + '/' + p_full_name + ".json", 'a') as file_main_json:
            file_main_json.write("{\n")
            file_main_json.write("    \"app-id\" : \"%s\",\n" % p_full_name)
            file_main_json.write("    \"runtime\" : \"org.gnome.Platform\",\n")
            file_main_json.write("    \"runtime-version\" : \"%s\",\n" % constants['GNOME_PLATFORM_VERSION'])
            file_main_json.write("    \"sdk\" : \"org.gnome.Sdk\",\n")
            file_main_json.write("    \"command\" : \"%s\",\n" % p_name)
            file_main_json.write("    \"finish-args\" : [\n")
            file_main_json.write("        \"--share=network\",\n")
            file_main_json.write("        \"--share=ipc\",\n")
            file_main_json.write("        \"--socket=fallback-x11\",\n")
            file_main_json.write("        \"--socket=wayland\"\n")
            file_main_json.write("    ],\n")
            file_main_json.write("    \"cleanup\" : [\n")
            file_main_json.write("        \"/include\",\n")
            file_main_json.write("        \"/lib/pkgconfig\",\n")
            file_main_json.write("        \"/man\",\n")
            file_main_json.write("        \"/share/doc\",\n")
            file_main_json.write("        \"/share/man\",\n")
            file_main_json.write("        \"/share/pkgconfig\",\n")
            file_main_json.write("        \"*.la\",\n")
            file_main_json.write("        \"*.a\"\n")
            file_main_json.write("    ],\n")
            file_main_json.write("    \"modules\" : [\n")
            file_main_json.write("        {\n")
            file_main_json.write("            \"name\" : \"%s\",\n" % p_name)
            file_main_json.write("            \"builddir\" : true,\n")
            file_main_json.write("            \"buildsystem\" : \"meson\",\n")
            file_main_json.write("            \"sources\" : [\n")
            file_main_json.write("                {\n")
            file_main_json.write("                    \"type\" : \"git\",\n")
            file_main_json.write("                    \"url\" : \"file://%s\"\n" % path)
            file_main_json.write("                }\n")
            file_main_json.write("            ]\n")
            file_main_json.write("        }\n")
            file_main_json.write("    ]\n")
            file_main_json.write("}\n")

        self.file.create_meson_postinstall_file(path)

        with open(path + '/' + "meson.build", 'a') as file_meson_build:
            file_meson_build.write("project('%s',\n" % p_name)
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

    def populate_data_folder(self, p_id, p_name):
        p_id_reverse = p_id.replace('.', '/') + '/' + p_name + '/'
        p_full_name = p_id + '.' + p_name
        p_path = p_id.replace('.', '/')

        with open(self.path + '/data/meson.build', 'a') as file_meson_build:
            file_meson_build.write("desktop_file = i18n.merge_file(\n")
            file_meson_build.write("  input: '%s.desktop.in',\n" % p_full_name)
            file_meson_build.write("  output: '%s.desktop',\n" % p_full_name)
            file_meson_build.write("  type: 'desktop',\n")
            file_meson_build.write("  po_dir: '../po',\n")
            file_meson_build.write("  install: true,\n")
            file_meson_build.write("  install_dir: join_paths(get_option('datadir'), 'applications')\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("desktop_utils = find_program('desktop-file-validate', required: false)\n")
            file_meson_build.write("if desktop_utils.found()\n")
            file_meson_build.write("  test('Validate desktop file', desktop_utils,\n")
            file_meson_build.write("    args: [desktop_file]\n")
            file_meson_build.write("  )\n")
            file_meson_build.write("endif\n")
            file_meson_build.write("\n")
            file_meson_build.write("appstream_file = i18n.merge_file(\n")
            file_meson_build.write("  input: '%s.appdata.xml.in',\n" % p_full_name)
            file_meson_build.write("  output: '%s.appdata.xml',\n" % p_full_name)
            file_meson_build.write("  po_dir: '../po',\n")
            file_meson_build.write("  install: true,\n")
            file_meson_build.write("  install_dir: join_paths(get_option('datadir'), '%s')\n" % constants['METADATA_FOLDER'])
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("appstream_util = find_program('appstream-util', required: false)\n")
            file_meson_build.write("if appstream_util.found()\n")
            file_meson_build.write("  test('Validate appstream file', appstream_util,\n")
            file_meson_build.write("    args: ['validate', appstream_file]\n")
            file_meson_build.write("  )\n")
            file_meson_build.write("endif\n")
            file_meson_build.write("\n")
            file_meson_build.write("install_data('%s.gschema.xml',\n" % p_full_name)
            file_meson_build.write("  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("compile_schemas = find_program('glib-compile-schemas', required: false)\n")
            file_meson_build.write("if compile_schemas.found()\n")
            file_meson_build.write("  test('Validate schema file', compile_schemas,\n")
            file_meson_build.write("    args: ['--strict', '--dry-run', meson.current_source_dir()]\n")
            file_meson_build.write("  )\n")
            file_meson_build.write("endif\n")
            file_meson_build.write("\n")

        with open(self.path + '/data/' + p_full_name + '.appdata.xml.in', 'a') as file_app_data:
            file_app_data.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_app_data.write("<component type=\"desktop\">\n")
            file_app_data.write("\t<id>%s.desktop</id>\n" % p_full_name)
            file_app_data.write("\t<metadata_license>CC0-1.0</metadata_license>\n")
            if self.license == 'GPL 3':
                file_app_data.write("\t<project_license>GPL-3.0-or-later</project_license>\n")
            elif self.license == 'AGPL 3':
                file_app_data.write("\t<project_license>AGPL-3.0-or-later</project_license>\n")
            elif self.license == 'Apache 2':
                file_app_data.write("\t<project_license></project_license>\n")
            elif self.license == 'GPL 2':
                file_app_data.write("\t<project_license></project_license>\n")
            elif self.license == 'LGPL 2':
                file_app_data.write("\t<project_license>LGPL-2.1-or-later</project_license>\n")
            elif self.license == 'LGPL 3':
                file_app_data.write("\t<project_license>LGPL-3.0-or-later</project_license>\n")
            elif self.license == 'MIT/X11':
                file_app_data.write("\t<project_license>MIT</project_license>\n")
            file_app_data.write("\t<description>\n")
            file_app_data.write("\t</description>\n")
            file_app_data.write("</component>\n")
            file_app_data.write("\n")

        self.file.create_desktop_file(self.path, p_full_name, p_name, p_id)
        self.file.create_gschema_file(self.path, p_full_name, p_name, p_path):

    def populate_po_dir(self, p_id, p_name):
        p_full_name = p_id + '.' + p_name
        files = ['window.ui', 'main.py', 'window.py']
        self.file.create_po_linguas_file(self.path)
        self.file.create_po_meson_file(self.path, p_name)
        self.file.create_po_potfiles_file(self.path, p_id, files)

    def populate_src_dir(self, p_id, p_name):
        class_name = "".join(w.capitalize() for w in p_name.split('-'))
        p_name_underscore = p_name.replace('-', '_')
        p_id_reverse = p_id.replace('.', '/') + '/' + p_name + '/'
        p_id_reverse_short = p_id.replace('.', '/')

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
            file_py_main.write("from .window import %sWindow\n" % class_name)
            file_py_main.write("\n")
            file_py_main.write("\n")
            file_py_main.write("class Application(Gtk.Application):\n")
            file_py_main.write("    def __init__(self):\n")
            file_py_main.write("        super().__init__(application_id='%s',\n" % p_id)
            file_py_main.write("                         flags=Gio.ApplicationFlags.FLAGS_NONE)\n")
            file_py_main.write("\n")
            file_py_main.write("    def do_activate(self):\n")
            file_py_main.write("        win = self.props.active_window\n")
            file_py_main.write("        if not win:\n")
            file_py_main.write("            win = %sWindow(application=self)\n" % class_name)
            file_py_main.write("        win.present()\n")
            file_py_main.write("\n")
            file_py_main.write("\n")
            file_py_main.write("def main(version):\n")
            file_py_main.write("    app = Application()\n")
            file_py_main.write("    return app.run(sys.argv)\n")
            file_py_main.write("\n")

        with open(self.path + '/src/meson.build', 'a') as file_meson_build:
            file_meson_build.write("pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())\n")
            file_meson_build.write("moduledir = join_paths(pkgdatadir, '%s')\n" % p_name_underscore)
            file_meson_build.write("gnome = import('gnome')\n")
            file_meson_build.write("\n")
            file_meson_build.write("gnome.compile_resources('%s',\n" % p_name)
            file_meson_build.write("  '%s.gresource.xml',\n" % p_name_underscore)
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
            file_meson_build.write("  input: '%s.in',\n" % p_name)
            file_meson_build.write("  output: '%s',\n" % p_name)
            file_meson_build.write("  configuration: conf,\n")
            file_meson_build.write("  install: true,\n")
            file_meson_build.write("  install_dir: get_option('bindir')\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("%s_sources = [\n" % p_name_underscore)
            file_meson_build.write("  '__init__.py',\n")
            file_meson_build.write("  'main.py',\n")
            file_meson_build.write("  'window.py',\n")
            file_meson_build.write("]\n")
            file_meson_build.write("\n")
            file_meson_build.write("install_data(%s_sources, install_dir: moduledir)\n" % p_name_underscore)
            file_meson_build.write("\n")

        with open(self.path + '/src/' + p_name + '.in', 'a') as file_exec:
            file_exec.write("#!@PYTHON@\n")
            file_exec.write("#\n")
            file_exec.write("# %s.in\n" % p_name)
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
            file_exec.write("gettext.install('%s', localedir)\n" % p_name)
            file_exec.write("\n")
            file_exec.write("if __name__ == '__main__':\n")
            file_exec.write("    import gi\n")
            file_exec.write("\n")
            file_exec.write("    from gi.repository import Gio\n")
            file_exec.write("    resource = Gio.Resource.load(os.path.join(pkgdatadir, '%s.gresource'))\n" % p_name)
            file_exec.write("    resource._register()\n")
            file_exec.write("\n")
            file_exec.write("    from %s import main\n" % p_name_underscore)
            file_exec.write("    sys.exit(main.main(VERSION))\n")

        st = os.stat(self.path + '/src/' + p_name + '.in')
        os.chmod(self.path + '/src/' + p_name + '.in', st.st_mode | stat.S_IEXEC)

        with open(self.path + '/src/' + p_name_underscore + '.gresource.xml', 'a') as file_gresource:
            file_gresource.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_gresource.write("<gresources>\n")
            file_gresource.write("  <gresource prefix=\"/%s\">\n" % p_id_reverse_short)
            file_gresource.write("    <file>window.ui</file>\n")
            file_gresource.write("  </gresource>\n")
            file_gresource.write("</gresources>\n")
            file_gresource.write("\n")

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
            file_py_window.write("@Gtk.Template(resource_path='/%swindow.ui')\n" % p_id_reverse)
            file_py_window.write("class %sWindow(Gtk.ApplicationWindow):\n" % class_name)
            file_py_window.write("    __gtype_name__ = '%sWindow'\n" % class_name)
            file_py_window.write("\n")
            file_py_window.write("    label = Gtk.Template.Child()\n")
            file_py_window.write("\n")
            file_py_window.write("    def __init__(self, **kwargs):\n")
            file_py_window.write("        super().__init__(**kwargs)\n")
            file_py_window.write("\n")

        with open(self.path + '/src/window.ui', 'a') as file_window_ui:
            file_window_ui.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_window_ui.write("\n")
            file_window_ui.write("<interface>\n")
            file_window_ui.write("  <requires lib=\"gtk+\" version=\"3.24\"/>\n")
            file_window_ui.write("    <template class=\"%sWindow\" parent=\"GtkApplicationWindow\">\n" % class_name)
            file_window_ui.write("      <property name=\"default-width\">600</property>\n")
            file_window_ui.write("    <property name=\"default-height\">300</property>\n")
            file_window_ui.write("    <child type=\"titlebar\">\n")
            file_window_ui.write("      <object class=\"GtkHeaderBar\" id=\"header_bar\">\n")
            file_window_ui.write("        <property name=\"visible\">True</property>\n")
            file_window_ui.write("        <property name=\"show-close-button\">True</property>\n")
            file_window_ui.write("        <property name=\"title\">Hello, World!</property>\n")
            file_window_ui.write("      </object>\n")
            file_window_ui.write("    </child>\n")
            file_window_ui.write("    <child>\n")
            file_window_ui.write("      <object class=\"GtkLabel\" id=\"label\">\n")
            file_window_ui.write("        <property name=\"label\">Hello, World!</property>\n")
            file_window_ui.write("        <property name=\"visible\">True</property>\n")
            file_window_ui.write("        <attributes>\n")
            file_window_ui.write("          <attribute name=\"weight\" value=\"bold\"/>\n")
            file_window_ui.write("          <attribute name=\"scale\" value=\"2\"/>\n")
            file_window_ui.write("        </attributes>\n")
            file_window_ui.write("      </object>\n")
            file_window_ui.write("    </child>\n")
            file_window_ui.write("    </template>\n")
            file_window_ui.write("  </interface>\n")
    
