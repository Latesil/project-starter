# c_template.py
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

class CTemplate():

    gpl_text = """ * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
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
        p_id_underscore = p_id.replace('.', '_').lower()

        os.makedirs(path + '/build-aux/meson')
        os.makedirs(path + '/' + 'data')
        os.makedirs(path + '/' + 'po')
        os.makedirs(path + '/' + 'src')

        with open(path + '/' + "COPYING", 'a') as file_license:
            if self.license == 'GPL 3':
                from .gpl import Gpl
                license = Gpl('3')
            file_license.write(license.get_text())

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
            file_meson_build.write("project('%s', 'c',\n" % p_name)
            file_meson_build.write("          version: '0.1.0',\n")
            file_meson_build.write("    meson_version: '>= 0.50.0',\n")
            file_meson_build.write("  default_options: [ 'warning_level=2',\n")
            file_meson_build.write("                     'c_std=gnu11',\n")
            file_meson_build.write("                   ],\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("i18n = import('i18n')\n")
            file_meson_build.write("\n")
            file_meson_build.write("config_h = configuration_data()\n")
            file_meson_build.write("config_h.set_quoted('PACKAGE_VERSION', meson.project_version())\n")
            file_meson_build.write("config_h.set_quoted('GETTEXT_PACKAGE', '%s')\n" % p_name)
            file_meson_build.write("config_h.set_quoted('LOCALEDIR', join_paths(get_option('prefix'), get_option('localedir')))\n")
            file_meson_build.write("configure_file(\n")
            file_meson_build.write("  output: '%s-config.h',\n" % p_id_underscore)
            file_meson_build.write("  configuration: config_h,\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("add_project_arguments([\n")
            file_meson_build.write("  '-I' + meson.build_root(),\n")
            file_meson_build.write("], language: 'c')\n")
            file_meson_build.write("\n")
            file_meson_build.write("subdir('data')\n")
            file_meson_build.write("subdir('src')\n")
            file_meson_build.write("subdir('po')\n")
            file_meson_build.write("\n")
            file_meson_build.write("meson.add_install_script('build-aux/meson/postinstall.py')\n")

        with open(path + '/' + p_id + ".json", 'a') as file_main_json:
            file_main_json.write("{\n")
            file_main_json.write("    \"app-id\" : \"%s\",\n" % p_id)
            file_main_json.write("    \"runtime\" : \"org.gnome.Platform\",\n")
            file_main_json.write("    \"runtime-version\" : \"3.34\",\n")
            file_main_json.write("    \"sdk\" : \"org.gnome.Sdk\",\n")
            file_main_json.write("    \"command\" : \"%s\",\n" % p_name)
            file_main_json.write("    \"finish-args\" : [\n")
            file_main_json.write("        \"--share=network\",\n")
            file_main_json.write("        \"--share=ipc\",\n")
            file_main_json.write("        \"--socket=fallback-x11\",\n")
            file_main_json.write("        \"--socket=wayland\"\n")
            file_main_json.write("    ],\n")
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
            file_main_json.write("            ]\n")
            file_main_json.write("        }\n")
            file_main_json.write("    ]\n")
            file_main_json.write("}\n")

    def populate_data_folder(self, p_id, p_name):
        p_path = p_id.replace('.', '/')

        with open(self.path + '/data/meson.build', 'a') as file_meson_build:
            file_meson_build.write("desktop_file = i18n.merge_file(\n")
            file_meson_build.write("  input: '%s.desktop.in',\n" % p_id)
            file_meson_build.write("  output: '%s.desktop',\n" % p_id)
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
            file_meson_build.write("  input: '%s.appdata.xml.in',\n" % p_id)
            file_meson_build.write("  output: '%s.appdata.xml',\n" % p_id)
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
            file_meson_build.write("install_data('%s.gschema.xml',\n" % p_id)
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

        with open(self.path + '/data/' + p_id + '.appdata.xml.in', 'a') as file_app_data:
            file_app_data.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_app_data.write("<component type=\"desktop\">\n")
            file_app_data.write("\t<id>%s.desktop</id>\n" % p_id)
            file_app_data.write("\t<metadata_license>CC0-1.0</metadata_license>\n")
            if self.license == 'GPL 3':
                file_app_data.write("\t<project_license>GPL-3.0-or-later</project_license>\n")
            file_app_data.write("\t<description>\n")
            file_app_data.write("\t</description>\n")
            file_app_data.write("</component>\n")
            file_app_data.write("\n")

        with open(self.path + '/data/' + p_id + '.desktop.in', 'a') as file_desktop:
            file_desktop.write("[Desktop Entry]\n")
            file_desktop.write("Name=%s\n" % p_name)
            file_desktop.write("Exec=%s\n" % p_name)
            if self.is_gui:
                file_desktop.write("Terminal=false\n")
            file_desktop.write("Type=Application\n")
            file_desktop.write("Categories=GTK;\n")
            file_desktop.write("StartupNotify=true\n")

        with open(self.path + '/data/' + p_id + '.gschema.xml', 'a') as file_gschema:
            file_gschema.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_gschema.write("<schemalist gettext-domain=\"%s\">\n" % p_name)
            file_gschema.write("\t<schema id=\"%s\" path=\"/%s/\">\n" % (p_id, p_path))
            file_gschema.write("\t</schema>\n")
            file_gschema.write("</schemalist>\n")
            file_gschema.write("\n")

    def populate_po_dir(self, p_id, p_name):
        p_id_underscore = p_id.replace('.', '_').lower()

        #TODO maybe there is another way to create an empty file?
        with open(self.path + '/po/LINGUAS', 'a') as file_linguas:
            file_linguas.close()

        with open(self.path + '/po/meson.build', 'a') as file_meson_build:
            file_meson_build.write("i18n.gettext('%s', preset: 'glib')\n" % p_name)
            file_meson_build.write("\n")

        with open(self.path + '/po/POTFILES', 'a') as file_potfiles:
            file_potfiles.write("data/%s.desktop.in\n" % p_id)
            file_potfiles.write("data/%s.appdata.xml.in\n" % p_id)
            file_potfiles.write("data/%s.gschema.xml\n" % p_id)
            file_potfiles.write("src/%s-window.ui\n" % p_id_underscore)
            file_potfiles.write("src/main.c\n")
            file_potfiles.write("src/%s-window.c\n" % p_id_underscore)
            file_potfiles.write("\n")

    def populate_src_dir(self, p_id, p_name):
        p_id_underscore = p_id.replace('.', '_').lower()
        p_id_reverse = p_id.replace('.', '/') + '/' + p_name + '/'
        p_id_reverse_short = p_id.replace('.', '/')
        window_name = "".join(w.capitalize() for w in p_name.split('-'))

        with open(self.path + '/src/main.c', 'a') as file_main_c:
            file_main_c.write("/* main.c\n")
            file_main_c.write(" *\n")
            file_main_c.write(" * Copyright 2020\n")
            file_main_c.write("\n")
            file_main_c.write(self.gpl_text)
            file_main_c.write("\n")
            file_main_c.write("#include <glib/gi18n.h>\n")
            file_main_c.write("\n")
            file_main_c.write("#include \"%s-config.h\"\n" % p_id_underscore)
            file_main_c.write("#include \"%s-window.h\"\n" % p_id_underscore)
            file_main_c.write("\n")
            file_main_c.write("static void\n")
            file_main_c.write("on_activate (GtkApplication *app)\n")
            file_main_c.write("{\n")
            file_main_c.write("	GtkWindow *window;\n")
            file_main_c.write("\n")
            file_main_c.write("	/* It's good practice to check your parameters at the beginning of the\n")
            file_main_c.write("	 * function. It helps catch errors early and in development instead of\n")
            file_main_c.write("	 * by your users.\n")
            file_main_c.write("	 */\n")
            file_main_c.write("\n")
            file_main_c.write("	g_assert (GTK_IS_APPLICATION (app));\n")
            file_main_c.write("\n")
            file_main_c.write("	/* Get the current window or create one if necessary. */\n")
            file_main_c.write("	window = gtk_application_get_active_window (app);\n")
            file_main_c.write("	if (window == NULL)\n")
            file_main_c.write("		window = g_object_new (%s_TYPE_WINDOW,\n" % p_id_underscore.upper())
            file_main_c.write("		                       \"application\", app,\n")
            file_main_c.write("		                       \"default-width\", 600,\n")
            file_main_c.write("		                       \"default-height\", 300,\n")
            file_main_c.write("		                       NULL);\n")
            file_main_c.write("\n")
            file_main_c.write("	/* Ask the window manager/compositor to present the window. */\n")
            file_main_c.write("	gtk_window_present (window);\n")
            file_main_c.write("}\n")
            file_main_c.write("\n")
            file_main_c.write("int\n")
            file_main_c.write("main (int   argc,\n")
            file_main_c.write("      char *argv[])\n")
            file_main_c.write("{\n")
            file_main_c.write("	g_autoptr(GtkApplication) app = NULL;\n")
            file_main_c.write("	int ret;\n")
            file_main_c.write("\n")
            file_main_c.write("	/* Set up gettext translations */\n")
            file_main_c.write("	bindtextdomain (GETTEXT_PACKAGE, LOCALEDIR);\n")
            file_main_c.write("	bind_textdomain_codeset (GETTEXT_PACKAGE, \"UTF-8\");\n")
            file_main_c.write("	textdomain (GETTEXT_PACKAGE);\n")
            file_main_c.write("\n")
            file_main_c.write("	/*\n")
            file_main_c.write("	 * Create a new GtkApplication. The application manages our main loop,\n")
            file_main_c.write("	 * application windows, integration with the window manager/compositor, and\n")
            file_main_c.write("	 * desktop features such as file opening and single-instance applications.\n")
            file_main_c.write("	 */\n")
            file_main_c.write("	app = gtk_application_new (\"%s\", G_APPLICATION_FLAGS_NONE);\n" % p_id)
            file_main_c.write("\n")
            file_main_c.write("	/*\n")
            file_main_c.write("	 * We connect to the activate signal to create a window when the application\n")
            file_main_c.write("	 * has been lauched. Additionally, this signal notifies us when the user\n")
            file_main_c.write("	 * tries to launch a \"second instance\" of the application. When they try\n")
            file_main_c.write("	 * to do that, we'll just present any existing window.\n")
            file_main_c.write("	 *\n")
            file_main_c.write("	 * Because we can't pass a pointer to any function type, we have to cast\n")
            file_main_c.write("	 * our \"on_activate\" function to a GCallback.\n")
            file_main_c.write("	 */\n")
            file_main_c.write("	g_signal_connect (app, \"activate\", G_CALLBACK (on_activate), NULL);\n")
            file_main_c.write("\n")
            file_main_c.write("	/*\n")
            file_main_c.write("	 * Run the application. This function will block until the applicaiton\n")
            file_main_c.write("	 * exits. Upon return, we have our exit code to return to the shell. (This\n")
            file_main_c.write("	 * is the code you see when you do `echo $?` after running a command in a\n")
            file_main_c.write("	 * terminal.\n")
            file_main_c.write("	 *\n")
            file_main_c.write("	 * Since GtkApplication inherits from GApplication, we use the parent class\n")
            file_main_c.write("	 * method \"run\". But we need to cast, which is what the \"G_APPLICATION()\"\n")
            file_main_c.write("	 * macro does.\n")
            file_main_c.write("	 */\n")
            file_main_c.write("	ret = g_application_run (G_APPLICATION (app), argc, argv);\n")
            file_main_c.write("\n")
            file_main_c.write("	return ret;\n")
            file_main_c.write("}\n")

        with open(self.path + '/src/meson.build', 'a') as file_meson_build:
            file_meson_build.write("%s_sources = [\n" % p_id_underscore)
            file_meson_build.write("  'main.c',\n")
            file_meson_build.write("  '%s-window.c',\n" % p_id_underscore)
            file_meson_build.write("]\n")
            file_meson_build.write("\n")
            file_meson_build.write("%s_deps = [\n" % p_id_underscore)
            file_meson_build.write("  dependency('gio-2.0', version: '>= 2.50'),\n")
            file_meson_build.write("  dependency('gtk+-3.0', version: '>= 3.22'),\n")
            file_meson_build.write("]\n")
            file_meson_build.write("\n")
            file_meson_build.write("gnome = import('gnome')\n")
            file_meson_build.write("\n")
            file_meson_build.write("%s_sources += gnome.compile_resources('%s-resources',\n" % (p_id_underscore, p_id_underscore))
            file_meson_build.write("  '%s.gresource.xml',\n" % p_id_underscore)
            file_meson_build.write("  c_name: '%s'\n" % p_id_underscore)
            file_meson_build.write(")\n")
            file_meson_build.write("\n")
            file_meson_build.write("executable('%s', %s_sources,\n" % (p_name, p_id_underscore))
            file_meson_build.write("  dependencies: %s_deps,\n" % p_id_underscore)
            file_meson_build.write("  install: true,\n")
            file_meson_build.write(")\n")
            file_meson_build.write("\n")

        with open(self.path + '/src/' + p_id_underscore + '.gresource.xml', 'a') as file_gresource:
            file_gresource.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file_gresource.write("<gresources>\n")
            file_gresource.write("  <gresource prefix=\"/%s\">\n" % p_id_reverse_short)
            file_gresource.write("    <file>%s-window.ui</file>\n" % p_id_underscore)
            file_gresource.write("  </gresource>\n")
            file_gresource.write("</gresources>\n")
            file_gresource.write("\n")

        with open(self.path + '/src/' + p_id_underscore + '-window.c', 'a') as file_window_c:
            file_window_c.write("/* main.c\n")
            file_window_c.write(" *\n")
            file_window_c.write(" * Copyright 2020\n")
            file_window_c.write(self.gpl_text)
            file_window_c.write("\n")
            file_window_c.write("#include \"%s-config.h\"\n" % p_id_underscore)
            file_window_c.write("#include \"%s-window.h\"\n" % p_id_underscore)
            file_window_c.write("\n")
            file_window_c.write("struct _%sWindow\n" % window_name) #CGuiExample
            file_window_c.write("{\n")
            file_window_c.write("  GtkApplicationWindow  parent_instance;\n")
            file_window_c.write("\n")
            file_window_c.write("  /* Template widgets */\n")
            file_window_c.write("  GtkHeaderBar        *header_bar;\n")
            file_window_c.write("  GtkLabel            *label;\n")
            file_window_c.write("};\n")
            file_window_c.write("\n")
            file_window_c.write("G_DEFINE_TYPE (%sWindow, %s_window, GTK_TYPE_APPLICATION_WINDOW)\n" % (window_name, p_id_underscore))
            file_window_c.write("\n")
            file_window_c.write("static void\n")
            file_window_c.write("%s_window_class_init (%sWindowClass *klass)\n" % (p_id_underscore, window_name))
            file_window_c.write("{\n")
            file_window_c.write("  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);\n")
            file_window_c.write("\n")
            file_window_c.write("  gtk_widget_class_set_template_from_resource (widget_class, \"/%s/%s-window.ui\");\n" % (p_id_reverse_short, p_id_underscore))
            file_window_c.write("  gtk_widget_class_bind_template_child (widget_class, %sWindow, header_bar);\n" % window_name)
            file_window_c.write("  gtk_widget_class_bind_template_child (widget_class, %sWindow, label);\n" % window_name)
            file_window_c.write("}\n")
            file_window_c.write("\n")
            file_window_c.write("static void\n")
            file_window_c.write("%s_window_init (%sWindow *self)\n" % (p_id_underscore, window_name))
            file_window_c.write("{\n")
            file_window_c.write("  gtk_widget_init_template (GTK_WIDGET (self));\n")
            file_window_c.write("}\n")

        with open(self.path + '/src/' + p_id_underscore + '-window.ui', 'a') as file_window_ui:
            file_window_ui.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
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

        with open(self.path + '/src/' + p_id_underscore + '-window.h', 'a') as file_window_h:
            file_window_h.write("/* c_gui_example-window.h\n")
            file_window_h.write(" *\n")
            file_window_h.write(" * Copyright 2020\n")
            file_window_h.write(self.gpl_text)
            file_window_h.write("\n")
            file_window_h.write("#pragma once\n")
            file_window_h.write("\n")
            file_window_h.write("#include <gtk/gtk.h>\n")
            file_window_h.write("\n")
            file_window_h.write("G_BEGIN_DECLS\n")
            file_window_h.write("\n")
            file_window_h.write("#define %s_TYPE_WINDOW (%s_window_get_type())\n" % (p_id_underscore.upper(), p_id_underscore))
            file_window_h.write("\n")
            file_window_h.write("G_DECLARE_FINAL_TYPE (%sWindow, %s_window, %s, WINDOW, GtkApplicationWindow)\n" % (window_name, p_id_underscore, p_id_underscore.upper()))
            file_window_h.write("\n")
            file_window_h.write("G_END_DECLS\n")
