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
        create_file(path, 'COPYING', license.get_text())

    def create_manifest_file(self, path, p_id, p_name, lang, ext=False):
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
        text = ()
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
        text = (f"#!/usr/bin/env python3\n",
                f"\n",
                f"from os import environ, path\n",
                f"from subprocess import call\n",
                f"\n",
                f"prefix = environ.get('MESON_INSTALL_PREFIX', '/usr/local')\n",
                f"datadir = path.join(prefix, 'share')\n",
                f"destdir = environ.get('DESTDIR', '')\n",
                f"\n",
                f"# Package managers set this so we don't need to run\n",
                f"if not destdir:\n",
                f"    print('Updating icon cache...')\n",
                f"    call(['gtk-update-icon-cache', '-qtf', path.join(datadir, 'icons', 'hicolor')])\n",
                f"\n",
                f"    print('Updating desktop database...')\n",
                f"    call(['update-desktop-database', '-q', path.join(datadir, 'applications')])\n",
                f"\n",
                f"    print('Compiling GSettings schemas...')\n",
                f"    call(['glib-compile-schemas', path.join(datadir, 'glib-2.0', 'schemas')])\n",
                f"\n",)

        create_file(path + '/build-aux/meson/', 'postinstall.py', text)

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
        text = (f"desktop_file = i18n.merge_file(\n",
                f"  input: '{p_full_name}.desktop.in',\n",
                f"  output: '{p_full_name}.desktop',\n",
                f"  type: 'desktop',\n",
                f"  po_dir: '../po',\n",
                f"  install: true,\n",
                f"  install_dir: join_paths(get_option('datadir'), 'applications')\n",
                f")\n",
                f"\n",
                f"desktop_utils = find_program('desktop-file-validate', required: false)\n",
                f"if desktop_utils.found()\n",
                f"  test('Validate desktop file', desktop_utils,\n",
                f"    args: [desktop_file]\n",
                f"  )\n",
                f"endif\n",
                f"\n",
                f"appstream_file = i18n.merge_file(\n",
                f"  input: '{p_full_name}.appdata.xml.in',\n",
                f"  output: '{p_full_name}.appdata.xml',\n",
                f"  po_dir: '../po',\n",
                f"  install: true,\n",
                f"  install_dir: join_paths(get_option('datadir'), '{constants['METADATA_FOLDER']}')\n",
                f")\n",
                f"\n",
                f"appstream_util = find_program('appstream-util', required: false)\n",
                f"if appstream_util.found()\n",
                f"  test('Validate appstream file', appstream_util,\n",
                f"    args: ['validate', appstream_file]\n",
                f"  )\n",
                f"endif\n",
                f"\n",
                f"install_data('{p_full_name}.gschema.xml',\n",
                f"  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')\n",
                f")\n",
                f"\n",
                f"compile_schemas = find_program('glib-compile-schemas', required: false)\n",
                f"if compile_schemas.found()\n",
                f"  test('Validate schema file', compile_schemas,\n",
                f"    args: ['--strict', '--dry-run', meson.current_source_dir()]\n",
                f"  )\n",
                f"endif\n",
                f"\n",)

        create_file(path, 'meson.build', text)

    def create_appdata_file(self, path, p_id, project_license):
        text = (f"""<?xml version="1.0" encoding="UTF-8"?>\n""",
                f"""<component type="desktop">\n""",
                f"""  <id>{p_id}.desktop</id>\n""",
                f"""  <metadata_license>CC0-1.0</metadata_license>\n""",)

        if project_license == "GPL 3":
            text += (f"""  <project_license>GPL-3.0-or-later</project_license>\n""",)
        elif project_license == "AGPL 3":
            text += (f"""  <project_license>AGPL-3.0-or-later</project_license>\n""",)
        elif project_license == "Apache 2":
            text += (f"""  <project_license></project_license>\n""",)
        elif project_license == "GPL 2":
            text += (f"""  <project_license></project_license>\n""",)
        elif project_license == "LGPL 2":
            text += (f"""  <project_license>LGPL-2.1-or-later</project_license>\n""",)
        elif project_license == "LGPL 3":
            text += (f"""  <project_license>LGPL-3.0-or-later</project_license>\n""",)
        elif project_license == "MIT/X11":
            text += (f"""  <project_license>MIT</project_license>\n""",)

        text += (f"""  <description>\n""",
                f"""  </description>\n""",
                f"""</component>\n""",
                f"""\n""",)

        create_file(path, p_id + '.appdata.xml.in', text)

    def create_gresource_file(self, path, p_name_underscore, p_id_reverse_short, files):
        text = (f"""<?xml version="1.0" encoding="UTF-8"?>\n""",
                f"""<gresources>\n""",
                f"""  <gresource prefix="/{p_id_reverse_short}">\n""",)
        
        for f in files:
            text += ("    <file>%s</file>\n" % f,)
            
        text += (f"""  </gresource>\n""",
                f"""</gresources>\n""",
                f"""\n""",)

        create_file(path + '/src/', p_name_underscore + '.gresource.xml', text)

    def create_window_ui_file(self, path, window_name):
        text = (f"""<?xml version="1.0" encoding="UTF-8"?>\n""",
                f"""\n""",
                f"""<interface>\n""",
                f"""  <requires lib="gtk+" version="3.24"/>\n""",
                f"""    <template class="{window_name}Window" parent="GtkApplicationWindow">\n""",
                f"""      <property name="default-width">600</property>\n""",
                f"""    <property name="default-height">300</property>\n""",
                f"""    <child type="titlebar">\n""",
                f"""      <object class="GtkHeaderBar" id="header_bar">\n""",
                f"""        <property name="visible">True</property>\n""",
                f"""        <property name="show-close-button">True</property>\n""",
                f"""        <property name="title">Hello, World!</property>\n""",
                f"""      </object>\n""",
                f"""    </child>\n""",
                f"""    <child>\n""",
                f"""      <object class="GtkLabel" id="label">\n""",
                f"""        <property name="label">Hello, World!</property>\n""",
                f"""        <property name="visible">True</property>\n""",
                f"""        <attributes>\n""",
                f"""          <attribute name="weight" value="bold"/>\n""",
                f"""          <attribute name="scale" value="2"/>\n""",
                f"""        </attributes>\n""",
                f"""      </object>\n""",
                f"""    </child>\n""",
                f"""    </template>\n""",
                f"""  </interface>\n""",)

        create_file(path + '/src/', 'window.ui', text)

