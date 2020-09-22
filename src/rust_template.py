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

import os
from .project_starter_constants import constants
from .file import File
from .template import Template

class RustTemplate(Template):

    """
    Rust Template Class
    """

    def __init__(self, is_gui, project_id, project_name, path, is_git, license):
        self.data = {}
        self.data['is_gui'] = is_gui
        self.data['project_id'] = project_id
        self.data['project_name'] = project_name
        self.data['root'] = path
        self.data['is_git'] = is_git
        self.data['lang'] = 'rust'
        self.data['project_license'] = license
        self.files = []
        self.data['po_files'] = ['window.ui']
        self.data['gresource_files'] = ['window.ui']

        ##############################################################
        
        self.data['window_name'] = "".join(w.capitalize() for w in self.data['project_name'].split('-'))

        ##############################################################

    def start(self):
        if self.data['is_gui']:
            self.create_folders(self.data['root'])
        else:
            self.create_folders(self.data['root'], gui=False)

        self.populate_root_dir(self.data)

        if self.data['is_gui']:
            self.populate_data_dir(self.data)
            self.populate_po_dir(self.data)

        self.populate_src_dir(self.data)

        if self.data['is_gui']:
            os.chdir(self.data['root'])
            os.system('git init')

        for f in self.files:
            f.create()
            if f.filename == 'cargo.sh':
                f.make_executable()

    def populate_root_dir(self, data):
        path = self.data['root'] + '/build-aux/meson' if self.data['is_gui'] else self.data['root'] + '/build-aux'

        sdk_extension = (
            f"sdk-extensions:\n",
            f"  - org.freedesktop.Sdk.Extension.rust-stable\n",
        )

        build_options = (
            f"build-options:\n",
            f"    append-path: /usr/lib/sdk/rust-stable/bin\n",
            f"    build-args:\n",
            f"      - --share=network\n",
            f"    env:\n",
            f"      - CARGO_HOME: /run/build/rust-example/cargo\n",
            f"        RUST_BACKTRACE: 1\n",
            f"        RUST_LOG: rust-example=debug\n",
        )

        copying_file = self.create_copying_file(self.data['root'], data)
        self.files.append(copying_file)

        if self.data['is_gui']:
            manifest_file = self.create_manifest_file(self.data['root'], data, 
                                                      sdk_extension=sdk_extension,
                                                      build_options=build_options)
            self.files.append(manifest_file)
            
            post_install_file = self.create_meson_postinstall_file(path)
            self.files.append(post_install_file)

        text_meson = (
            f"project('{data['project_name']}',\n",
            f"          version: '0.1.0',\n",
            f"    meson_version: '>= {constants['MESON_VERSION']}',\n",
            f"  default_options: [ 'warning_level=2',\n",
            f"                   ],\n",
            f")\n",
            f"\n",
        )

        if self.data['is_gui']:
            text_meson += (
                "i18n = import('i18n')\n",
            )

        text_meson += (f"\n",
                       f"\n",)

        if self.data['is_gui']:
            text_meson += (
                "subdir('data')\n",
            )

        text_meson += (
            "subdir('src')\n",
        )

        if self.data['is_gui']:
            text_meson += (
                "subdir('po')\n",
            )

        text_meson += (f"\n",)

        if self.data['is_gui']:
            text_meson += (
                "meson.add_install_script('build-aux/meson/postinstall.py')\n",
            )

        main_meson_file = File(self.data['root'], 'meson.build', text_meson)
        self.files.append(main_meson_file)

        text_cargo = (
            f"""#!/bin/sh\n""",
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
            f"""if [ $BUILDTYPE = "release" ]\n""",
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
            f"""\n""",
        )
        cargo_file = File(self.data['root'] + '/build-aux/', 'cargo.sh', text_cargo)
        self.files.append(cargo_file)

        text_cargo_toml = (
            f"[package]\n",
            f"name = \"rust-example\"\n",
            f"version = \"0.1.0\"\n",
            f"edition = \"2018\"\n",
            f"\n",
            f"[dependencies.gtk]\n",
            f"version = \"0.8.1\"\n",
            f"features = [\"v3_24\"]\n",
            f"\n",
            f"[dependencies.gdk]\n",
            f"version = \"0.12.1\"\n",
            f"features = [\"v3_24\"]\n",
            f"\n",
            f"[dependencies.gio]\n",
            f"version = \"0.8.1\"\n",
            f"features = [\"v2_60\"]\n",
            f"\n",
            f"[dependencies.glib]\n",
            f"version = \"0.9.2\"\n",
            f"features = [\"v2_60\"]\n",
            f"\n",
            f"[dependencies.gettext-rs]\n",
            f"version = \"0.4.4\"\n",
            f"features = [\"gettext-system\"]\n",
        )
        cargo_toml_file = File(self.data['root'], 'Cargo.toml', text_cargo_toml)
        self.files.append(cargo_toml_file)

    def populate_data_dir(self, data):
        path = self.data['root'] + 'data/'

        meson_data_file = self.create_data_meson_file(path, data)
        self.files.append(meson_data_file)

        appdata_file = self.create_appdata_file(path, data)
        self.files.append(appdata_file)

        desktop_file = self.create_desktop_file(path, data)
        self.files.append(desktop_file)

        gschema_file = self.create_gschema_file(path, data)
        self.files.append(gschema_file)

    def populate_po_dir(self, data):
        path = self.data['root'] + 'po/'

        linguas_file = self.create_po_linguas_file(path)
        self.files.append(linguas_file)

        po_meson_file = self.create_po_meson_file(path, data)
        self.files.append(po_meson_file)

        potfiles_file = self.create_po_potfiles_file(path, data)
        self.files.append(potfiles_file)

    def populate_src_dir(self, data):
        path = self.data['root'] + 'src/'

        if self.data['is_gui']:
            text_config = (
                f"pub static PKGDATADIR: &str = @pkgdatadir@;\n",
                f"pub static VERSION: &str = @VERSION@;\n",
                f"pub static LOCALEDIR: &str = @localedir@;\n",
            )
            config_src_file = File(path, 'config.rs.in', text_config)
            self.files.append(config_src_file)

        if self.data['is_gui']:
            text_main = (
                f"use gettextrs::*;\n",
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
                f"    bindtextdomain(\"{data['project_name']}\", config::LOCALEDIR);\n",
                f"    textdomain(\"{data['project_name']}\");\n",
                f"\n",
                f"    let res = gio::Resource::load(config::PKGDATADIR.to_owned() + \"/{data['project_name']}.gresource\")\n",
                f"        .expect(\"Could not load resources\");\n",
                f"    gio::resources_register(&res);\n",
                f"\n",
                f"    let app = gtk::Application::new(Some(\"{data['project_id']}\"), Default::default()).unwrap();\n",
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
                f"}}\n",
            )
        else:
            text_main = (
                f"fn main() {{\n",
                f"    println!(\"Hello World\");\n",
                f"}}\n"
            )
        main_src_file = File(path, 'main.rs', text_main)
        self.files.append(main_src_file)

        if self.data['is_gui']:
            text_meson = (
                f"pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())\n",
                f"gnome = import('gnome')\n",
                f"\n",
                f"gnome.compile_resources('{data['project_name']}',\n",
                f"  '{data['project_name_underscore']}.gresource.xml',\n",
                f"  gresource_bundle: true,\n",
                f"  install: true,\n",
                f"  install_dir: pkgdatadir,\n",
                f")\n",
                f"\n",
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
                f"\n",
                f"cargo_script = find_program(join_paths(meson.source_root(), 'build-aux/cargo.sh'))\n",
                f"cargo_release = custom_target(\n",
                f"  'cargo-build',\n",
                f"  build_by_default: true,\n",
                f"  input: sources,\n",
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
                f")\n",
            )
            meson_src_file = File(path, 'meson.build', text_meson)
            self.files.append(meson_src_file)

        if self.data['is_gui']:
            gresource_file = self.create_gresource_file(path, data)
            self.files.append(gresource_file)

            text_window = (
                f"use gtk::prelude::*;\n",
                f"\n",
                f"pub struct Window {{\n",
                f"    pub widget: gtk::ApplicationWindow,\n",
                f"}}\n",
                f"\n",
                f"impl Window {{\n",
                f"    pub fn new() -> Self {{\n",
                f"        let builder = gtk::Builder::new_from_resource(\"/{data['project_id'].replace('.', '/')}/window.ui\");\n",
                f"        let widget: gtk::ApplicationWindow = builder\n",
                f"            .get_object(\"window\")\n",
                f"            .expect(\"Failed to find the window object\");\n",
                f"\n",
                f"        Self {{ widget }}\n",
                f"    }}\n",
                f"}}\n",
            )
            window_file = File(path, 'window.rs', text_window)
            self.files.append(window_file)

            text_window_ui = (
                f"""<?xml version="1.0" encoding="UTF-8"?>\n""",
                f"""<interface>\n""",
                f"""  <requires lib="gtk+" version="3.24"/>\n""",
                f"""    <object class="GtkApplicationWindow" id="window">\n""",
                f"""      <property name="default-width">600</property>\n""",
                f"""      <property name="default-height">300</property>\n""",
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
                f"""    </object>\n""",
                f"""  </interface>\n""",
            )
            window_file_ui = File(path, 'window.ui', text_window_ui)
            self.files.append(window_file_ui)

