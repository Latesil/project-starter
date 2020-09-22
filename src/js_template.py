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

import os
import datetime
from .project_starter_constants import constants
from .file import File
from .template import Template


class JsTemplate(Template):

    """
    JavaScript Template Class
    """

    def __init__(self, is_gui, project_id, project_name, path, is_git, license):
        self.data = {}
        self.data['is_gui'] = is_gui
        self.data['project_id'] = project_id
        self.data['project_name'] = project_name
        self.data['root'] = path
        self.data['is_git'] = is_git
        self.data['lang'] = 'js'
        self.data['project_license'] = license
        self.data['po_files'] = ['window.ui', 'window.js', 'main.js']
        self.data['gresource_files'] = ['window.ui']
        self.data['gresource_files_additional'] = ['window.js', 'main.js']
        self.data['year'] = datetime.datetime.now().year

        ##############################################################
        
        self.data['window_name'] = "".join(w.capitalize() for w in self.data['project_name'].split('-'))

        ##############################################################

        self.files = []

    def start(self):
        self.create_folders(self.data['root'])
        self.populate_root_dir(self.data)
        self.populate_data_dir(self.data)
        self.populate_po_dir(self.data)
        self.populate_src_dir(self.data)

        if self.data['is_git']:
            os.chdir(self.data['root'])
            os.system('git init')

        self.create_files(self.files, executable=self.data['project_id'] + '.in')

    def populate_root_dir(self, data):
        path = data['root']
        path_meson_postinstall = data['root'] + 'build-aux/meson/'

        copying_file = self.create_copying_file(path, data)
        self.files.append(copying_file)

        manifest_file = self.create_manifest_file(path, data)
        self.files.append(manifest_file)

        post_install_file = self.create_meson_postinstall_file(path_meson_postinstall)
        self.files.append(post_install_file)

        text = (
            f"project('{data['project_name']}',\n",
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
            f"meson.add_install_script('build-aux/meson/postinstall.py')\n",
        )

        main_meson_file = File(path, 'meson.build', text)
        self.files.append(main_meson_file)

    def populate_src_dir(self, data):
        path = data['root'] + 'src/'

        text_main = (
            f"/* main.js\n",
            f" *\n",
            f" * Copyright {data['year']}\n",
            f" *\n",
            f"{self.get_gpl(data['lang'])}",
            f" */\n",
            f"\n",
            f"pkg.initGettext();\n",
            f"pkg.initFormat();\n",
            f"pkg.require({{\n",
            f"  'Gio': '2.0',\n",
            f"  'Gtk': '3.0'\n",
            f"}});\n",
            f"\n",
            f"const {{ Gio, Gtk }} = imports.gi;\n",
            f"\n",
            f"const {{ {data['window_name']}Window }} = imports.window;\n",
            f"\n",
            f"function main(argv) {{\n",
            f"    const application = new Gtk.Application({{\n",
            f"        application_id: '{data['project_id']}',\n",
            f"        flags: Gio.ApplicationFlags.FLAGS_NONE,\n",
            f"    }});\n",
            f"\n",
            f"    application.connect('activate', app => {{\n",
            f"        let activeWindow = app.activeWindow;\n",
            f"\n",
            f"        if (!activeWindow) {{\n",
            f"            activeWindow = new {data['window_name']}Window(app);\n",
            f"        }}\n",
            f"\n",
            f"        activeWindow.present();\n",
            f"    }});\n",
            f"\n",
            f"    return application.run(argv);\n",
            f"}}\n",
        )

        main_src_file = File(path, 'main.js', text_main)
        self.files.append(main_src_file)

        text_meson = (
            f"pkgdatadir = join_paths(get_option('datadir'), meson.project_name())\n",
            f"gnome = import('gnome')\n",
            f"\n",
            f"src_res = gnome.compile_resources('{data['project_id']}.src',\n",
            f"  '{data['project_id']}.src.gresource.xml',\n",
            f"  gresource_bundle: true,\n",
            f"  install: true,\n",
            f"  install_dir: pkgdatadir,\n",
            f")\n",
            f"\n",
            f"data_res = gnome.compile_resources('{data['project_id']}.data',\n",
            f"  '{data['project_id']}.data.gresource.xml',\n",
            f"  gresource_bundle: true,\n",
            f"  install: true,\n",
            f"  install_dir: pkgdatadir,\n",
            f")\n",
            f"\n",
            f"bin_conf = configuration_data()\n",
            f"bin_conf.set('GJS', find_program('gjs').path())\n",
            f"bin_conf.set('PACKAGE_VERSION', meson.project_version())\n",
            f"bin_conf.set('PACKAGE_NAME', meson.project_name())\n",
            f"bin_conf.set('prefix', get_option('prefix'))\n",
            f"bin_conf.set('libdir', join_paths(get_option('prefix'), get_option('libdir')))\n",
            f"bin_conf.set('datadir', join_paths(get_option('prefix'), get_option('datadir')))\n",
            f"\n",
            f"configure_file(\n",
            f"  input: '{data['project_id']}.in',\n",
            f"  output: '{data['project_id']}',\n",
            f"  configuration: bin_conf,\n",
            f"  install: true,\n",
            f"  install_dir: get_option('bindir')\n",
            f")\n",
        )

        meson_src_file = File(path, 'meson.build', text_meson)
        self.files.append(meson_src_file)
        
        gresource_file = self.create_gresource_file(path, data, prefix='data')
        self.files.append(gresource_file)

        additional_gresource_file = self.create_gresource_file(path, data, additional=True, prefix='src')
        self.files.append(additional_gresource_file)

        text_id_in = (
            f"#!@GJS@\n",
            f"imports.package.init({{\n",
            f"  name: \"@PACKAGE_NAME@\",\n",
            f"  version: \"@PACKAGE_VERSION@\",\n",
            f"  prefix: \"@prefix@\",\n",
            f"  libdir: \"@libdir@\",\n",
            f"  datadir: \"@datadir@\",\n",
            f"}});\n",
            f"imports.package.run(imports.main);\n",
        )

        in_src_file = File(path, data['project_id'] + '.in', text_id_in)
        self.files.append(in_src_file)

        text_window = (
            f"/* window.js\n",
            f" *\n",
            f" * Copyright {data['year']}\n",
            f" *\n",
            f"{self.get_gpl(data['lang'])}",
            f" */\n",
            f"\n",
            f"const {{ GObject, Gtk }} = imports.gi;\n",
            f"\n",
            f"var {data['window_name']}Window = GObject.registerClass({{\n",
            f"    GTypeName: '{data['window_name']}Window',\n",
            f"    Template: 'resource:///{data['project_id'].replace('.', '/')}/window.ui',\n",
            f"    InternalChildren: ['label']\n",
            f"}}, class {data['window_name']}Window extends Gtk.ApplicationWindow {{\n",
            f"    _init(application) {{\n",
            f"        super._init({{ application }});\n",
            f"    }}\n",
            f"}});\n",
            f"\n",
        )
        
        window_file = File(path, 'window.js', text_window)
        self.files.append(window_file)

        window_ui_file = self.create_window_ui_file(path, data)
        self.files.append(window_ui_file)
