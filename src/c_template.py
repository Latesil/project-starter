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

import os
import datetime
from .project_starter_constants import constants
from .file import File
from .template import Template

class CTemplate(Template):

    def __init__(self, is_gui, project_id, project_name, path, is_git, license):
        self.data = {}
        self.data['is_gui'] = is_gui
        self.data['project_id'] = project_id
        self.data['project_name'] = project_name
        self.data['root'] = path
        self.data['is_git'] = is_git
        self.data['project_license'] = license
        self.files = []
        self.data['lang'] = 'c'
        self.data['year'] = datetime.datetime.now().year

        #####################################################

        self.data['project_name_unserscore'] = self.data['project_name'].replace('-','_').lower()
        self.data['window_name'] = "".join(w.capitalize() for w in self.data['project_name'].split('-'))
        self.data['ui_filename'] = self.data['project_name_unserscore'] + '-window.ui'

        self.data['po_files'] = [self.data['project_name_unserscore'] + '-window.ui', 
                        'main.c', 
                        self.data['project_name_unserscore'] + '-window.c']
        self.data['gresource_files'] = [self.data['project_name_unserscore'] + '-window.ui']

        #####################################################

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

        if self.data['is_git']:
            os.chdir(self.data['root'])
            os.system('git init')

        self.create_files(self.files, executable=self.data['project_name'] + '.in')

    def populate_root_dir(self, data):
        path = os.path.join(data['root'], 'build-aux/meson')

        copying_file = self.create_copying_file(data['root'], data)
        self.files.append(copying_file)

        if self.data['is_gui']:
            post_install_file = self.create_meson_postinstall_file(path)
            self.files.append(post_install_file)

        text = (
            f"project('{data['project_name']}', 'c',\n",
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
            f"config_h.set_quoted('GETTEXT_PACKAGE', '{data['project_name']}')\n",
            f"config_h.set_quoted('LOCALEDIR', join_paths(get_option('prefix'), get_option('localedir')))\n",
            f"configure_file(\n",
            f"  output: '{data['project_name_unserscore']}-config.h',\n",
            f"  configuration: config_h,\n",
            f")\n",
            f"\n",
            f"add_project_arguments([\n",
            f"  '-I' + meson.build_root(),\n",
            f"], language: 'c')\n",
            f"\n",
        )

        if data['is_gui']:
            text += (f"subdir('data')\n",)

        text += (f"subdir('src')\n",)

        if data['is_gui']:
            text += (f"subdir('po')\n",)
        
        text += (f"\n",)

        if data['is_gui']:
            text += (f"meson.add_install_script('build-aux/meson/postinstall.py')\n",)

        main_meson_file = File(data['root'], 'meson.build', text)
        self.files.append(main_meson_file)

        if data['is_gui']:
            manifest_file = self.create_manifest_file(self.data['root'], data)
            self.files.append(manifest_file)

    def populate_data_dir(self, data):
        path = os.path.join(data['root'], 'data')

        meson_data_file = self.create_data_meson_file(path, data)
        self.files.append(meson_data_file)

        appdata_file = self.create_appdata_file(path, data)
        self.files.append(appdata_file)

        desktop_file = self.create_desktop_file(path, data, gui=data['is_gui'])
        self.files.append(desktop_file)

        gschema_file = self.create_gschema_file(path, data)
        self.files.append(gschema_file)

    def populate_src_dir(self, data):
        path = os.path.join(data['root'], 'src')

        if data['is_gui']:
            text_main = (
                f"/* main.c\n",
                f" *\n",
                f" * Copyright {data['year']}\n",
                f"\n",
                f"{self.get_gpl(data['lang'])}",
                f" */\n",
                f"\n",
                f"#include <glib/gi18n.h>\n",
                f"\n",
                f"#include \"{data['project_name_unserscore']}-config.h\"\n",
                f"#include \"{data['project_name_unserscore']}-window.h\"\n",
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
                f"		window = g_object_new ({data['project_name_unserscore'].upper()}_TYPE_WINDOW,\n",
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
                f"	app = gtk_application_new (\"{data['project_id']}\", G_APPLICATION_FLAGS_NONE);\n",
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
                f"}}\n",
            )
        else:
            text_main = (
                f"/* main.c\n",
                f" *\n",
                f" * Copyright {data['year']}\n",
                f"\n",
                f"{self.get_gpl(data['lang'])}",
                f" */\n",
                f"\n",
                f"#include \"{data['project_name_unserscore']}-config.h\"\n",
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
                f"}}\n",
            )

        main_c_file = File(path, 'main.c', text_main)
        self.files.append(main_c_file)
        
        text_meson = (
            f"{data['project_name_unserscore']}_sources = [\n",
            f"  'main.c',\n",
        )

        if data['is_gui']:
            text_meson += (f"  '{data['project_name_unserscore']}-window.c',\n",)

        text_meson += (
            f"]\n",
            f"\n",
            f"{data['project_name_unserscore']}_deps = [\n",
            f"  dependency('gio-2.0', version: '>= 2.50'),\n",
        )

        if data['is_gui']:
            text_meson += (f"  dependency('gtk+-3.0', version: '>= 3.22'),\n",)

        text_meson += (
            f"]\n",
            f"\n",
            f"gnome = import('gnome')\n",
            f"\n",
            f"{data['project_name_unserscore']}_sources += gnome.compile_resources('{data['project_name_unserscore']}-resources',\n",
            f"  '{data['project_name_unserscore']}.gresource.xml',\n",
            f"  c_name: '{data['project_name_unserscore']}'\n",
            f")\n",
            f"\n",
            f"executable('{data['project_name']}', {data['project_name_unserscore']}_sources,\n",
            f"  dependencies: {data['project_name_unserscore']}_deps,\n",
            f"  install: true,\n",
            f")\n",
            f"\n",
        )
        
        meson_src_file = File(path, 'meson.build', text_meson)
        self.files.append(meson_src_file)

        if data['is_gui']:
            gresource_file = self.create_gresource_file(path, data)
            self.files.append(gresource_file)

        if data['is_gui']:
            text_window = (
                f"/* main.c\n",
                f" *\n",
                f" * Copyright {data['year']}\n",
                f"{self.get_gpl(data['lang'])}",
                f" */\n",
                f"\n",
                f"#include \"{data['project_name_unserscore']}-config.h\"\n",
                f"#include \"{data['project_name_unserscore']}-window.h\"\n",
                f"\n",
                f"struct _{data['window_name']}Window\n", #CGuiExample
                f"{{\n",
                f"  GtkApplicationWindow  parent_instance;\n",
                f"\n",
                f"  /* Template widgets */\n",
                f"  GtkHeaderBar        *header_bar;\n",
                f"  GtkLabel            *label;\n",
                f"}};\n",
                f"\n",
                f"G_DEFINE_TYPE ({data['window_name']}Window, {data['project_name_unserscore']}_window, GTK_TYPE_APPLICATION_WINDOW)\n",
                f"\n",
                f"static void\n",
                f"{data['project_name_unserscore']}_window_class_init ({data['window_name']}WindowClass *klass)\n",
                f"{{\n",
                f"  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);\n",
                f"\n",
                f"  gtk_widget_class_set_template_from_resource (widget_class, \"/{data['project_id'].replace('.', '/')}/{data['project_name_unserscore']}-window.ui\");\n",
                f"  gtk_widget_class_bind_template_child (widget_class, {data['window_name']}Window, header_bar);\n",
                f"  gtk_widget_class_bind_template_child (widget_class, {data['window_name']}Window, label);\n",
                f"}}\n",
                f"\n",
                f"static void\n",
                f"{data['project_name_unserscore']}_window_init ({data['window_name']}Window *self)\n",
                f"{{\n",
                f"  gtk_widget_init_template (GTK_WIDGET (self));\n",
                f"}}\n",
            )
            
            window_file = File(path, data['project_name_unserscore'] + '-window.c', text_window)
            self.files.append(window_file)

            window_ui_file = self.create_window_ui_file(path, data)
            self.files.append(window_ui_file)

            text_window_h = (
                f"/* c_gui_example-window.h\n",
                f" *\n",
                f" * Copyright {data['year']}\n",
                f"{self.get_gpl(data['lang'])}",
                f" */\n",
                f"\n",
                f"#pragma once\n",
                f"\n",
                f"#include <gtk/gtk.h>\n",
                f"\n",
                f"G_BEGIN_DECLS\n",
                f"\n",
                f"#define {data['project_name_unserscore'].upper()}_TYPE_WINDOW ({data['project_name_unserscore']}_window_get_type())\n",
                f"\n",
                f"G_DECLARE_FINAL_TYPE ({data['window_name']}Window, {data['project_name_unserscore']}_window, {data['project_name_unserscore'].upper()}, WINDOW, GtkApplicationWindow)\n",
                f"\n",
                f"G_END_DECLS\n",
            )

            window_h_file = File(path, data['project_name_unserscore'] + '-window.h', text_window_h)
            self.files.append(window_h_file)
