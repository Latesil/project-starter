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
from .project_starter_constants import constants
from .common_files import File
from .helpers import *

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
        self.file.create_manifest_file(path, p_id, p_name, self.lang)
        self.file.create_meson_postinstall_file(path)

        text = (f"project('{p_name}',\n",
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
                f"meson.add_install_script('build-aux/meson/postinstall.py')\n",)

        create_file(path + '/', 'meson.build', text)

    def populate_data_folder(self, p_id, p_name):
        p_id_reverse = p_id.replace('.', '/') + '/' + p_name + '/'
        p_full_name = p_id + '.' + p_name
        p_path = p_id.replace('.', '/')

        self.file.create_data_meson_file(self.path, p_id)
        self.file.create_appdata_file(self.path, p_id, self.license)
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

        text_main = (f"/* main.js\n",
                     f" *\n",
                     f" * Copyright 2020\n",
                     f" *\n",
                     self.gpl_text,
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
                     f"const {{ {window_name}Window }} = imports.window;\n",
                     f"\n",
                     f"function main(argv) {{\n",
                     f"    const application = new Gtk.Application({{\n",
                     f"        application_id: '{p_id}',\n",
                     f"        flags: Gio.ApplicationFlags.FLAGS_NONE,\n",
                     f"    }});\n",
                     f"\n",
                     f"    application.connect('activate', app => {{\n",
                     f"        let activeWindow = app.activeWindow;\n",
                     f"\n",
                     f"        if (!activeWindow) {{\n",
                     f"            activeWindow = new {window_name}Window(app);\n",
                     f"        }}\n",
                     f"\n",
                     f"        activeWindow.present();\n",
                     f"    }});\n",
                     f"\n",
                     f"    return application.run(argv);\n",
                     f"}}\n",)

        create_file(path + '/src/', 'main.js', text_main)

        text_meson = (f"pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())\n",
                      f"gnome = import('gnome')\n",
                      f"\n",
                      f"gnome.compile_resources('{p_id}.src',\n",
                      f"  '{p_id}.src.gresource.xml',\n",
                      f"  gresource_bundle: true,\n",
                      f"  install: true,\n",
                      f"  install_dir: pkgdatadir,\n",
                      f")\n",
                      f"\n",
                      f"gnome.compile_resources('{p_id}.data',\n",
                      f"  '{p_id}.data.gresource.xml',\n",
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
                      f"  input: '{p_id}.in',\n",
                      f"  output: '{p_id}',\n",
                      f"  configuration: bin_conf,\n",
                      f"  install: true,\n",
                      f"  install_dir: get_option('bindir')\n",
                      f")\n",)

        create_file(path + '/src/', 'meson.build', text_meson)

        files = ['window.js', 'main.js']
        self.file.create_gresource_file(self.path, p_id, p_id_reverse, files)

        text_id_in = (f"#!@GJS@\n",
                        f"imports.package.init({{\n",
                        f"  name: \"@PACKAGE_NAME@\",\n",
                        f"  version: \"@PACKAGE_VERSION@\",\n",
                        f"  prefix: \"@prefix@\",\n",
                        f"  libdir: \"@libdir@\",\n",
                        f"  datadir: \"@datadir@\",\n",
                        f"}});\n",
                        f"imports.package.run(imports.main);\n",)

        create_file(path + '/src/', p_id + 'in', text_id_in)
        make_executable(self.path + '/src/' + p_id + '.in')

        text_window = (f"/* window.js\n",
                        f" *\n",
                        f" * Copyright 2020\n",
                        f" *\n",
                        self.gpl_text,
                        f"\n",
                        f"const {{ GObject, Gtk }} = imports.gi;\n",
                        f"\n",
                        f"var {window_name}Window = GObject.registerClass({{\n",
                        f"    GTypeName: '{window_name}Window',\n",
                        f"    Template: 'resource:///{p_id_reverse_short}/window.ui',\n",
                        f"    InternalChildren: ['label']\n",
                        f"}}, class %sWindow extends Gtk.ApplicationWindow {{\n",
                        f"    _init(application) {{\n",
                        f"        super._init({{ application }});\n",
                        f"    }}\n",
                        f"}});\n",
                        f"\n")
        
        create_file(path + '/src/', 'window.js', text_window)

        self.file.create_window_ui_file(self.path, window_name)
