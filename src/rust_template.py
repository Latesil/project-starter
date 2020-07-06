# rust_template.py
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

class RustTemplate():

    gpl_text = """# This program is free software: you can redistribute it and/or modify
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
"""

    def __init__(self, is_gui, project_id, project_name, path, is_git, license):
        self.is_gui = is_gui
        self.project_id = project_id
        self.project_name = project_name
        self.path = path
        self.is_git = is_git
        self.license = license

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
            file_license.write(license.get_text())

        with open(path + '/' + p_full_name + ".json", 'a') as file_main_json:
            file_main_json.write("{\n")
            file_main_json.write("    \"app-id\" : \"%s\",\n" % p_full_name)
            file_main_json.write("    \"runtime\" : \"org.gnome.Platform\",\n")
            file_main_json.write("    \"runtime-version\" : \"3.34\",\n")
            file_main_json.write("    \"sdk\" : \"org.gnome.Sdk\",\n")
            file_main_json.write("    \"sdk-extensions\" : [\n")
            file_main_json.write("        \"org.freedesktop.Sdk.Extension.rust-stable\"\n")
            file_main_json.write("    \"],\"\n")
            file_main_json.write("    \"command\" : \"%s\",\n" % p_name)
            file_main_json.write("    \"finish-args\" : [\n")
            file_main_json.write("        \"--share=network\",\n")
            file_main_json.write("        \"--share=ipc\",\n")
            file_main_json.write("        \"--socket=fallback-x11\",\n")
            file_main_json.write("        \"--socket=wayland\"\n")
            file_main_json.write("    ],\n")
            file_main_json.write("    \"build-options\" : {\n")
            file_main_json.write("        \"append-path\" : \"/usr/lib/sdk/rust-stable/bin\",\n")
            file_main_json.write("        \"build-args\" : [\n")
            file_main_json.write("            \"--share=network\"\n")
            file_main_json.write("        \"],\n")
            file_main_json.write("        \"env\" : {\n")
            file_main_json.write("            \"CARGO_HOME\" : \"/run/build/rust-gui-example/cargo\",\n")
            file_main_json.write("            \"RUST_BACKTRACE\" : \"1\",\n")
            file_main_json.write("            \"RUST_LOG\" : \"rust-gui-example=debug\"\n")
            file_main_json.write("        }\n")
            file_main_json.write("    },\n")
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
            file_main_json.write("            ],\n")
            file_main_json.write("        },\n")
            file_main_json.write("    ],\n")
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
            file_meson_build.write("    meson_version: '>= 0.50.0',\n")
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
