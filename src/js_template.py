# js_template.py
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

class JsTemplate():

    def __init__(self, is_gui, project_id, project_name, path, is_git, license):
        self.is_gui = is_gui
        self.project_id = project_id
        self.project_name = project_name
        self.path = path
        self.is_git = is_git
        self.lang = 'js'
        self.license = license
        self.file = File()
        self.gpl_text = self.file.get_gpl()

    def start(self):
        self.create_basic_gui_structure(self.project_id, self.project_name, self.path)
        self.populate_data_folder(self.project_id, self.project_name)
        self.populate_po_dir(self.project_id, self.project_name)
        self.populate_src_dir(self.project_id, self.project_name)
        if self.is_git:
            os.chdir(self.path)
            os.system('git init')

    def create_basic_gui_structure(self, p_id, p_name, path):
        p_full_name = p_id + '.' + p_name
        p_id_underscore = p_id.replace('.', '_').lower()

        os.makedirs(path + '/build-aux/meson')
        os.makedirs(path + '/' + 'data')
        os.makedirs(path + '/' + 'po')
        os.makedirs(path + '/' + 'src')

        self.file.create_copying_file(path, self.license)
        self.file.create_manifest_file(path, p_full_name, p_name, self.lang)
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

        self.file.create_data_meson_file(self.path, p_id)

        with open(self.path + '/data/' + p_id + '.appdata.xml.in', 'a') as file_app_data:
            file_app_data.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_app_data.write("<component type=\"desktop\">\n")
            file_app_data.write("\t<id>%s.desktop</id>\n" % p_id)
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
        self.file.create_gschema_file(self.path, p_full_name, p_name, p_path)

    def populate_po_dir(self, p_id, p_name):
        # p_full_name = p_id + '.' + p_name
        files = ['window.ui', 'window.js', 'main.js']

        self.file.create_po_linguas_file(self.path)
        self.file.create_po_meson_file(self.path, p_name)
        self.file.create_po_potfiles_file(self.path, p_id, files)

    def populate_src_dir(self, p_id, p_name):
        p_name_underscore = p_name.replace('-', '_')
        p_id_reverse = p_id.replace('.', '/') + '/' + p_name + '/'
        p_id_reverse_short = p_id.replace('.', '/')
        window_name = "".join(w.capitalize() for w in p_name.split('-'))

        with open(self.path + '/src/main.js', 'a') as file_js_main:
            file_js_main.write("/* main.js\n")
            file_js_main.write(" *\n")
            file_js_main.write(" * Copyright 2020\n")
            file_js_main.write(" *\n")
            file_js_main.write(self.gpl_text)
            file_js_main.write("\n")
            file_js_main.write("pkg.initGettext();\n")
            file_js_main.write("pkg.initFormat();\n")
            file_js_main.write("pkg.require({\n")
            file_js_main.write("  'Gio': '2.0',\n")
            file_js_main.write("  'Gtk': '3.0'\n")
            file_js_main.write("});\n")
            file_js_main.write("\n")
            file_js_main.write("const { Gio, Gtk } = imports.gi;\n")
            file_js_main.write("\n")
            file_js_main.write("const { %sWindow } = imports.window;\n" % window_name)
            file_js_main.write("\n")
            file_js_main.write("function main(argv) {\n")
            file_js_main.write("    const application = new Gtk.Application({\n")
            file_js_main.write("        application_id: '%s',\n" % p_id)
            file_js_main.write("        flags: Gio.ApplicationFlags.FLAGS_NONE,\n")
            file_js_main.write("    });\n")
            file_js_main.write("\n")
            file_js_main.write("    application.connect('activate', app => {\n")
            file_js_main.write("        let activeWindow = app.activeWindow;\n")
            file_js_main.write("\n")
            file_js_main.write("        if (!activeWindow) {\n")
            file_js_main.write("            activeWindow = new %sWindow(app);\n" % window_name)
            file_js_main.write("        }\n")
            file_js_main.write("\n")
            file_js_main.write("        activeWindow.present();\n")
            file_js_main.write("    });\n")
            file_js_main.write("\n")
            file_js_main.write("    return application.run(argv);\n")
            file_js_main.write("}\n")

        with open(self.path + '/src/meson.build', 'a') as file_meson_build:
            file_meson_build.write("pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())\n")
            file_meson_build.write("gnome = import('gnome')\n")
            file_meson_build.write("\n")
            file_meson_build.write("gnome.compile_resources('%s.src',\n" % p_id)
            file_meson_build.write("  '%s.src.gresource.xml',\n" % p_id)
            file_meson_build.write("  gresource_bundle: true,\n")
            file_meson_build.write("  install: true,\n")
            file_meson_build.write("  install_dir: pkgdatadir,\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("gnome.compile_resources('%s.data',\n" % p_id)
            file_meson_build.write("  '%s.data.gresource.xml',\n" % p_id)
            file_meson_build.write("  gresource_bundle: true,\n")
            file_meson_build.write("  install: true,\n")
            file_meson_build.write("  install_dir: pkgdatadir,\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("bin_conf = configuration_data()\n")
            file_meson_build.write("bin_conf.set('GJS', find_program('gjs').path())\n")
            file_meson_build.write("bin_conf.set('PACKAGE_VERSION', meson.project_version())\n")
            file_meson_build.write("bin_conf.set('PACKAGE_NAME', meson.project_name())\n")
            file_meson_build.write("bin_conf.set('prefix', get_option('prefix'))\n")
            file_meson_build.write("bin_conf.set('libdir', join_paths(get_option('prefix'), get_option('libdir')))\n")
            file_meson_build.write("bin_conf.set('datadir', join_paths(get_option('prefix'), get_option('datadir')))\n")
            file_meson_build.write("\n")
            file_meson_build.write("configure_file(\n")
            file_meson_build.write("  input: '%s.in',\n" % p_id)
            file_meson_build.write("  output: '%s',\n" % p_id)
            file_meson_build.write("  configuration: bin_conf,\n")
            file_meson_build.write("  install: true,\n")
            file_meson_build.write("  install_dir: get_option('bindir')\n")
            file_meson_build.write(")\n")

        with open(self.path + '/src/' + p_id + '.data.gresource.xml', 'a') as file_gresource_data:
            file_gresource_data.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_gresource_data.write("<gresources>\n")
            file_gresource_data.write("  <gresource prefix=\"/%s\">\n" % p_id_reverse_short)
            file_gresource_data.write("    <file>window.ui</file>\n")
            file_gresource_data.write("  </gresource>\n")
            file_gresource_data.write("</gresources>\n")
            file_gresource_data.write("\n")

        with open(self.path + '/src/' + p_id + '.in', 'a') as file_in:
            file_in.write("#!@GJS@\n")
            file_in.write("imports.package.init({\n")
            file_in.write("  name: \"@PACKAGE_NAME@\",\n")
            file_in.write("  version: \"@PACKAGE_VERSION@\",\n")
            file_in.write("  prefix: \"@prefix@\",\n")
            file_in.write("  libdir: \"@libdir@\",\n")
            file_in.write("  datadir: \"@datadir@\",\n")
            file_in.write("});\n")
            file_in.write("imports.package.run(imports.main);\n")

        st = os.stat(self.path + '/src/' + p_id + '.in')
        os.chmod(self.path + '/src/' + p_id + '.in', st.st_mode | stat.S_IEXEC)

        with open(self.path + '/src/' + p_id + '.src.gresource.xml', 'a') as file_gresource_src:
            file_gresource_src.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_gresource_src.write("<gresources>\n")
            file_gresource_src.write("  <gresource prefix=\"/%s/js\">\n" % p_id_reverse_short)
            file_gresource_src.write("    <file>window.js</file>\n")
            file_gresource_src.write("    <file>main.js</file>\n")
            file_gresource_src.write("  </gresource>\n")
            file_gresource_src.write("</gresources>\n")
            file_gresource_src.write("\n")

        with open(self.path + '/src/window.js', 'a') as file_js_window:
            file_js_window.write("/* window.js\n")
            file_js_window.write(" *\n")
            file_js_window.write(" * Copyright 2020\n")
            file_js_window.write(" *\n")
            file_js_window.write(self.gpl_text)
            file_js_window.write("\n")
            file_js_window.write("const { GObject, Gtk } = imports.gi;\n")
            file_js_window.write("\n")
            file_js_window.write("var %sWindow = GObject.registerClass({\n" % window_name)
            file_js_window.write("    GTypeName: '%sWindow',\n" % window_name)
            file_js_window.write("    Template: 'resource:///%s/window.ui',\n" % p_id_reverse_short)
            file_js_window.write("    InternalChildren: ['label']\n")
            file_js_window.write("}, class %sWindow extends Gtk.ApplicationWindow {\n" % window_name)
            file_js_window.write("    _init(application) {\n")
            file_js_window.write("        super._init({ application });\n")
            file_js_window.write("    }\n")
            file_js_window.write("});\n")
            file_js_window.write("\n")

        with open(self.path + '/src/window.ui', 'a') as file_window_ui:
            file_window_ui.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_window_ui.write("<interface>\n")
            file_window_ui.write("  <requires lib=\"gtk+\" version=\"3.24\"/>\n")
            file_window_ui.write("    <template class=\"%sWindow\" parent=\"GtkApplicationWindow\">\n" % window_name)
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
