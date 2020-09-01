# common_files.py
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

from .project_starter_constants import constants
from .helpers import *

class File:

    def __init__(self):
        self.gpl = """# This program is free software: you can redistribute it and/or modify
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

    def get_gpl(self):
        return self.gpl

    def create_copying_file(self, path, project_license):
        with open(path + '/COPYING', 'a') as file_license:
            if project_license == 'GPL 3':
                from .gpl import Gpl
                license = Gpl('3')
            elif project_license == 'GPL 2':
                from .gpl import Gpl
                license = Gpl('2')
            elif project_license == 'AGPL 3':
                from .agpl import Agpl
                license = Agpl()
            elif project_license == 'Apache 2':
                from .apache import Apache
                license = Apache()
            elif project_license == 'LGPL 3':
                from .lgpl import Lgpl
                license = Lgpl('3')
            elif project_license == 'LGPL 2':
                from .lgpl import Lgpl
                license = Lgpl('2')
            elif project_license == 'MIT/X11':
                from .mit import Mit
                license = Mit()
            file_license.write(license.get_text())

    def create_manifest_file(self, path, p_id, p_name, lang):
        #TODO rewrite: move lang specific code to appropriate templates
        with open(path + '/' + p_id + ".json", 'a') as file_main_json:
            file_main_json.write("{\n")
            file_main_json.write("    \"app-id\" : \"%s\",\n" % p_id)
            file_main_json.write("    \"runtime\" : \"org.gnome.Platform\",\n")
            file_main_json.write("    \"runtime-version\" : \"%s\",\n" % constants['GNOME_PLATFORM_VERSION'])
            file_main_json.write("    \"sdk\" : \"org.gnome.Sdk\",\n")

            if lang == 'rust':
                file_main_json.write("    \"sdk-extensions\" : [\n")
                file_main_json.write("        \"org.freedesktop.Sdk.Extension.rust-stable\"\n")
                file_main_json.write("    ],\n")

            if lang == 'js':
                file_main_json.write("    \"command\" : \"%s\",\n" % p_id)
            else:
                file_main_json.write("    \"command\" : \"%s\",\n" % p_name)

            file_main_json.write("    \"finish-args\" : [\n")
            file_main_json.write("        \"--share=network\",\n")
            file_main_json.write("        \"--share=ipc\",\n")
            file_main_json.write("        \"--socket=fallback-x11\",\n")
            file_main_json.write("        \"--socket=wayland\"\n")
            file_main_json.write("    ],\n")

            if lang == 'rust':
                file_main_json.write("    \"build-options\" : {\n")
                file_main_json.write("        \"append-path\" : \"/usr/lib/sdk/rust-stable/bin\",\n")
                file_main_json.write("        \"build-args\" : [\n")
                file_main_json.write("            \"--share=network\"\n")
                file_main_json.write("        ],\n")
                file_main_json.write("        \"env\" : {\n")
                file_main_json.write("            \"CARGO_HOME\" : \"/run/build/%s/cargo\",\n" % p_name)
                file_main_json.write("            \"RUST_BACKTRACE\" : \"1\",\n")
                file_main_json.write("            \"RUST_LOG\" : \"%s=debug\"\n" % p_name)
                file_main_json.write("        }\n")
                file_main_json.write("    },\n")

            file_main_json.write("    \"cleanup\" : [\n")
            file_main_json.write("        \"/include\",\n")
            file_main_json.write("        \"/lib/pkgconfig\",\n")
            file_main_json.write("        \"/man\",\n")
            file_main_json.write("        \"/share/doc\",\n")

            if lang == 'js' or lang == 'c':
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

    def create_po_meson_file(self, path, p_name):
        text = (f"i18n.gettext('{p_name}', preset: 'glib')\n",)
        create_file(path, 'meson.build', text)

    def create_po_linguas_file(self, path):
        text = () # TODO find another solution
        create_file(path, 'LINGUAS', text, empty=True)

    def create_po_potfiles_file(self, path, p_id, files):
        if not isinstance(files, list):
            print('Cannot create POTFILES. Argument is invalid (must be list)')
            return

        text = (f"data/{p_id}.desktop.in\n",
                f"data/{p_id}.appdata.xml.in\n",
                f"data/{p_id}.gschema.xml\n",)

        for f in files:
            text += ("src/%s\n" % f,)

        text += ("\n",)
        create_file(path, 'POTFILES', text)

    def create_meson_postinstall_file(self, path):
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

    def create_desktop_file(self, path, p_full_name, p_name, p_id, gui=True):
        text = (f"[Desktop Entry]\n",
                f"Name={p_name}\n",
                f"Exec={p_name}\n",)

        if gui:
            text += (f"Terminal=false\n",)

        text += (f"Type=Application\n",
                 f"Categories=GTK;\n",
                 f"StartupNotify=true\n",
                 f"Icon={p_id}\n",)

        create_file(path, p_full_name + '.desktop.in', text)

    def create_gschema_file(self, path, p_full_name, p_name, p_path):
        text = (f"""<?xml version="1.0" encoding="UTF-8"?>\n""",
                f"""<schemalist gettext-domain="{p_name}">\n""",
                f"""    <schema id="{p_full_name}" path="/{p_path}/">\n""",
                f"""    </schema>\n""",
                f"""</schemalist>\n""",)
        create_file(path, p_full_name + '.gschema.xml', text)

    def create_data_meson_file(self, path, p_full_name):
        with open(path + 'meson.build', 'a') as file_meson_build:
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

    def create_appdata_file(self, path, p_id, project_license):
        with open(path + p_id + '.appdata.xml.in', 'a') as file_app_data:
            file_app_data.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_app_data.write("<component type=\"desktop\">\n")
            file_app_data.write("\t<id>%s.desktop</id>\n" % p_id)
            file_app_data.write("\t<metadata_license>CC0-1.0</metadata_license>\n")
            if project_license == 'GPL 3':
                file_app_data.write("\t<project_license>GPL-3.0-or-later</project_license>\n")
            elif project_license == 'AGPL 3':
                file_app_data.write("\t<project_license>AGPL-3.0-or-later</project_license>\n")
            elif project_license == 'Apache 2':
                file_app_data.write("\t<project_license></project_license>\n")
            elif project_license == 'GPL 2':
                file_app_data.write("\t<project_license></project_license>\n")
            elif project_license == 'LGPL 2':
                file_app_data.write("\t<project_license>LGPL-2.1-or-later</project_license>\n")
            elif project_license == 'LGPL 3':
                file_app_data.write("\t<project_license>LGPL-3.0-or-later</project_license>\n")
            elif project_license == 'MIT/X11':
                file_app_data.write("\t<project_license>MIT</project_license>\n")
            file_app_data.write("\t<description>\n")
            file_app_data.write("\t</description>\n")
            file_app_data.write("</component>\n")
            file_app_data.write("\n")

    def create_gresource_file(self, path, p_name_underscore, p_id_reverse_short, files):
        with open(path + '/src/' + p_name_underscore + '.gresource.xml', 'a') as file_gresource:
            file_gresource.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_gresource.write("<gresources>\n")
            file_gresource.write("  <gresource prefix=\"/%s\">\n" % p_id_reverse_short)
            for f in files:
                file_gresource.write("    <file>%s</file>\n" % f)
            file_gresource.write("  </gresource>\n")
            file_gresource.write("</gresources>\n")
            file_gresource.write("\n")

    def create_window_ui_file(self, path, window_name):
        with open(path + '/src/window.ui', 'a') as file_window_ui:
            file_window_ui.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_window_ui.write("\n")
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

