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

    def create_manifest_file(self, path, p_full_name, p_name, lang):
        #TODO rewrite: move lang specific code to appropriate templates
        with open(path + '/' + p_full_name + ".json", 'a') as file_main_json:
            file_main_json.write("{\n")

            if lang == 'python':
                file_main_json.write("    \"app-id\" : \"%s\",\n" % p_full_name)
            else:
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
        with open(path + '/po/meson.build', 'a') as file_meson_build:
            file_meson_build.write("i18n.gettext('%s', preset: 'glib')\n" % p_name)
            file_meson_build.write("\n")

    def create_po_linguas_file(self, path):
        #TODO maybe there is another way to create an empty file?
        with open(path + '/po/LINGUAS', 'a') as file_linguas:
            file_linguas.close()

    def create_po_potfiles_file(self, path, p_id, files):
        if not isinstance(files, list):
            print('Cannot create POTFILES. Argument is invalid')
            return

        with open(path + '/po/POTFILES', 'a') as file_potfiles:
            file_potfiles.write("data/%s.desktop.in\n" % p_id)
            file_potfiles.write("data/%s.appdata.xml.in\n" % p_id)
            file_potfiles.write("data/%s.gschema.xml\n" % p_id)
            for f in files:
                file_potfiles.write("src/%s\n" % f)
            file_potfiles.write("\n")

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
        with open(path + '/data/' + p_full_name + '.desktop.in', 'a') as file_desktop:
            file_desktop.write("[Desktop Entry]\n")
            file_desktop.write("Name=%s\n" % p_name)
            file_desktop.write("Exec=%s\n" % p_name)
            if gui:
                file_desktop.write("Terminal=false\n")
            file_desktop.write("Type=Application\n")
            file_desktop.write("Categories=GTK;\n")
            file_desktop.write("StartupNotify=true\n")
            file_desktop.write("Icon=%s" % p_id)

    def create_gschema_file(self, path, p_full_name, p_name, p_path):
        with open(path + '/data/' + p_full_name + '.gschema.xml', 'a') as file_gschema:
            file_gschema.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_gschema.write("<schemalist gettext-domain=\"%s\">\n" % p_name)
            file_gschema.write("\t<schema id=\"%s\" path=\"/%s/\">\n" % (p_full_name, p_path))
            file_gschema.write("\t</schema>\n")
            file_gschema.write("</schemalist>\n")
            file_gschema.write("\n")

    def create_data_meson_file(self, path, p_full_name):
        with open(path + '/data/meson.build', 'a') as file_meson_build:
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
            
