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
from gi.repository import GLib
from .project_starter_constants import constants

class GnomeExtensionTemplate():

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

    def __init__(self, ext_name, ext_uuid, ext_description, is_git):
        self.ext_name = ext_name
        self.ext_uuid = ext_uuid
        self.ext_description = ext_description
        self.is_git = is_git
        self.path = GLib.get_home_dir() + '/.local/share/gnome-shell/extensions/' + self.ext_uuid

    def start(self):
        self.create_basic_structure(self.ext_name, self.ext_description, self.ext_uuid, self.path)
        if self.is_git:
            os.chdir(self.path)
            os.system('git init')

    def create_basic_structure(self, e_name, e_descr, e_uuid, path):

        os.makedirs(self.path)

        with open(path + '/extension.js', 'a') as file_extension_js:
            file_extension_js.write("/* extension.js\n")
            file_extension_js.write(" *\n")
            file_extension_js.write(" * This program is free software: you can redistribute it and/or modify\n")
            file_extension_js.write(" * it under the terms of the GNU General Public License as published by\n")
            file_extension_js.write(" * the Free Software Foundation, either version 2 of the License, or\n")
            file_extension_js.write(" * (at your option) any later version.\n")
            file_extension_js.write(" *\n")
            file_extension_js.write(" * This program is distributed in the hope that it will be useful,\n")
            file_extension_js.write(" * but WITHOUT ANY WARRANTY; without even the implied warranty of\n")
            file_extension_js.write(" * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n")
            file_extension_js.write(" * GNU General Public License for more details.\n")
            file_extension_js.write(" *\n")
            file_extension_js.write(" * You should have received a copy of the GNU General Public License\n")
            file_extension_js.write(" * along with this program.  If not, see <http://www.gnu.org/licenses/>.\n")
            file_extension_js.write(" *\n")
            file_extension_js.write(" * SPDX-License-Identifier: GPL-2.0-or-later\n")
            file_extension_js.write(" */\n")
            file_extension_js.write("\n")
            file_extension_js.write("/* exported init */\n")
            file_extension_js.write("\n")
            file_extension_js.write("class Extension {\n")
            file_extension_js.write("    constructor() {\n")
            file_extension_js.write("    }\n")
            file_extension_js.write("\n")
            file_extension_js.write("    enable() {\n")
            file_extension_js.write("    }\n")
            file_extension_js.write("\n")
            file_extension_js.write("    disable() {\n")
            file_extension_js.write("    }\n")
            file_extension_js.write("}\n")
            file_extension_js.write("\n")
            file_extension_js.write("function init() {\n")
            file_extension_js.write("    return new Extension();\n")
            file_extension_js.write("}\n")

        with open(path + '/metadata.json', 'a') as file_metadata_json:
            file_metadata_json.write("{\n")
            file_metadata_json.write("  \"name\": \"%s\",\n" % e_name)
            file_metadata_json.write("  \"description\": \"%s\",\n" % e_descr)
            file_metadata_json.write("  \"uuid\": \"%s\",\n" % e_uuid)
            file_metadata_json.write("  \"shell-version\": [\n")
            file_metadata_json.write("    \"%s\"\n" % constants['SHELL_VERSION'])
            file_metadata_json.write("  ]\n")
            file_metadata_json.write("}\n")

        with open(path + '/stylesheet.css', 'a') as file_css:
            file_css.write("/* Add your custom extension styling here */\n")
            file_css.write("\n")

