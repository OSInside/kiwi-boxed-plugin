# Copyright (c) 2025 SUSE LLC.  All rights reserved.
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
from tempfile import NamedTemporaryFile
from typing import (
    List, Optional
)
from kiwi.path import Path
from kiwi.command import Command
from kiwi.defaults import Defaults as KiwiDefaults

from kiwi_boxed_plugin.box_download import BoxDownload
from kiwi_boxed_plugin.exceptions import (
    KiwiError
)

log = logging.getLogger('kiwi')


class BoxContainerBuild:
    """
    **Implements boxbuild command for container based build**

    Implements an interface to run a kiwi build box using
    the podman container engine

    :param str boxname: name of the box from kiwi_boxed_plugin.yml
    :param str arch: arch name for box
    """
    def __init__(
        self, boxname: str, arch: str = ''
    ) -> None:
        self.kiwi_cache = f'/{KiwiDefaults.get_shared_cache_location()}'
        self.arch = arch or platform.machine()
        self.box = BoxDownload(boxname, arch)
        self.kiwi_exit: Optional[int] = None

    def run(
        self, kiwi_build_command: List[str],
        keep_open: bool = False, kiwi_version: str = '',
        custom_shared_path: str = ''
    ) -> None:
        """
        Start the build process in a container

        :param list kiwi_build_command:
            kiwi build command line Example:

            .. code:: python

                [
                    '--type', 'oem', 'system', 'build',
                    '--description', 'some/description',
                    '--target-dir', 'some/target-dir'
                ]

        :param bool keep_open: keep container running True|False
        :param str kiwi_version: pip install this kiwi version
        :param str custom_shared_path: make this path available in the container
        """
        self.kiwi_build_command = kiwi_build_command
        desc = os.path.abspath(
            self._pop_arg_param('--description')
        )
        target_dir = os.path.abspath(
            self._pop_arg_param('--target-dir')
        )
        Path.create(target_dir)

        container_name = self.box.fetch_container()

        container_cmdline = [
            'kiwi="{0}"'.format(' '.join(self.kiwi_build_command))
        ]
        if keep_open:
            container_cmdline.append('kiwi-no-halt')
        if kiwi_version:
            container_cmdline.append(
                'kiwi_version=_{0}_'.format(kiwi_version)
            )
        if custom_shared_path:
            custom_shared_path = os.path.abspath(custom_shared_path)
            if not os.path.exists(custom_shared_path):
                raise KiwiError(
                    f'Custom share path {custom_shared_path} does not exist'
                )
            container_cmdline.append(
                'custom_mount=_{0}_'.format(custom_shared_path)
            )

        if not os.path.exists(desc):
            raise KiwiError(
                f'Image description {desc} does not exist'
            )

        self.cmdline = NamedTemporaryFile(prefix='cmdline')
        with open(self.cmdline.name, 'w') as cmdline:
            cmdline.write('{0}'.format(' '.join(container_cmdline)))
            cmdline.write(os.linesep)

        if not os.path.isdir(self.kiwi_cache):
            Command.run(['sudo', 'mkdir', '-p', self.kiwi_cache])
        container_run = [
            'sudo', 'podman', 'run',
            '--rm',
            '-ti',
            '--privileged',
            '--net', 'host',
            '--cap-add', 'AUDIT_WRITE',
            '--cap-add', 'AUDIT_CONTROL',
            '--cap-add', 'CAP_MKNOD',
            '--cap-add', 'CAP_SYS_ADMIN',
            '--volume', '/var/cache/kiwi:/var/cache/kiwi',
            '--volume', f'{self.cmdline.name}:/container.cmdline',
            '--volume', f'{target_dir}:/bundle',
            '--volume', f'{desc}:/description',
            '--volume', '/dev:/dev'
        ]
        if custom_shared_path:
            container_run.append('--volume')
            container_run.append(f'{custom_shared_path}:{custom_shared_path}')
        container_run.append(container_name)

        log.debug(
            'Calling podman: {0}'.format(container_run)
        )
        os.system(
            ' '.join(container_run)
        )

        exit_code_file = os.sep.join([target_dir, 'result.code'])
        build_log_file = os.sep.join([target_dir, 'result.log'])
        self.kiwi_exit = 0
        if os.path.exists(exit_code_file):
            with open(exit_code_file) as exit_code:
                self.kiwi_exit = int(exit_code.readline())

        if self.kiwi_exit != 0:
            raise KiwiError(
                f'Box build failed. Find build log at: {build_log_file!r}'
            )

        log.info(
            f'Box build done. Find build log at: {build_log_file!r}'
        )

    def _pop_arg_param(self, arg: str) -> str:
        arg_index = self.kiwi_build_command.index(arg)
        arg_value = ''
        if arg_index:
            arg_value = self.kiwi_build_command[arg_index + 1]
            del self.kiwi_build_command[arg_index + 1]
            del self.kiwi_build_command[arg_index]
        return arg_value
