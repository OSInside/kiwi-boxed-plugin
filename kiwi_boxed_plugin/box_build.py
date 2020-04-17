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
import logging
import platform
from kiwi.path import Path

from kiwi_boxed_plugin.box_download import BoxDownload
from kiwi_boxed_plugin.defaults import Defaults

log = logging.getLogger('kiwi')


class BoxBuild:
    """
    **Implements boxbuild command**

    Implements an interface to run a kiwi build box using
    the KVM virtualization platform

    :param string boxname: name of the box from kiwi_boxed_plugin.yml
    :param string arch: arch name for box
    """
    def __init__(self, boxname, ram=None, arch=None):
        self.ram = ram
        self.arch = arch or platform.machine()
        self.box = BoxDownload(boxname, arch)

    def run(self, kiwi_build_command, update_check=True, keep_open=False):
        """
        Start the build process in a box VM using KVM

        :param list kiwi_build_command:
            kiwi build command line Example:

            .. code:: python

                [
                    '--type', 'vmx', 'system', 'build',
                    '--description', 'some/description',
                    '--target-dir', 'some/target-dir'
                ]

        :param bool update_check: check for box updates True|False
        :param bool keep_open: keep VM running True|False
        """
        self.kiwi_build_command = kiwi_build_command
        desc = self._pop_arg_param(
            '--description'
        )
        target_dir = self._pop_arg_param(
            '--target-dir'
        )
        Path.create(target_dir)
        vm_setup = self.box.fetch(update_check)
        vm_append = [
            vm_setup.append,
            'kiwi=\\"{0}\\"'.format(' '.join(self.kiwi_build_command))
        ]
        if keep_open:
            vm_append.append('kiwi-no-halt')
        vm_run = [
            'qemu-system-{0}'.format(self.arch),
            '-m', format(self.ram or vm_setup.ram)
        ] + Defaults.get_qemu_generic_setup() + [
            '-kernel', vm_setup.kernel,
            '-append', '"{0}"'.format(' '.join(vm_append))
        ] + Defaults.get_qemu_storage_setup(vm_setup.system) + \
            Defaults.get_qemu_network_setup() + \
            Defaults.get_qemu_console_setup() + \
            Defaults.get_qemu_shared_path_setup(0, desc, 'kiwidescription') + \
            Defaults.get_qemu_shared_path_setup(1, target_dir, 'kiwibundle')
        if vm_setup.initrd:
            vm_run += ['-initrd', vm_setup.initrd]
        os.environ['TMPDIR'] = Defaults.get_local_box_cache_dir()
        log.debug(
            'Set TMPDIR: {0}'.format(os.environ['TMPDIR'])
        )
        log.debug(
            'Calling Qemu: {0}'.format(vm_run)
        )
        os.system(
            ' '.join(vm_run)
        )
        log.info(
            'Box build done. Find build log at: {0}'.format(
                os.sep.join([target_dir, 'result.log'])
            )
        )

    def _pop_arg_param(self, arg):
        arg_index = self.kiwi_build_command.index(arg)
        if arg_index:
            value = self.kiwi_build_command[arg_index + 1]
            del self.kiwi_build_command[arg_index + 1]
            del self.kiwi_build_command[arg_index]
            return value
