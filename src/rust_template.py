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
            file_cargo_shell_script.write("    cargo build --manifest-path \\n")
            file_cargo_shell_script.write("        \"$MESON_SOURCE_ROOT\"/Cargo.toml --verbose && \\\n")
            file_cargo_shell_script.write("        cp \"$CARGO_TARGET_DIR\"/debug/\"$APP_BIN\" \"$OUTPUT\"\n")
            file_cargo_shell_script.write("fi\n")
            file_cargo_shell_script.write("\n")

        with open(path + '/' + "cargo.toml", 'a') as file_cargo_toml:
            file_cargo_toml.write("[package]\n")
            file_cargo_toml.write("name = \"%s\"\n" % p_name)
            file_cargo_toml.write("version = \"0.1.0\"\n")
            file_cargo_toml.write("edition = \"2018\"\n")
            file_cargo_toml.write("\n")
            file_cargo_toml.write("[dependencies.gtk]\n")
            file_cargo_toml.write("version = \"0.8.1\"\n")
            file_cargo_toml.write("features = [\"v3_24\"]\n")
            file_cargo_toml.write("\n")
            file_cargo_toml.write("[dependencies.gdk]\n")
            file_cargo_toml.write("version = \"0.12.1\"\n")
            file_cargo_toml.write("features = [\"v3_24\"]\n")
            file_cargo_toml.write("\n")
            file_cargo_toml.write("[dependencies.gio]\n")
            file_cargo_toml.write("version = \"0.8.1\"\n")
            file_cargo_toml.write("features = [\"v2_60\"]\n")
            file_cargo_toml.write("\n")
            file_cargo_toml.write("[dependencies.glib]\n")
            file_cargo_toml.write("version = \"0.9.2\"\n")
            file_cargo_toml.write("features = [\"v2_60\"]\n")
            file_cargo_toml.write("\n")
            file_cargo_toml.write("[dependencies.gettext-rs]\n")
            file_cargo_toml.write("version = \"0.4.4\"\n")
            file_cargo_toml.write("features = [\"gettext-system\"]\n")

    def populate_data_folder(self, p_id, p_name):
        p_id_reverse = p_id.replace('.', '/') + '/' + p_name + '/'
        p_full_name = p_id + '.' + p_name
        p_path = p_id.replace('.', '/')

        with open(self.path + '/data/meson.build', 'a') as file_meson_build:
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
            file_meson_build.write("  install_dir: join_paths(get_option('datadir'), 'appdata')\n")
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

        with open(self.path + '/data/' + p_full_name + '.appdata.xml.in', 'a') as file_app_data:
            file_app_data.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_app_data.write("<component type=\"desktop\">\n")
            file_app_data.write("\t<id>%s.desktop</id>\n" % p_full_name)
            file_app_data.write("\t<metadata_license>CC0-1.0</metadata_license>\n")
            if self.license == 'GPL 3':
                file_app_data.write("\t<project_license>GPL-3.0-or-later</project_license>\n")
            file_app_data.write("\t<description>\n")
            file_app_data.write("\t</description>\n")
            file_app_data.write("</component>\n")
            file_app_data.write("\n")

        with open(self.path + '/data/' + p_full_name + '.desktop.in', 'a') as file_desktop:
            file_desktop.write("[Desktop Entry]\n")
            file_desktop.write("Name=%s\n" % p_name)
            file_desktop.write("Exec=%s\n" % p_name)
            if self.is_gui:
                file_desktop.write("Terminal=false\n")
            file_desktop.write("Type=Application\n")
            file_desktop.write("Categories=GTK;\n")
            file_desktop.write("StartupNotify=true\n")

        with open(self.path + '/data/' + p_full_name + '.gschema.xml', 'a') as file_gschema:
            file_gschema.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_gschema.write("<schemalist gettext-domain=\"%s\">" % p_name)
            file_gschema.write("\t<schema id=\"%s\" path=\"/%s/\">" % (p_full_name, p_path))
            file_gschema.write("\t</schema>\n")
            file_gschema.write("</schemalist>\n")
            file_gschema.write("\n")

    def populate_po_dir(self, p_id, p_name):
        p_full_name = p_id + '.' + p_name

        #TODO maybe there is another way to create an empty file?
        with open(self.path + '/po/LINGUAS', 'a') as file_linguas:
            file_linguas.close()

        with open(self.path + '/po/meson.build', 'a') as file_meson_build:
            file_meson_build.write("i18n.gettext('%s', preset: 'glib')\n" % p_name)
            file_meson_build.write("\n")

        with open(self.path + '/po/POTFILES', 'a') as file_potfiles:
            file_potfiles.write("data/%s.desktop.in\n" % p_full_name)
            file_potfiles.write("data/%s.appdata.xml.in\n" % p_full_name)
            file_potfiles.write("data/%s.gschema.xml.in\n" % p_full_name)
            file_potfiles.write("src/window.ui\n")
            file_potfiles.write("\n")

    def populate_src_dir(self, p_id, p_name):
        p_name_underscore = p_name.replace('-', '_')
        p_id_reverse = p_id.replace('.', '/') + '/' + p_name + '/'
        p_id_reverse_short = p_id.replace('.', '/')

        with open(self.path + '/src/config.rs.in', 'a') as file_config_rs:
            file_config_rs.write("pub static PKGDATADIR: &str = @pkgdatadir@;\n")
            file_config_rs.write("pub static VERSION: &str = @VERSION@;\n")
            file_config_rs.write("pub static LOCALEDIR: &str = @localedir@;\n")

        with open(self.path + '/src/main.rs', 'a') as file_py_main:
            file_py_main.write("use gettextrs::*;\n")
            file_py_main.write("use gio::prelude::*;\n")
            file_py_main.write("use gtk::prelude::*;\n")
            file_py_main.write("#\n")
            file_py_main.write("mod config;\n")
            file_py_main.write("mod window;\n")
            file_py_main.write("use crate::window::Window;\n")
            file_py_main.write("\n")
            file_py_main.write("fn main() {\n")
            file_py_main.write("    gtk::init().unwrap_or_else(|_| panic!(\"Failed to initialize GTK.\"));)\n")
            file_py_main.write("\n")
            file_py_main.write("    setlocale(LocaleCategory::LcAll, \"\");\n")
            file_py_main.write("    bindtextdomain(\"%s\", config::LOCALEDIR);\n" % p_name)
            file_py_main.write("    textdomain(\"%s\");\n" % p_name)
            file_py_main.write("\n")
            file_py_main.write("    let res = gio::Resource::load(config::PKGDATADIR.to_owned() + \"/%s.gresource\")\n" % p_name)
            file_py_main.write("        .expect(\"Could not load resources\");\n")
            file_py_main.write("    gio::resources_register(&res);\n")
            file_py_main.write("\n")
            file_py_main.write("    let app = gtk::Application::new(Some(\"%s\"), Default::default()).unwrap();\n" % p_id)
            file_py_main.write("    app.connect_activate(move |app| {\n")
            file_py_main.write("        let window = Window::new();\n")
            file_py_main.write("\n")
            file_py_main.write("        window.widget.set_application(Some(app));\n")
            file_py_main.write("        app.add_window(&window.widget);\n")
            file_py_main.write("        window.widget.present();\n")
            file_py_main.write("    });\n")
            file_py_main.write("\n")
            file_py_main.write("    let ret = app.run(&std::env::args().collect::<Vec<_>>());\n")
            file_py_main.write("    std::process::exit(ret);\n")
            file_py_main.write("}\n")

        with open(self.path + '/src/meson.build', 'a') as file_meson_build:
            file_meson_build.write("pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())\n")
            file_meson_build.write("moduledir = join_paths(pkgdatadir, '%s')\n" % p_name_underscore)
            file_meson_build.write("gnome = import('gnome')\n")
            file_meson_build.write("\n")
            file_meson_build.write("gnome.compile_resources('%s',\n" % p_name)
            file_meson_build.write("  '%s.gresource.xml',\n" % p_name_underscore)
            file_meson_build.write("  gresource_bundle: true,\n")
            file_meson_build.write("  install: true,\n")
            file_meson_build.write("  install_dir: pkgdatadir,\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("desktop_utils = find_program('desktop-file-validate', required: false)\n")
            file_meson_build.write("if desktop_utils.found()\n")
            file_meson_build.write("  test('Validate desktop file', desktop_utils,\n")
            file_meson_build.write("    args: [desktop_file]\n")
            file_meson_build.write("  )\n")
            file_meson_build.write("endif\n")
            file_meson_build.write("\n")
            file_meson_build.write("python = import('python')\n")
            file_meson_build.write("\n")
            file_meson_build.write("conf = configuration_data()\n")
            file_meson_build.write("conf.set('PYTHON', python.find_installation('python3').path())\n")
            file_meson_build.write("conf.set('VERSION', meson.project_version())\n")
            file_meson_build.write("conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))\n")
            file_meson_build.write("conf.set('pkgdatadir', pkgdatadir)\n")
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
            file_meson_build.write("  check: true\n"
            file_meson_build.write(")\n")
            file_meson_build.write("sources = files(\n")
            file_meson_build.write("  'config.rs',\n")
            file_meson_build.write("  'main.rs',\n")
            file_meson_build.write("  'window.rs',\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("cargo_script = find_program(join_paths(meson.source_root(), 'build-aux/cargo.sh'))\n")
            file_meson_build.write("cargo_release = custom_target(\n")
            file_meson_build.write("  'cargo-build',\n")
            file_meson_build.write("  build_by_default: true,\n")
            file_meson_build.write("  input: sources,\n")
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

        with open(self.path + '/src/' + p_name_underscore + '.gresource.xml', 'a') as file_gresource:
            file_gresource.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_gresource.write("<gresources>\n")
            file_gresource.write("  <gresource prefix=\"/%s\">\n" % p_id_reverse_short)
            file_gresource.write("    <file>window.ui</file>\n")
            file_gresource.write("  </gresource>\n")
            file_gresource.write("</gresources>\n")
            file_gresource.write("\n")

        with open(self.path + '/src/window.py', 'a') as file_py_window:
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
            file_window_ui.write("\n")
            file_window_ui.write("<interface>\n")
            file_window_ui.write("  <requires lib=\"gtk+\" version=\"3.24\"/>\n")
            file_window_ui.write("    <template class=\"%sWindow\" parent=\"GtkApplicationWindow\">\n" % class_name)
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
