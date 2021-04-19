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
           [--box-debug]
           [--kiwi-version=<version>]
           [--shared-path=<path>]
           [--no-update-check]
           [--no-snapshot]
           [--9p-sharing | --virtiofs-sharing]
           [--x86_64 | --aarch64]
           [--machine=<qemu_machine>]
           [--cpu=<qemu_cpu>]
           -- <kiwi_build_command_args>...
       kiwi-ng system boxbuild --list-boxes
       kiwi-ng system boxbuild help

commands:
    boxbuild
        build a system image in a self contained virtual machine,
        where separator -- marks the start of arguments passed to
        the build command.

options:
    --box=<name>
        Name of the virtual machine that should be used for
        the build process.

    --list-boxes
        show available build boxes.

    --box-memory=<vmgb>
        Number of GBs to reserve as main memory for the virtual
        machine. By default 8GB will be used.

    --no-update-check
        Skip check for available box update. The option has no
        effect if the selected box does not yet exist on the host.

    --no-snapshot
        Run box with snapshot mode switched off. This causes the
        box disk file to be modified by the build process and allows
        to keep a persistent package cache as part of the box.
        The option can be used to increase the build performance
        due to data stored in the box which doesn't have to be
        reloaded from the network. On the contrary this option
        invalidates the immutable box attribute and should be
        used with care. On update of the box all data stored
        will be wiped. To prevent this combine the option with
        the --no-update-check option.

    --9p-sharing|--virtiofs-sharing
        Select sharing backend to use for sharing data between the
        host and the box. This can be either 9p or virtiofs. By
        default 9p is used

    --x86_64|--aarch64
        Select box for the given architecture. If no architecture
        is selected the host architecture is used for selecting
        the box. The selected box architecture also specifies the
        target architecture for the image build with that box.

    --box-debug
        In debug mode the started virtual machine will be kept open

    --kiwi-version=<version>
        Specify a KIWI version to use for the build. The referenced
        KIWI will be fetched from pip and replaces the box installed
        KIWI version. Note: If --no-snapshot is used in combination
        with this option, the change of the KIWI version will be
        permanently stored in the used box.

    --shared-path=<path>
        Optional host path to share with the box. The same path
        as it is present on the host will also be available inside
        of the box during build time.

    --machine=<qemu_machine>
        Optional machine name used by QEMU. By default no specific
        value is used here and qemu selects its default machine type.
        For cross arch builds or for system architectures for which
        QEMU defines no default like for Arm, it's required to specify
        a machine name.

        If you don’t care about reproducing the idiosyncrasies of
        a particular bit of hardware, the best option is to use
        the 'virt' machine type.

    --cpu=<qemu_cpu>
        Optional CPU type used by QEMU. By default the host CPU
        type is used which is only a good selection if the host
        and the selected box are from the same architecture. On
        cross arch builds it's required to specify the CPU
        emulation the box should use

    -- <kiwi_build_command_args>...
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

from kiwi_boxed_plugin.box_build import BoxBuild
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
            request_update_check = not self.command_args.get(
                '--no-update-check'
            )
            request_snapshot_mode = not self.command_args.get(
                '--no-snapshot'
            )
            keep_open = self.command_args.get('--box-debug')
            kiwi_version = self.command_args.get('--kiwi-version')
            shared_path = self.command_args.get('--shared-path')
            box_build = BoxBuild(
                boxname=self.command_args.get('--box'),
                ram=self.command_args.get('--box-memory'),
                arch=self._get_box_arch(),
                machine=self.command_args.get('--machine'),
                cpu=self.command_args.get('--cpu') or 'host',
                sharing_backend=self._get_sharing_backend()
            )
            box_build.run(
                self._validate_kiwi_build_command(),
                request_update_check,
                request_snapshot_mode,
                keep_open,
                kiwi_version,
                shared_path
            )

    def _validate_kiwi_build_command(self):
        kiwi_build_command = [
            'system', 'build'
        ]
        kiwi_build_command += self.command_args.get(
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

    def _get_box_arch(self):
        box_arch = None
        if self.command_args.get('--x86_64'):
            box_arch = 'x86_64'
        elif self.command_args.get('--aarch64'):
            box_arch = 'aarch64'
        return box_arch

    def _get_sharing_backend(self):
        return 'virtiofs' if self.command_args.get(
            '--virtiofs-sharing'
        ) else '9p'
