# file.py
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

from .project_starter_constants import constants
import os

class File:

    def __init__(self, path, filename, text):
        self.path = path if path.endswith('/') else path + '/'
        self.filename = filename
        self.text = text

    def create(path, filename, text):
        with open(path + filename, 'a') as f:
            if text:
                f.writelines(text)
            else:
                # TODO maybe there is another way to create an empty file?
                f.close()  