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
from .project_starter_constants import constants
from .common_files import File
from .helpers import *

class CTemplate():

    def __init__(self, is_gui, project_id, project_name, path, is_git, license):
        self.is_gui = is_gui
        self.project_id = project_id
        self.project_name = project_name
        self.path = path
        self.is_git = is_git
        self.lang = 'c'
        self.license = license
        self.file = File()
        self.gpl_text = self.file.get_gpl()

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
        p_full_name = p_id + '.' + p_name
        p_id_underscore = p_id.replace('.', '_').lower()

        if self.is_gui:
            os.makedirs(path + '/build-aux/meson')
            os.makedirs(path + '/' + 'data')
            os.makedirs(path + '/' + 'po')
        os.makedirs(path + '/' + 'src')

        self.file.create_copying_file(path, self.license)

        if self.is_gui:
            self.file.create_meson_postinstall_file(path)

        with open(path + '/' + "meson.build", 'a') as file_meson_build:
            text = (f"project('{p_name}', 'c',\n",
                    f"          version: '0.1.0',\n",
                    f"    meson_version: '>= {constants['MESON_VERSION']}',\n",
                    f"  default_options: [ 'warning_level=2',\n",
                    f"                     'c_std=gnu11',\n",
                    f"                   ],\n",
                    f")\n",
                    f"\n",
                    f"i18n = import('i18n')\n",
                    f"\n",
                    f"config_h = configuration_data()\n",
                    f"config_h.set_quoted('PACKAGE_VERSION', meson.project_version())\n",
                    f"config_h.set_quoted('GETTEXT_PACKAGE', '{p_name}')\n",
                    f"config_h.set_quoted('LOCALEDIR', join_paths(get_option('prefix'), get_option('localedir')))\n",
                    f"configure_file(\n",
                    f"  output: '{p_id_underscore}-config.h',\n",
                    f"  configuration: config_h,\n",
                    f")\n",
                    f"\n",
                    f"add_project_arguments([\n",
                    f"  '-I' + meson.build_root(),\n",
                    f"], language: 'c')\n",
                    f"\n",)

            if self.is_gui:
                text += (f"subdir('data')\n",)

            text += (f"subdir('src')\n",)

            if self.is_gui:
                text = (f"subdir('po')\n",)
            
            text += (f"\n",)

            if self.is_gui:
                text += (f"meson.add_install_script('build-aux/meson/postinstall.py')\n",)

        if self.is_gui:
            self.file.create_manifest_file(path, p_id, p_name, self.lang)

    def populate_data_folder(self, p_id, p_name):
        p_path = p_id.replace('.', '/')

        self.file.create_data_meson_file(self.path, p_id)
        self.file.create_appdata_file(self.path, p_id, self.license)
        self.file.create_desktop_file(self.path, p_full_name, p_name, p_id, gui=self.gui)
        self.file.create_gschema_file(self.path, p_full_name, p_name, p_path)

    def populate_po_dir(self, p_id, p_name):
        p_id_underscore = p_id.replace('.', '_').lower()
        files = [p_id_underscore + '-window.ui', 'main.c', p_id_underscore + '-window.c']
        self.file.create_po_linguas_file(self.path)
        self.file.create_po_meson_file(self.path, p_name)
        self.file.create_po_potfiles_file(self.path, p_id, files)

    def populate_src_dir(self, p_id, p_name):
        p_id_underscore = p_id.replace('.', '_').lower()
        p_id_reverse = p_id.replace('.', '/') + '/' + p_name + '/'
        p_id_reverse_short = p_id.replace('.', '/')
        window_name = "".join(w.capitalize() for w in p_name.split('-'))

        if self.is_gui:
            text_main = (f"/* main.c\n",
                        f" *\n",
                        f" * Copyright 2020\n",
                        f"\n",
                        self.gpl_text,
                        f"\n",
                        f"#include <glib/gi18n.h>\n",
                        f"\n",
                        f"#include \"{p_id_underscore}-config.h\"\n",
                        f"#include \"{p_id_underscore}-window.h\"\n",
                        f"\n",
                        f"static void\n",
                        f"on_activate (GtkApplication *app)\n",
                        f"{{\n",
                        f"	GtkWindow *window;\n",
                        f"\n",
                        f"	/* It's good practice to check your parameters at the beginning of the\n",
                        f"	 * function. It helps catch errors early and in development instead of\n",
                        f"	 * by your users.\n",
                        f"	 */\n",
                        f"\n",
                        f"	g_assert (GTK_IS_APPLICATION (app));\n",
                        f"\n",
                        f"	/* Get the current window or create one if necessary. */\n",
                        f"	window = gtk_application_get_active_window (app);\n",
                        f"	if (window == NULL)\n",
                        f"		window = g_object_new ({p_id_underscore.upper()}_TYPE_WINDOW,\n",
                        f"		                       \"application\", app,\n",
                        f"		                       \"default-width\", 600,\n",
                        f"		                       \"default-height\", 300,\n",
                        f"		                       NULL);\n",
                        f"\n",
                        f"	/* Ask the window manager/compositor to present the window. */\n",
                        f"	gtk_window_present (window);\n",
                        f"}}\n",
                        f"\n",
                        f"int\n",
                        f"main (int   argc,\n",
                        f"      char *argv[])\n",
                        f"{{\n",
                        f"	g_autoptr(GtkApplication) app = NULL;\n",
                        f"	int ret;\n",
                        f"\n",
                        f"	/* Set up gettext translations */\n",
                        f"	bindtextdomain (GETTEXT_PACKAGE, LOCALEDIR);\n",
                        f"	bind_textdomain_codeset (GETTEXT_PACKAGE, \"UTF-8\");\n",
                        f"	textdomain (GETTEXT_PACKAGE);\n",
                        f"\n",
                        f"	/*\n",
                        f"	 * Create a new GtkApplication. The application manages our main loop,\n",
                        f"	 * application windows, integration with the window manager/compositor, and\n",
                        f"	 * desktop features such as file opening and single-instance applications.\n",
                        f"	 */\n",
                        f"	app = gtk_application_new (\"{p_id}\", G_APPLICATION_FLAGS_NONE);\n",
                        f"\n",
                        f"	/*\n",
                        f"	 * We connect to the activate signal to create a window when the application\n",
                        f"	 * has been lauched. Additionally, this signal notifies us when the user\n",
                        f"	 * tries to launch a \"second instance\" of the application. When they try\n",
                        f"	 * to do that, we'll just present any existing window.\n",
                        f"	 *\n",
                        f"	 * Because we can't pass a pointer to any function type, we have to cast\n",
                        f"	 * our \"on_activate\" function to a GCallback.\n",
                        f"	 */\n",
                        f"	g_signal_connect (app, \"activate\", G_CALLBACK (on_activate), NULL);\n",
                        f"\n",
                        f"	/*\n",
                        f"	 * Run the application. This function will block until the applicaiton\n",
                        f"	 * exits. Upon return, we have our exit code to return to the shell. (This\n",
                        f"	 * is the code you see when you do `echo $?` after running a command in a\n",
                        f"	 * terminal.\n",
                        f"	 *\n",
                        f"	 * Since GtkApplication inherits from GApplication, we use the parent class\n",
                        f"	 * method \"run\". But we need to cast, which is what the \"G_APPLICATION()\"\n",
                        f"	 * macro does.\n",
                        f"	 */\n",
                        f"	ret = g_application_run (G_APPLICATION (app), argc, argv);\n",
                        f"\n",
                        f"	return ret;\n",
                        f"}}\n",)
        else:
            text_main = (f"/* main.c\n",
                        f" *\n",
                        f" * Copyright 2020\n",
                        f"\n",
                        self.gpl_text,
                        f"\n",
                        f"#include \"{p_id_underscore}-config.h\"\n",
                        f"\n",
                        f"#include <glib.h>\n",
                        f"#include <stdlib.h>\n",
                        f"\n",
                        f"gint\n",
                        f"main (gint   argc,\n",
                        f"      gchar *argv[])\n",
                        f"{{\n",
                        f"  g_autoptr(GOptionContext) context = NULL;\n",
                        f"  g_autoptr(GError) error = NULL;\n",
                        f"  gboolean version = FALSE;\n",
                        f"  GOptionEntry main_entries[] = {{\n",
                        f"    {{ \"version\", 0, 0, G_OPTION_ARG_NONE, &version, \"Show program version\" }},\n",
                        f"    {{ NULL }}\n",
                        f"  }};\n",
                        f"\n",
                        f"  context = g_option_context_new (\"- my command line tool\");\n",
                        f"  g_option_context_add_main_entries (context, main_entries, NULL);\n",
                        f"\n",
                        f"  if (!g_option_context_parse (context, &argc, &argv, &error))\n",
                        f"    {{\n",
                        f"      g_printerr (\"%s\n\", error->message);\n",
                        f"      return EXIT_FAILURE;\n",
                        f"    }}\n",
                        f"\n",
                        f"  if (version)\n",
                        f"    {{\n",
                        f"      g_printerr (\"%s\n\", PACKAGE_VERSION);\n",
                        f"      return EXIT_SUCCESS;\n",
                        f"    }}\n",
                        f"\n",
                        f"  return EXIT_SUCCESS;\n",
                        f"}}\n",)

        create_file(path + '/src/', 'main.c', text_main)
        
        text_meson = (f"{p_id_underscore}_sources = [\n",
                        f"  'main.c',\n",)

        if self.is_gui:
            text_meson += (f"  '{p_id_underscore}-window.c',\n",)

        text_meson += (f"]\n",
                        f"\n",
                        f"{p_id_underscore}_deps = [\n",
                        f"  dependency('gio-2.0', version: '>= 2.50'),\n",)

        if self.is_gui:
            text_meson += (f"  dependency('gtk+-3.0', version: '>= 3.22'),\n",)

        text_meson += (f"]\n",
                        f"\n",
                        f"gnome = import('gnome')\n",
                        f"\n",
                        f"{p_id_underscore}_sources += gnome.compile_resources('{p_id_underscore}-resources',\n",
                        f"  '{p_id_underscore}.gresource.xml',\n",
                        f"  c_name: '{p_id_underscore}'\n",
                        f")\n",
                        f"\n",
                        f"executable('{p_name}', {p_name_underscore}_sources,\n",
                        f"  dependencies: {p_id_underscore}_deps,\n",
                        f"  install: true,\n",
                        f")\n",
                        f"\n",)
        
        create_file(path + '/src/', 'meson.build', text_meson)

        if self.is_gui:
            files = ['window.ui']
            self.file.create_gresource_file(path, p_name_underscore, p_id_reverse, files)

        if self.is_gui:
            text_window = (f"/* main.c\n",
                           f" *\n",
                           f" * Copyright 2020\n",
                           self.gpl_text
                           f"\n",
                           f"#include \"{p_id_underscore}-config.h\"\n",
                           f"#include \"{p_id_underscore}-window.h\"\n",
                           f"\n",
                           f"struct _{window_name}Window\n", #CGuiExample
                           f"{{\n",
                           f"  GtkApplicationWindow  parent_instance;\n",
                           f"\n",
                           f"  /* Template widgets */\n",
                           f"  GtkHeaderBar        *header_bar;\n",
                           f"  GtkLabel            *label;\n",
                           f"}};\n",
                           f"\n",
                           f"G_DEFINE_TYPE ({window_name}Window, {p_id_underscore}_window, GTK_TYPE_APPLICATION_WINDOW)\n",
                           f"\n",
                           f"static void\n",
                           f"{p_id_underscore}_window_class_init ({window_name}WindowClass *klass)\n",
                           f"{{\n",
                           f"  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);\n",
                           f"\n",
                           f"  gtk_widget_class_set_template_from_resource (widget_class, \"/{p_id_reverse_short}/{p_id_underscore}-window.ui\");\n",
                           f"  gtk_widget_class_bind_template_child (widget_class, {window_name}Window, header_bar);\n",
                           f"  gtk_widget_class_bind_template_child (widget_class, {window_name}Window, label);\n",
                           f"}}\n",
                           f"\n",
                           f"static void\n",
                           f"{p_id_underscore}_window_init ({window_name}Window *self)\n",
                           f"{{\n",
                           f"  gtk_widget_init_template (GTK_WIDGET (self));\n",
                           f"}}\n",)
            
            create_file(path + '/src/', p_id_underscore + '-window.c', text_window)

            self.file.create_window_ui_file(self, path, window_name)
            text_window_h = (f"/* c_gui_example-window.h\n",
                            f" *\n",
                            f" * Copyright 2020\n",
                            self.gpl_text,
                            f"\n",
                            f"#pragma once\n",
                            f"\n",
                            f"#include <gtk/gtk.h>\n",
                            f"\n",
                            f"G_BEGIN_DECLS\n",
                            f"\n",
                            f"#define {p_id_underscore.upper()}_TYPE_WINDOW ({p_id_underscore}_window_get_type())\n",
                            f"\n",
                            f"G_DECLARE_FINAL_TYPE ({window_name}Window, {p_id_underscore}_window, {p_id_underscore.upper()}, WINDOW, GtkApplicationWindow)\n",
                            f"\n",
                            f"G_END_DECLS\n",)

            create_file(path + '/src/', p_id_underscore + '-window.h', text_window_h)
