# helpers.py
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

def create_folders(folders):
    if len(folders) == 0:
        print('Folder creation error: empty list')
        return
    
    for f in folders:
        dir = self.root + f
        if not os.path.exists(dir):
            os.mkdir(dir)
        else:
            print('Folder with name {f} already exists!')

def create_file(path, filename, text, empty=False):
    with open(path  + filename, 'a') as f:
        if not empty:
            f.writelines(text)
        else:
            # TODO maybe there is another way to create an empty file?
            f.close()