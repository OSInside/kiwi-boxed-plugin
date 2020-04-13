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
from collections import OrderedDict
from kiwi.command import Command

from kiwi_boxed_plugin.box_download import BoxDownload
from kiwi_boxed_plugin.defaults import Defaults

log = logging.getLogger('kiwi')


class BoxBuild:
    """
    **Implements boxbuild command**

    Implements an interface to run a kiwi build box using
    the KVM virtualization platform
    """
    def __init__(self, boxname, arch=None):
        self.arch = arch or platform.machine()
        self.box = BoxDownload(boxname, arch)

    def run(self, kiwi_build_command_args, update_check=True):
        vm_setup = self.box.fetch(update_check)
        vm_run = [
            'qemu-system-{0}'.format(self.arch)
        ] + Defaults.get_qemu_generic_setup() + [
            '-kernel', vm_setup.kernel,
            '-append', '{0} kiwi="{1}"'.format(
                vm_setup.append, self._prepare_vm_kiwi_command_args(
                    kiwi_build_command_args
                )
            )
        ] + Defaults.get_qemu_storage_setup(vm_setup.system) + \
            Defaults.get_qemu_network_setup() + \
            Defaults.get_qemu_console_setup() + \
            Defaults.get_qemu_shared_path_setup(0, kiwi_build_command_args.get(
                '--description'
            ), 'kiwidescription') + \
            Defaults.get_qemu_shared_path_setup(1, kiwi_build_command_args.get(
                '--target-dir'
            ), 'kiwibundle')
        return Command.call(
            vm_run, self._create_runtime_environment()
        )

    def _create_runtime_environment(self):
        return dict(
            os.environ, TMPDIR=Defaults.get_local_box_cache_dir()
        )

    def _prepare_vm_kiwi_command_args(self, args):
        args_dict = OrderedDict(list(args.items()))
        args_list = []
        if '--description' in args_dict:
            del args_dict['--description']
        if '--target-dir' in args_dict:
            del args_dict['--target-dir']
        for key, value in list(args_dict.items()):
            args_list.append(key)
            if value:
                args_list.append(value)
        return ' '.join(args_list)
