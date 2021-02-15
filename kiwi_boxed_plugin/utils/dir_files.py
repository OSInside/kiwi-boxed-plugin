# Copyright (c) 2020 SUSE Software Solutions Germany GmbH.  All rights reserved.
#
# This file is part of kiwi-boxed-build.
#
# kiwi-boxed-build is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kiwi-boxed-build is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kiwi-boxed-build.  If not, see <http://www.gnu.org/licenses/>
#
import os
from tempfile import NamedTemporaryFile

from kiwi.path import Path
from kiwi.command import Command


class DirFiles:
    """
    **Directory File Manager**

    Connects registered files to a named temporary file
    and updates the contents of the given directory with
    the registered files in an atomic operation
    """
    def __init__(self, dirname):
        self.dirname = dirname
        self.dirname_tmp = ''.join(
            [self.dirname, '.tmp']
        )
        self.dirname_wipe = ''.join(
            [self.dirname, '.wipe']
        )
        self.collection = {}
        Path.wipe(self.dirname_tmp)

    def register(self, filename):
        """
        Register given filename to be handled as a temporary
        file. The given filename gets overwritten with the
        contents of the temporary file on call of the commit
        method

        :param string filename: file path name

        :return: name of created temporary file

        :rtype: string
        """
        tmpfile = NamedTemporaryFile()
        self.collection[os.path.basename(filename)] = tmpfile.name
        return tmpfile.name

    def commit(self):
        """
        Update instance directory with contents of registered files

        Use an atomic operation that prepares a tmp directory with
        all registered files and move it to the directory given at
        instance creation time. Please note the operation is not
        fully atomic as it uses two move commands in a series
        """
        Path.create(self.dirname_tmp)
        bash_command = [
            'cp', '-a', f'{self.dirname}/*', self.dirname_tmp
        ]
        Command.run(
            ['bash', '-c', ' '.join(bash_command)], raise_on_error=False
        )
        for origin, tmpname in list(self.collection.items()):
            Command.run(
                ['mv', tmpname, os.sep.join([self.dirname_tmp, origin])]
            )
        Command.run(
            ['mv', self.dirname, self.dirname_wipe]
        )
        Command.run(
            ['mv', self.dirname_tmp, self.dirname]
        )
        Command.run(
            ['rm', '-rf', self.dirname_wipe]
        )
