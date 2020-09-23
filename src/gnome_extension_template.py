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
from gi.repository import GLib
from .file import File
from .template import Template
from .project_starter_constants import constants

class GnomeExtensionTemplate(Template):

    def __init__(self, ext_name, ext_uuid, ext_description, is_git):
        self.data = {}
        self.data['ext_name'] = ext_name
        self.data['ext_uuid'] = ext_uuid
        self.data['ext_description'] = ext_description
        self.data['is_git'] = is_git
        self.data['root'] = os.path.join(GLib.get_home_dir(), constants['GNOME_EXTENSION_PATH'], self.data['ext_uuid'])
        self.files = []

    def start(self):
        self.populate_root_dir(self.data)
        if self.data['is_git']:
            os.chdir(self.data['root'])
            os.system('git init')

        for f in self.files:
            f.create()
    
    def create_folders(self, root):
        os.makedirs(root)

    def populate_root_dir(self, data):
        self.create_folders(data['root'])
        path = data['root']

        text_file_extension_js = (
            f"/* extension.js\n",
            f" *\n",
            f" * This program is free software: you can redistribute it and/or modify\n",
            f" * it under the terms of the GNU General Public License as published by\n",
            f" * the Free Software Foundation, either version 2 of the License, or\n",
            f" * (at your option) any later version.\n",
            f" *\n",
            f" * This program is distributed in the hope that it will be useful,\n",
            f" * but WITHOUT ANY WARRANTY; without even the implied warranty of\n",
            f" * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n",
            f" * GNU General Public License for more details.\n",
            f" *\n",
            f" * You should have received a copy of the GNU General Public License\n",
            f" * along with this program.  If not, see <http://www.gnu.org/licenses/>.\n",
            f" *\n",
            f" * SPDX-License-Identifier: GPL-2.0-or-later\n",
            f" */\n",
            f"\n",
            f"/* exported init */\n",
            f"\n",
            f"class Extension {{\n",
            f"    constructor() {{\n",
            f"    }}\n",
            f"\n",
            f"    enable() {{\n",
            f"    }}\n",
            f"\n",
            f"    disable() {{\n",
            f"    }}\n",
            f"}}\n",
            f"\n",
            f"function init() {{\n",
            f"    return new Extension();\n",
            f"}}\n",
        )
        extension_js_file = File(path, '/extension.js', text_file_extension_js)
        self.files.append(extension_js_file)

        file_metadata_json_text = (
            f"{{\n",
            f"  \"name\": \"{data['ext_name']}\",\n",
            f"  \"description\": \"{data['ext_description']}\",\n",
            f"  \"uuid\": \"{data['ext_uuid']}\",\n",
            f"  \"shell-version\": [\n",
            f"    \"{constants['SHELL_VERSION']}\"\n",
            f"  ]\n",
            f"}}\n",
        )
        file_metadata_json = File(path, '/metadata.json', file_metadata_json_text)
        self.files.append(file_metadata_json)

        file_css_text = (
            f"/* Add your custom extension styling here */\n",
            f"\n",
        )
        file_css = File(path, '/stylesheet.css', file_css_text)
        self.files.append(file_css)

