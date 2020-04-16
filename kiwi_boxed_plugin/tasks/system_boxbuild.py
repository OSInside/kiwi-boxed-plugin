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
"""
usage: kiwi-ng system boxbuild -h | --help
       kiwi-ng system boxbuild --box=<name>
           [--box-memory=<vmgb>]
           [--no-update-check]
           [--x86_64 ]
           <kiwi_build_command_args>...
       kiwi-ng system boxbuild --list-boxes

commands:
    boxbuild
        build a system image in a self contained virtual machine

options:
    --box=<name>
        Name of the virtual machine that should be used for
        the build process.

    --list-boxes
        show available build boxes.

    --box-memory=<vmgb>
        Number of GBs to reserve as main memory for the virtual
        machine. By default 4GB will be used.

    --no-update-check
        Skip check for available box update. The option has no
        effect if the selected box does not yet exist on the host.

    --x86_64
        Select box for the x86_64 architecture. If no architecture
        is selected the host architecture is used for selecting
        the box. The selected box architecture also specifies the
        target architecture for the image build with that box.

    <kiwi_build_command_args>...
        List of command parameters as supported by the kiwi-ng
        build command. The information given here is passed
        along to the kiwi-ng system build command running in
        the virtual machine.
"""
import logging
import os
from docopt import docopt
from kiwi.tasks.base import CliTask
from kiwi.help import Help

import kiwi.tasks.system_build

from kiwi_boxed_plugin.box_download import BoxDownload
from kiwi_boxed_plugin.plugin_config import PluginConfig

log = logging.getLogger('kiwi')


class SystemBoxbuildTask(CliTask):
    def process(self):
        self.manual = Help()
        if self.command_args.get('help') is True:
            return self.manual.show('kiwi::system::boxbuild')

        elif self.command_args.get('--list-boxes'):
            print(PluginConfig().dump_config())

        elif self.command_args.get('--box'):
            kiwi_command_args = self._validate_kiwi_build_command()
            print(kiwi_command_args)
            box = BoxDownload('suse')
            vm_setup = box.fetch(update_check=True)
            print(vm_setup)

    def _validate_kiwi_build_command(self):
        kiwi_build_command = self.command_args.get(
            '<kiwi_build_command_args>'
        )
        if '--' in kiwi_build_command:
            kiwi_build_command.remove('--')
        log.info(
            'Validating kiwi_build_command_args:{0}    {1}'.format(
                os.linesep, kiwi_build_command
            )
        )
        docopt(
            doc=kiwi.tasks.system_build.__doc__,
            argv=kiwi_build_command
        )
        final_kiwi_build_command = []
        if self.global_args.get('--type'):
            final_kiwi_build_command.append('--type')
            final_kiwi_build_command.append(self.global_args.get('--type'))
        if self.global_args.get('--profile'):
            for profile in sorted(set(self.global_args.get('--profile'))):
                final_kiwi_build_command.append('--profile')
                final_kiwi_build_command.append(profile)
        final_kiwi_build_command += kiwi_build_command
        log.info(
            'Building with:{0}    {1}'.format(
                os.linesep, final_kiwi_build_command
            )
        )
        return final_kiwi_build_command
