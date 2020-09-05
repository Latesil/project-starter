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
from .project_starter_constants import constants
from .common_files import File
from .helpers import *

class RustTemplate():

    def __init__(self, is_gui, project_id, project_name, path, is_git, license):
        self.is_gui = is_gui
        self.project_id = project_id
        self.project_name = project_name
        self.path = path
        self.is_git = is_git
        self.lang = 'rust'
        self.license = license
        self.file = File()

    def start(self):
        self.create_basic_gui_structure(self.project_id, self.project_name, self.path)
        if self.is_gui:
            self.populate_data_folder(self.project_id, self.project_name)
            self.populate_po_dir(self.project_id, self.project_name)
        self.populate_src_dir(self.project_id, self.project_name)
        if self.is_git:
            os.chdir(self.path)
            os.system('git init')

    def create_basic_gui_structure(self, p_id, p_name, path):
        build_aux_path = '/build-aux/meson' if self.is_gui else '/build-aux'
        os.makedirs(path + build_aux_path)
        if self.is_gui:
            os.makedirs(path + '/' + 'data')
            os.makedirs(path + '/' + 'po')
        os.makedirs(path + '/' + 'src')

        self.file.create_copying_file(path, self.license)

        if self.is_gui
            self.file.create_manifest_file(path, p_id, p_name, self.lang)
            self.file.create_meson_postinstall_file(path)

        text_meson = (f"project('{p_name}',\n",
                      f"          version: '0.1.0',\n",
                      f"    meson_version: '>= {constants['MESON_VERSION']}',\n",
                      f"  default_options: [ 'warning_level=2',\n",
                      f"                   ],\n",
                      f")\n",
                      f"\n",)

        if self.is_gui:
            text_meson += ("i18n = import('i18n')\n",)

        text_meson += (f"\n",
                       f"\n",)

        if self.is_gui:
            text_meson += ("subdir('data')\n",)

        text_meson += (f"subdir('src')\n",)

        if self.is_gui:
            text_meson += ("subdir('po')\n",)

        text_meson += (f"\n",)

        if self.is_gui:
            text_meson += ("meson.add_install_script('build-aux/meson/postinstall.py')\n",)

        create_file(path + '/', 'meson.build', text_meson)

        text_cargo = (f"""#!/bin/sh\n""",
                      f"""\n""",
                      f"""export MESON_BUILD_ROOT="$1"\n""",
                      f"""export MESON_SOURCE_ROOT="$2"\n""",
                      f"""export CARGO_TARGET_DIR="$MESON_BUILD_ROOT"/target\n""",
                      f"""export CARGO_HOME="$CARGO_TARGET_DIR"/cargo-home\n""",
                      f"""export OUTPUT="$3"\n""",
                      f"""export BUILDTYPE="$4"\n""",
                      f"""export APP_BIN="$5"\n""",
                      f"""\n""",
                      f"""\n""",
                      f"""if [[ $BUILDTYPE = "release" ]]\n""",
                      f"""then\n""",
                      f"""    echo "RELEASE MODE"\n""",
                      f"""    cargo build --manifest-path \\\n""",
                      f"""        "$MESON_SOURCE_ROOT"/Cargo.toml --release && \\\n""",
                      f"""        cp "$CARGO_TARGET_DIR"/release/"$APP_BIN" "$OUTPUT"\n""",
                      f"""else\n""",
                      f"""    echo "DEBUG MODE"\n""",
                      f"""    cargo build --manifest-path \\\n""",
                      f"""        "$MESON_SOURCE_ROOT"/Cargo.toml --verbose && \\\n""",
                      f"""        cp "$CARGO_TARGET_DIR"/debug/"$APP_BIN" "$OUTPUT"\n""",
                      f"""fi\n""",
                      f"""\n""",)
        
        create_file(path + '/build-aux/', 'cargo.sh', text_cargo)
        make_executable(path + '/build-aux/cargo.sh')

    def populate_data_folder(self, p_id, p_name):
        p_id_reverse = p_id.replace('.', '/') + '/' + p_name + '/'
        p_full_name = p_id + '.' + p_name
        p_path = p_id.replace('.', '/')

        self.file.create_data_meson_file(self.path, p_id)
        self.file.create_appdata_file(self.path, p_id, self.license)
        self.file.create_desktop_file(self.path, p_full_name, p_name, p_id)
        self.file.create_gschema_file(self.path, p_full_name, p_name, p_path)

    def populate_po_dir(self, p_id, p_name):
        p_full_name = p_id + '.' + p_name
        files = ['window.ui']

        self.file.create_po_linguas_file(self.path)
        self.file.create_po_meson_file(self.path, p_name)
        self.file.create_po_potfiles_file(self.path, p_id, files)

    def populate_src_dir(self, p_id, p_name):
        p_name_underscore = p_name.replace('-', '_')
        p_id_reverse = p_id.replace('.', '/') + '/' + p_name + '/'
        p_id_reverse_short = p_id.replace('.', '/')

        if self.is_gui:
            text_config = (f"pub static PKGDATADIR: &str = @pkgdatadir@;\n",
                           f"pub static VERSION: &str = @VERSION@;\n",
                           f"pub static LOCALEDIR: &str = @localedir@;\n",)
            
            create_file(path + '/src/', 'config.rs.in', text_config)

        if self.is_gui:
            text_main = (f"use gettextrs::*;\n",
                         f"use gio::prelude::*;\n",
                         f"use gtk::prelude::*;\n",
                         f"\n",
                         f"mod config;\n",
                         f"mod window;\n",
                         f"use crate::window::Window;\n",
                         f"\n",
                         f"fn main() {{\n",
                         f"    gtk::init().unwrap_or_else(|_| panic!(\"Failed to initialize GTK.\"));\n",
                         f"\n",
                         f"    setlocale(LocaleCategory::LcAll, \"\");\n",
                         f"    bindtextdomain(\"{p_name}\", config::LOCALEDIR);\n",
                         f"    textdomain(\"%{p_name}\");\n",
                         f"\n",
                         f"    let res = gio::Resource::load(config::PKGDATADIR.to_owned() + \"/{p_name}.gresource\")\n",
                         f"        .expect(\"Could not load resources\");\n",
                         f"    gio::resources_register(&res);\n",
                         f"\n",
                         f"    let app = gtk::Application::new(Some(\"{p_id}\"), Default::default()).unwrap();\n",
                         f"    app.connect_activate(move |app| {{\n",
                         f"        let window = Window::new();\n",
                         f"\n",
                         f"        window.widget.set_application(Some(app));\n",
                         f"        app.add_window(&window.widget);\n",
                         f"        window.widget.present();\n",
                         f"    }});\n",
                         f"\n",
                         f"    let ret = app.run(&std::env::args().collect::<Vec<_>>());\n",
                         f"    std::process::exit(ret);\n",
                         f"}}\n",)
        else:
            text_main = (f"fn main() {{\n",
                        f"    println!(\"Hello World\");\n",
                        f"}}\n")

        create_file(path + '/src/', 'main.rs', text_main)

        if self.is_cli:
            text_meson = (f"pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())\n",
                         f"gnome = import('gnome')\n",
                         f"\n",
                         f"gnome.compile_resources('{p_name}',\n",
                         f"  '{p_name_underscore}.gresource.xml',\n",
                         f"  gresource_bundle: true,\n"",
                         f"  install: true,\n",
                         f"  install_dir: pkgdatadir,\n",
                         f")\n"",
                         f"\n"",
                         f"conf = configuration_data()\n",
                         f"conf.set_quoted('VERSION', meson.project_version())\n",
                         f"conf.set_quoted('localedir', join_paths(get_option('prefix'), get_option('localedir')))\n",
                         f"conf.set_quoted('pkgdatadir', pkgdatadir)\n",
                         f"\n",
                         f"configure_file(\n",
                         f"  input: 'config.rs.in',\n",
                         f"  output: 'config.rs',\n",
                         f"  configuration: conf,\n",
                         f")\n",
                         f"\n",
                         f"# Copy the config.rs output to the source directory.\n",
                         f"run_command(\n",
                         f"  'cp',\n",
                         f"  join_paths(meson.build_root(), 'src', 'config.rs'),\n",
                         f"  join_paths(meson.source_root(), 'src', 'config.rs'),\n",
                         f"  check: true\n",
                         f")\n",
                         f"\n",
                         f"sources = files(\n",
                         f"  'config.rs',\n",
                         f"  'main.rs',\n",
                         f"  'window.rs',\n",
                         f")\n",
                         f"{p_name_underscore}_sources = [",
                         f"  'main.rs',\n",
                         f"]\n",
                         f"{p_name_underscore}_deps = [\n",
                         f"]\n",
                         f"cargo_script = find_program(join_paths(meson.source_root(), 'build-aux/cargo.sh'))\n",
                         f"cargo_release = custom_target(\n",
                         f"  'cargo-build',\n",
                         f"  build_by_default: true,\n",
                         f"  input: sources,\n",
                         f"  input: {p_name_underscore}_sources,\n",
                         f"  output: meson.project_name(),\n",
                         f"  console: true,\n",
                         f"  install: true,\n",
                         f"  install_dir: get_option('bindir'),\n",
                         f"  command: [\n",
                         f"    cargo_script,\n",
                         f"    meson.build_root(),\n",
                         f"    meson.source_root(),\n",
                         f"    '@OUTPUT@',\n",
                         f"    get_option('buildtype'),\n",
                         f"    meson.project_name(),\n",
                         f" ]\n",
                         f")\n",)

        create_file(path + '/src/', 'meson.build', text_meson)

        if self.is_gui:
            files = ['window.ui']
            self.file.create_gresource_file(path, p_name_underscore, p_id_reverse, files)

            text_window = (f"use gtk::prelude::*;\n",
                    f"\n",
                    f"pub struct Window {{\n",
                    f"    pub widget: gtk::ApplicationWindow,\n",
                    f"}}\n",
                    f"\n",
                    f"impl Window {{\n",
                    f"    pub fn new() -> Self {{\n",
                    f"        let builder = gtk::Builder::new_from_resource(\"/{p_id_reverse_short}/window.ui\");\n",
                    f"        let widget: gtk::ApplicationWindow = builder\n",
                    f"            .get_object(\"window\")\n"",
                    f"            .expect(\"Failed to find the window object\");\n",
                    f"\n",
                    f"        Self {{ widget }}\n",
                    f"    }}\n",
                    f"}}\n",)

            create_file(path + '/src/', 'window.rs', text_window)

            text_window_ui = (f"""<?xml version="1.0" encoding="UTF-8"?>\n""",
                              f"""<interface>\n""",
                              f"""  <requires lib="gtk+" version="3.24"/>\n""",
                              f"""    <object class="GtkApplicationWindow" id="window">\n""",
                              f"""      <property name="default-width">600</property>\n""",
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
                              f"""      </object>\n"""",
                              f"""    </child>\n""",
                              f"""    </object>\n""",
                              f"""  </interface>\n""",)

            create_file(path + '/src/', 'window.ui', text_window_ui)

