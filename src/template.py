# template.py
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
from .project_starter_constants import constants
from .file import File


class Template:

    gui_folders = ['build-aux/meson', 'data', 'src', 'po']
    cli_folders = ['src']

    def __init__(self):
        self.files = []

    def get_gpl(self, lang):
        if lang == 'python':
            comment = '#'
        else:
            comment = '*'

        gpl = f""" {comment} This program is free software: you can redistribute it and/or modify
{comment} it under the terms of the GNU General Public License as published by
{comment} the Free Software Foundation, either version 3 of the License, or
{comment} (at your option) any later version.
{comment}
{comment} This program is distributed in the hope that it will be useful,
{comment} but WITHOUT ANY WARRANTY; without even the implied warranty of
{comment} MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
{comment} GNU General Public License for more details.
{comment}
{comment} You should have received a copy of the GNU General Public License
{comment} along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
        return gpl

    def create_folders(self, root, additional_folders=None, gui=True):
        if additional_folders is None:
            additional_folders = []
        else:
            if len(additional_folders) == 0:
                print('Folder creation error: empty list')
                return

        if gui:
            final_folders = self.gui_folders + additional_folders
        else:
            final_folders = self.cli_folders + additional_folders

        for folder in final_folders:
            directory = os.path.join(root, folder)
            if not os.path.exists(directory):
                os.makedirs(directory)
            else:
                print(f'Folder with name {folder} already exists!')

    ########## /build-aux/meson/ dir ###############

    def create_meson_postinstall_file(self, path):
        text = (
            f"#!/usr/bin/env python3\n",
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
            f"\n",
        )

        f = File(path, 'postinstall.py', text)
        return f

    ########## end /build-aux/meson/ dir ########


    ################## /po dir ##################

    def create_po_potfiles_file(self, path, data):
        if not isinstance(data['po_files'], list):
            print('Cannot create POTFILES. Argument is invalid (must be list)')
            return

        text = (
            f"data/{data['project_id']}.desktop.in\n",
            f"data/{data['project_id']}.appdata.xml.in\n",
            f"data/{data['project_id']}.gschema.xml\n",
        )

        for f in data['po_files']:
            text += (f"src/{f}\n",)

        text += (f"\n",)

        f = File(path, 'POTFILES', text)
        return f

    def create_po_linguas_file(self, path):
        text = ()
        f = File(path, 'LINGUAS', text)
        return f

    def create_po_meson_file(self, path, data):
        text = (f"i18n.gettext('{data['project_name']}', preset: 'glib')\n",)
        f = File(path, 'meson.build', text)
        return f

    ################## end /po dir ##################


    ################## / dir ########################

    def create_copying_file(self, path, data):
        if data['project_license'] == 'GPL 3':
            from .gpl import Gpl
            license = Gpl('3')
        elif data['project_license'] == 'GPL 2':
            from .gpl import Gpl
            license = Gpl('2')
        elif data['project_license'] == 'AGPL 3':
            from .agpl import Agpl
            license = Agpl()
        elif data['project_license'] == 'Apache 2':
            from .apache import Apache
            license = Apache()
        elif data['project_license'] == 'LGPL 3':
            from .lgpl import Lgpl
            license = Lgpl('3')
        elif data['project_license'] == 'LGPL 2':
            from .lgpl import Lgpl
            license = Lgpl('2')
        elif data['project_license'] == 'MIT/X11':
            from .mit import Mit
            license = Mit()

        f = File(path, 'COPYING', license.get_text())
        return f

    def create_manifest_file(self, path, data, sdk_extension=None, build_options=None):
        text = (
            f"""app-id: {data['project_id']}\n""",
            f"""runtime: org.gnome.Platform\n""",
            f"""runtime-version: '{constants['GNOME_PLATFORM_VERSION']}'\n""",
            f"""sdk: org.gnome.Sdk\n""",
        )

        if sdk_extension:
            text += sdk_extension

        if data['lang'] == 'js':
            text += (f"""command: {data['project_id']}\n""",)
        else:
            text += (f"""command: {data['project_name']}\n""",)
        
        text += (
            f"""finish-args:\n""",
            f"""  - --share=network\n""",
            f"""  - --share=ipc\n""",
            f"""  - --socket=fallback-x11\n""",
            f"""  - --socket=wayland\n""",
        )

        if build_options:
            text += build_options

        text += (
            f"""cleanup:\n""",
            f"""  - /include\n""",
            f"""  - /lib/pkgconfig\n""",
            f"""  - /man\n""",
            f"""  - /share/doc\n""",
            f"""  - /share/gtk-doc\n""",
            f"""  - /share/man\n""",
            f"""  - /share/pkgconfig\n""",
            f"""  - '*.la'\n""",
            f"""  - '*.a'\n""",
            f"""modules:\n""",
            f"""  - name: {data['project_name']}\n""",
            f"""    builddir: true\n""",
            f"""    buildsystem: meson\n""",
            f"""    sources:\n""",
            f"""      - type: dir\n""",
            f"""        path: .\n""",
        )

        f = File(path, data['project_id'] + ".yaml", text)
        return f

    ################# end / dir #################


    ################# /data dir #################

    def create_desktop_file(self, path, data, gui=True):
        text = (f"[Desktop Entry]\n",)

        if data['lang'] == 'rust' or data['lang'] == 'python':
            text += (f"Name={data['project_name']}\n",
                    f"Exec={data['project_name']}\n",)
        else:
            text += (f"Name={data['project_name']}\n",
                    f"Exec={data['project_id']}\n",)

        if gui:
            text += (f"Terminal=false\n",)

        text += (f"Type=Application\n",
                 f"Categories=GTK;\n",
                 f"StartupNotify=true\n",)

        f = File(path, data['project_id'] + '.desktop.in', text)
        return f

    def create_gschema_file(self, path, data):
        text = (
            f"""<?xml version="1.0" encoding="UTF-8"?>\n""",
            f"""<schemalist gettext-domain="{data['project_name']}">\n""",
            f"""    <schema id="{data['project_id']}" path="/{data['project_id'].replace('.', '/')}/">\n""",
            f"""    </schema>\n""",
            f"""</schemalist>\n""",
        )

        f = File(path, data['project_id'] + '.gschema.xml', text)
        return f

    def create_data_meson_file(self, path, data):
        text = (
            f"desktop_file = i18n.merge_file(\n",
            f"  input: '{data['project_id']}.desktop.in',\n",
            f"  output: '{data['project_id']}.desktop',\n",
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
            f"  input: '{data['project_id']}.appdata.xml.in',\n",
            f"  output: '{data['project_id']}.appdata.xml',\n",
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
            f"install_data('{data['project_id']}.gschema.xml',\n",
            f"  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')\n",
            f")\n",
            f"\n",
            f"compile_schemas = find_program('glib-compile-schemas', required: false)\n",
            f"if compile_schemas.found()\n",
            f"  test('Validate schema file', compile_schemas,\n",
            f"    args: ['--strict', '--dry-run', meson.current_source_dir()]\n",
            f"  )\n",
            f"endif\n",
            f"\n",
        )

        f = File(path, 'meson.build', text)
        return f

    def create_appdata_file(self, path, data):
        text = (
            f"""<?xml version="1.0" encoding="UTF-8"?>\n""",
            f"""<component type="desktop">\n""",
            f"""  <id>{data['project_id']}.desktop</id>\n""",
            f"""  <metadata_license>CC0-1.0</metadata_license>\n""",
        )

        if data['project_license'] == "GPL 3":
            text += (f"""  <project_license>GPL-3.0-or-later</project_license>\n""",)
        elif data['project_license'] == "AGPL 3":
            text += (f"""  <project_license>AGPL-3.0-or-later</project_license>\n""",)
        elif data['project_license'] == "Apache 2":
            text += (f"""  <project_license></project_license>\n""",)
        elif data['project_license'] == "GPL 2":
            text += (f"""  <project_license></project_license>\n""",)
        elif data['project_license'] == "LGPL 2":
            text += (f"""  <project_license>LGPL-2.1-or-later</project_license>\n""",)
        elif data['project_license'] == "LGPL 3":
            text += (f"""  <project_license>LGPL-3.0-or-later</project_license>\n""",)
        elif data['project_license'] == "MIT/X11":
            text += (f"""  <project_license>MIT</project_license>\n""",)

        text += (
            f"""  <description>\n""",
            f"""    <p>\n""",
            f"""    </p>\n""",
            f"""  </description>\n""",
            f"""</component>\n""",
            f"""\n""",
        )

        f = File(path, data['project_id'] + '.appdata.xml.in', text)
        return f

    def create_gresource_file(self, path, data, additional=False, prefix=None):
        text = (f"""<?xml version="1.0" encoding="UTF-8"?>\n""",
                f"""<gresources>\n""",)
        
        if not additional:
            text += (f"""  <gresource prefix="/{data['project_id'].replace('.', '/')}">\n""",)
        else:
            text += (f"""  <gresource prefix="/{data['project_id'].replace('.', '/')}/js">\n""",)
        
        if not additional:
            for f in data['gresource_files']:
                text += (f"    <file>{f}</file>\n",)
        else:
            for f in data['gresource_files_additional']:
                text += (f"    <file>{f}</file>\n",)
            
        text += (f"""  </gresource>\n""",
                f"""</gresources>\n""",
                f"""\n""",)

        if prefix:
            f = File(path, data['project_id'] + '.' + prefix + '.gresource.xml', text)
        else:
            if data['lang'] == 'js':
                f = File(path, data['project_id'] + '.gresource.xml', text)
            else:
                f = File(path, data['project_name'].replace('-', '_') + '.gresource.xml', text)

        return f

    ############### end /data dir #################


    ################# /src/ dir ###################

    def create_window_ui_file(self, path, data):
        text = (
            f"""<?xml version="1.0" encoding="UTF-8"?>\n""",
            f"""<interface>\n""",
            f"""  <requires lib="gtk+" version="3.24"/>\n""",
            f"""    <template class="{data['window_name']}Window" parent="GtkApplicationWindow">\n""",
            f"""      <property name="default-width">600</property>\n""",
            f"""    <property name="default-height">300</property>\n""",
            f"""    <child type="titlebar">\n""",
        )
        
        if data['lang'] == 'js':
            text += (f"""      <object class="GtkHeaderBar" id="headerBar">\n""",)
        else:
            text += (f"""      <object class="GtkHeaderBar" id="header_bar">\n""",)

        text += (
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
            f"""  </interface>\n""",
        )

        if data['lang'] == 'c':
            f = File(path, data['ui_filename'], text)
        else:
            f = File(path, 'window.ui', text)
        return f

    ############### end /src/ dir #################

    def create_files(self, files, executable=None):
        """
        Creates all files in list, and make one of them executable
        executable is a string contains filename
        """
        for f in files:
            f.create()
            if executable:
                if f.filename == executable:
                    f.make_executable()


    def populate_po_dir(self, data):
        path = os.path.join(data['root'], 'po')

        linguas_file = self.create_po_linguas_file(path)
        self.files.append(linguas_file)

        po_meson_file = self.create_po_meson_file(path, data)
        self.files.append(po_meson_file)

        potfiles_file = self.create_po_potfiles_file(path, data)
        self.files.append(potfiles_file)

        self.create_files(self.files)
        self.files = []

    def populate_data_dir(self, data):
        path = os.path.join(data['root'], 'data')

        meson_data_file = self.create_data_meson_file(path, data)
        self.files.append(meson_data_file)

        appdata_file = self.create_appdata_file(path, data)
        self.files.append(appdata_file)

        desktop_file = self.create_desktop_file(path, data)
        self.files.append(desktop_file)

        gschema_file = self.create_gschema_file(path, data)
        self.files.append(gschema_file)

        self.create_files(self.files)
        self.files = []
