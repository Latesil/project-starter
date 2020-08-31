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
from .project_starter_constants import constants
from .common_files import File

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

        with open(path + '/' + "meson.build", 'a') as file_meson_build:
            file_meson_build.write("project('%s',\n" % p_name)
            file_meson_build.write("          version: '0.1.0',\n")
            file_meson_build.write("    meson_version: '>= %s',\n" % constants['MESON_VERSION'])
            file_meson_build.write("  default_options: [ 'warning_level=2',\n")
            file_meson_build.write("                   ],\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            if self.is_gui:
                file_meson_build.write("i18n = import('i18n')\n")
            file_meson_build.write("\n")
            file_meson_build.write("\n")
            if self.is_gui:
                file_meson_build.write("subdir('data')\n")
            file_meson_build.write("subdir('src')\n")
            if self.is_gui:
                file_meson_build.write("subdir('po')\n")
            file_meson_build.write("\n")
            if self.is_gui:
                file_meson_build.write("meson.add_install_script('build-aux/meson/postinstall.py')\n")

        with open(path + '/build-aux/cargo.sh', 'a') as file_cargo_shell_script:
            file_cargo_shell_script.write("#!/bin/sh\n")
            file_cargo_shell_script.write("\n")
            file_cargo_shell_script.write("export MESON_BUILD_ROOT=\"$1\"\n")
            file_cargo_shell_script.write("export MESON_SOURCE_ROOT=\"$2\"\n")
            file_cargo_shell_script.write("export CARGO_TARGET_DIR=\"$MESON_BUILD_ROOT\"/target\n")
            file_cargo_shell_script.write("export CARGO_HOME=\"$CARGO_TARGET_DIR\"/cargo-home\n")
            file_cargo_shell_script.write("export OUTPUT=\"$3\"\n")
            file_cargo_shell_script.write("export BUILDTYPE=\"$4\"\n")
            file_cargo_shell_script.write("export APP_BIN=\"$5\"\n")
            file_cargo_shell_script.write("\n")
            file_cargo_shell_script.write("\n")
            file_cargo_shell_script.write("if [[ $BUILDTYPE = \"release\" ]]\n")
            file_cargo_shell_script.write("then\n")
            file_cargo_shell_script.write("    echo \"RELEASE MODE\"\n")
            file_cargo_shell_script.write("    cargo build --manifest-path \\\n")
            file_cargo_shell_script.write("        \"$MESON_SOURCE_ROOT\"/Cargo.toml --release && \\\n")
            file_cargo_shell_script.write("        cp \"$CARGO_TARGET_DIR\"/release/\"$APP_BIN\" \"$OUTPUT\"\n")
            file_cargo_shell_script.write("else\n")
            file_cargo_shell_script.write("    echo \"DEBUG MODE\"\n")
            file_cargo_shell_script.write("    cargo build --manifest-path \\\n")
            file_cargo_shell_script.write("        \"$MESON_SOURCE_ROOT\"/Cargo.toml --verbose && \\\n")
            file_cargo_shell_script.write("        cp \"$CARGO_TARGET_DIR\"/debug/\"$APP_BIN\" \"$OUTPUT\"\n")
            file_cargo_shell_script.write("fi\n")
            file_cargo_shell_script.write("\n")

        st = os.stat(path + '/build-aux/cargo.sh')
        os.chmod(path + '/build-aux/cargo.sh', st.st_mode | stat.S_IEXEC)

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
            with open(self.path + '/src/config.rs.in', 'a') as file_config_rs:
                file_config_rs.write("pub static PKGDATADIR: &str = @pkgdatadir@;\n")
                file_config_rs.write("pub static VERSION: &str = @VERSION@;\n")
                file_config_rs.write("pub static LOCALEDIR: &str = @localedir@;\n")

        with open(self.path + '/src/main.rs', 'a') as file_rs_main:
            if self.is_gui:
                file_rs_main.write("use gettextrs::*;\n")
                file_rs_main.write("use gio::prelude::*;\n")
                file_rs_main.write("use gtk::prelude::*;\n")
                file_rs_main.write("\n")
                file_rs_main.write("mod config;\n")
                file_rs_main.write("mod window;\n")
                file_rs_main.write("use crate::window::Window;\n")
                file_rs_main.write("\n")
                file_rs_main.write("fn main() {\n")
                file_rs_main.write("    gtk::init().unwrap_or_else(|_| panic!(\"Failed to initialize GTK.\"));\n")
                file_rs_main.write("\n")
                file_rs_main.write("    setlocale(LocaleCategory::LcAll, \"\");\n")
                file_rs_main.write("    bindtextdomain(\"%s\", config::LOCALEDIR);\n" % p_name)
                file_rs_main.write("    textdomain(\"%s\");\n" % p_name)
                file_rs_main.write("\n")
                file_rs_main.write("    let res = gio::Resource::load(config::PKGDATADIR.to_owned() + \"/%s.gresource\")\n" % p_name)
                file_rs_main.write("        .expect(\"Could not load resources\");\n")
                file_rs_main.write("    gio::resources_register(&res);\n")
                file_rs_main.write("\n")
                file_rs_main.write("    let app = gtk::Application::new(Some(\"%s\"), Default::default()).unwrap();\n" % p_id)
                file_rs_main.write("    app.connect_activate(move |app| {\n")
                file_rs_main.write("        let window = Window::new();\n")
                file_rs_main.write("\n")
                file_rs_main.write("        window.widget.set_application(Some(app));\n")
                file_rs_main.write("        app.add_window(&window.widget);\n")
                file_rs_main.write("        window.widget.present();\n")
                file_rs_main.write("    });\n")
                file_rs_main.write("\n")
                file_rs_main.write("    let ret = app.run(&std::env::args().collect::<Vec<_>>());\n")
                file_rs_main.write("    std::process::exit(ret);\n")
                file_rs_main.write("}\n")
            else:
                file_rs_main.write("fn main() {\n")
                file_rs_main.write("    println!(\"Hello World\");\n")
                file_rs_main.write("}\n")

        with open(self.path + '/src/meson.build', 'a') as file_meson_build:
            if self.is_cli:
                file_meson_build.write("pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())\n")
                file_meson_build.write("gnome = import('gnome')\n")
                file_meson_build.write("\n")
                file_meson_build.write("gnome.compile_resources('%s',\n" % p_name)
                file_meson_build.write("  '%s.gresource.xml',\n" % p_name_underscore)
                file_meson_build.write("  gresource_bundle: true,\n")
                file_meson_build.write("  install: true,\n")
                file_meson_build.write("  install_dir: pkgdatadir,\n")
                file_meson_build.write(")\n")
                file_meson_build.write("\n")
                file_meson_build.write("conf = configuration_data()\n")
                file_meson_build.write("conf.set_quoted('VERSION', meson.project_version())\n")
                file_meson_build.write("conf.set_quoted('localedir', join_paths(get_option('prefix'), get_option('localedir')))\n")
                file_meson_build.write("conf.set_quoted('pkgdatadir', pkgdatadir)\n")
                file_meson_build.write("\n")
                file_meson_build.write("configure_file(\n")
                file_meson_build.write("  input: 'config.rs.in',\n")
                file_meson_build.write("  output: 'config.rs',\n")
                file_meson_build.write("  configuration: conf,\n")
                file_meson_build.write(")\n")
                file_meson_build.write("\n")
                file_meson_build.write("# Copy the config.rs output to the source directory.\n")
                file_meson_build.write("run_command(\n")
                file_meson_build.write("  'cp',\n")
                file_meson_build.write("  join_paths(meson.build_root(), 'src', 'config.rs'),\n")
                file_meson_build.write("  join_paths(meson.source_root(), 'src', 'config.rs'),\n")
                file_meson_build.write("  check: true\n")
                file_meson_build.write(")\n")
                file_meson_build.write("\n")
            if self.is_cli:
                file_meson_build.write("sources = files(\n")
                file_meson_build.write("  'config.rs',\n")
                file_meson_build.write("  'main.rs',\n")
                file_meson_build.write("  'window.rs',\n")
                file_meson_build.write(")\n")
            else:
                file_meson_build.write("%s_sources = [\n" % p_name_underscore)
                file_meson_build.write("  'main.rs',\n")
                file_meson_build.write("]\n")
            file_meson_build.write("\n")
            if not self.is_cli:
                file_meson_build.write("%s_deps = [\n" % p_name_underscore)
                file_meson_build.write("]\n")
            file_meson_build.write("cargo_script = find_program(join_paths(meson.source_root(), 'build-aux/cargo.sh'))\n")
            file_meson_build.write("cargo_release = custom_target(\n")
            file_meson_build.write("  'cargo-build',\n")
            file_meson_build.write("  build_by_default: true,\n")
            if self.is_gui:
                file_meson_build.write("  input: sources,\n")
            else:
                file_meson_build.write("  input: %s_sources,\n" % p_name_underscore)
            file_meson_build.write("  output: meson.project_name(),\n")
            file_meson_build.write("  console: true,\n")
            file_meson_build.write("  install: true,\n")
            file_meson_build.write("  install_dir: get_option('bindir'),\n")
            file_meson_build.write("  command: [\n")
            file_meson_build.write("    cargo_script,\n")
            file_meson_build.write("    meson.build_root(),\n")
            file_meson_build.write("    meson.source_root(),\n")
            file_meson_build.write("    '@OUTPUT@',\n")
            file_meson_build.write("    get_option('buildtype'),\n")
            file_meson_build.write("    meson.project_name(),\n")
            file_meson_build.write("  ]\n")
            file_meson_build.write(")\n")

        if self.is_gui:
            files = ['window.ui']
            self.file.create_gresource_file(path, p_name_underscore, p_id_reverse, files)

            with open(self.path + '/src/window.rs', 'a') as file_py_window:
                file_py_window.write("use gtk::prelude::*;\n")
                file_py_window.write("\n")
                file_py_window.write("pub struct Window {\n")
                file_py_window.write("    pub widget: gtk::ApplicationWindow,\n")
                file_py_window.write("}\n")
                file_py_window.write("\n")
                file_py_window.write("impl Window {\n")
                file_py_window.write("    pub fn new() -> Self {\n")
                file_py_window.write("        let builder = gtk::Builder::new_from_resource(\"/%s/window.ui\");\n" % p_id_reverse_short)
                file_py_window.write("        let widget: gtk::ApplicationWindow = builder\n")
                file_py_window.write("            .get_object(\"window\")\n")
                file_py_window.write("            .expect(\"Failed to find the window object\");\n")
                file_py_window.write("\n")
                file_py_window.write("        Self { widget }\n")
                file_py_window.write("    }\n")
                file_py_window.write("}\n")

            with open(self.path + '/src/window.ui', 'a') as file_window_ui:
                file_window_ui.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                file_window_ui.write("<interface>\n")
                file_window_ui.write("  <requires lib=\"gtk+\" version=\"3.24\"/>\n")
                file_window_ui.write("    <object class=\"GtkApplicationWindow\" id=\"window\">\n")
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
                file_window_ui.write("    </object>\n")
                file_window_ui.write("  </interface>\n")
