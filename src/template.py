# template.py
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
from .common_files import CommonFile
from .helpers import *


class Template:
    folders = []

    def __init__(self, root):
        self.root = root if root.endswith('/') else root + '/'

    def populate_data_folder(self, project_id, project_name):
        self.CommonFile.create_data_meson_file(self.path, self.project_full_name)
        self.CommonFile.create_appdata_file(self.path, self.project_full_name, self.license)
        self.CommonFile.create_desktop_file(self.path, self.project_full_name, self.project_name, self.project_id)
        self.CommonFile.create_gschema_file(self.path, self.project_full_name, self.project_name, p_path)

    def prepare_manifest(self, filename):
        pass

    def create_folders(self, folders):
        if len(folders) == 0:
            print('Folder creation error: empty list')
            return

        for f in folders:
            directory = self.root + f
            if not os.path.exists(directory):
                os.mkdir(directory)
            else:
                print(f'Folder with name {f} already exists!')
                
