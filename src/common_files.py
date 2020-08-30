# common_files.py
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

class File:

    def __init__(self):
        self.gpl = """# This program is free software: you can redistribute it and/or modify
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

    def get_gpl(self):
        return self.gpl

    """def create_desktop_file(self, path, p_id, p_name, p_full_name):
        with open(path + '/data/' + p_full_name + '.desktop.in', 'a') as file_desktop:
            file_desktop.write("[Desktop Entry]\n")
            file_desktop.write("Name=%s\n" % p_name)
            file_desktop.write("Exec=%s\n" % p_name)
            file_desktop.write("Terminal=false\n")
            file_desktop.write("Type=Application\n")
            file_desktop.write("Categories=GTK;\n")
            file_desktop.write("StartupNotify=true\n")
            file_desktop.write("Icon=%s" % p_id)"""

    def create_meson_postinstall_file(self, path):
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
