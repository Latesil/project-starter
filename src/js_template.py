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

class JsTemplate():

    gpl_text = """ * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
"""

    def __init__(self, is_gui, project_id, project_name, path, is_git, license):
        self.is_gui = is_gui
        self.project_id = project_id
        self.project_name = project_name
        self.path = path
        self.is_git = is_git
        self.license = license

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

        with open(path + '/' + p_id + ".json", 'a') as file_main_json:
            file_main_json.write("{\n")
            file_main_json.write("    \"app-id\" : \"%s\",\n" % p_id)
            file_main_json.write("    \"runtime\" : \"org.gnome.Platform\",\n")
            file_main_json.write("    \"runtime-version\" : \"%s\",\n" % constants['GNOME_PLATFORM_VERSION'])
            file_main_json.write("    \"sdk\" : \"org.gnome.Sdk\",\n")
            file_main_json.write("    \"command\" : \"%s\",\n" % p_id)
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
            file_main_json.write("        \"/share/gtk-doc\",\n")
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

        with open(path + '/build-aux/meson/postinstall.py', 'a') as file_postinstall:
            file_postinstall.write("#!/usr/bin/env python3\n")
            file_postinstall.write("\n")
            file_postinstall.write("from os import environ, path\n")
            file_postinstall.write("from subprocess import call\n")
            file_postinstall.write("\n")
            file_postinstall.write("prefix = environ.get('MESON_INSTALL_PREFIX', '/usr/local')\n")
            file_postinstall.write("datadir = path.join(prefix, 'share')\n")
            file_postinstall.write("destdir = environ.get('DESTDIR', '')\n")
            file_postinstall.write("\n")
            file_postinstall.write("# Package managers set this so we don't need to run\n")
            file_postinstall.write("if not destdir:\n")
            file_postinstall.write("    print('Updating icon cache...')\n")
            file_postinstall.write("    call(['gtk-update-icon-cache', '-qtf', path.join(datadir, 'icons', 'hicolor')])\n")
            file_postinstall.write("\n")
            file_postinstall.write("    print('Updating desktop database...')\n")
            file_postinstall.write("    call(['update-desktop-database', '-q', path.join(datadir, 'applications')])\n")
            file_postinstall.write("\n")
            file_postinstall.write("    print('Compiling GSettings schemas...')\n")
            file_postinstall.write("    call(['glib-compile-schemas', path.join(datadir, 'glib-2.0', 'schemas')])\n")
            file_postinstall.write("\n")

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
            file_meson_build.write("  input: '%s.desktop.in',\n" % p_id)
            file_meson_build.write("  output: '%s.desktop',\n" % p_id)
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
            file_meson_build.write("  input: '%s.appdata.xml.in',\n" % p_id)
            file_meson_build.write("  output: '%s.appdata.xml',\n" % p_id)
            file_meson_build.write("  po_dir: '../po',\n")
            file_meson_build.write("  install: true,\n")
            file_meson_build.write("  install_dir: join_paths(get_option('datadir'), 'appdata')\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("appstream_util = find_program('appstream-util', required: false)\n")
            file_meson_build.write("if appstream_util.found()\n")
            file_meson_build.write("  test('Validate appstream file', appstream_util,\n")
            file_meson_build.write("    args: ['validate', appstream_file]\n")
            file_meson_build.write("  )\n")
            file_meson_build.write("endif\n")
            file_meson_build.write("\n")
            file_meson_build.write("install_data('%s.gschema.xml',\n" % p_id)
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

        with open(self.path + '/data/' + p_id + '.appdata.xml.in', 'a') as file_app_data:
            file_app_data.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_app_data.write("<component type=\"desktop\">\n")
            file_app_data.write("\t<id>%s.desktop</id>\n" % p_id)
            file_app_data.write("\t<metadata_license>CC0-1.0</metadata_license>\n")
            if self.license == 'GPL 3':
                file_app_data.write("\t<project_license>GPL-3.0-or-later</project_license>\n")
            file_app_data.write("\t<description>\n")
            file_app_data.write("\t</description>\n")
            file_app_data.write("</component>\n")
            file_app_data.write("\n")

        with open(self.path + '/data/' + p_id + '.desktop.in', 'a') as file_desktop:
            file_desktop.write("[Desktop Entry]\n")
            file_desktop.write("Name=%s\n" % p_name)
            file_desktop.write("Exec=%s\n" % p_name)
            file_desktop.write("Terminal=false\n")
            file_desktop.write("Type=Application\n")
            file_desktop.write("Categories=GTK;\n")
            file_desktop.write("StartupNotify=true\n")

        with open(self.path + '/data/' + p_id + '.gschema.xml', 'a') as file_gschema:
            file_gschema.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_gschema.write("<schemalist gettext-domain=\"%s\">\n" % p_name)
            file_gschema.write("\t<schema id=\"%s\" path=\"/%s/\">\n" % (p_id, p_path))
            file_gschema.write("\t</schema>\n")
            file_gschema.write("</schemalist>\n")
            file_gschema.write("\n")

    def populate_po_dir(self, p_id, p_name):
        p_full_name = p_id + '.' + p_name

        #TODO maybe there is another way to create an empty file?
        with open(self.path + '/po/LINGUAS', 'a') as file_linguas:
            file_linguas.close()

        with open(self.path + '/po/meson.build', 'a') as file_meson_build:
            file_meson_build.write("i18n.gettext('%s', preset: 'glib')\n" % p_name)
            file_meson_build.write("\n")

        with open(self.path + '/po/POTFILES', 'a') as file_potfiles:
            file_potfiles.write("data/%s.desktop.in\n" % p_id)
            file_potfiles.write("data/%s.appdata.xml.in\n" % p_id)
            file_potfiles.write("data/%s.gschema.xml\n" % p_id)
            file_potfiles.write("src/window.ui\n")
            file_potfiles.write("src/window.js\n")
            file_potfiles.write("src/main.js\n")
            file_potfiles.write("\n")

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
