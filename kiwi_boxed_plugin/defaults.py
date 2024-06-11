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
import pathlib
from typing import List
from kiwi.path import Path
from pkg_resources import resource_filename
import subprocess

from kiwi_boxed_plugin.exceptions import KiwiBoxPluginVirtioFsError

VIRTIOFSD_PROCESS_LIST = []
HOST_SSH_PORT_FORWARDED_TO_BOX = 10000


class Defaults:
    """
    **Implements default values**

    Provides static methods for default values and state information
    """
    box_ssh_port_forwarded_to_host = 10022

    @staticmethod
    def get_plugin_config_file() -> str:
        """
        Config file name: `kiwi_boxed_plugin.yml`
        Locations are searched in this order:
            1. ENV variable: $KIWI_BOXED_PLUGIN_CFG
               full path to file, name is freely selectable
            2. $PWD/kiwi_boxed_plugin.yml
            3. $HOME/.config/kiwi/kiwi_boxed_plugin.yml
            4. /etc/kiwi_boxed_plugin.yml
            5. Resource (default config, coming with the package)
        """
        config_name = "kiwi_boxed_plugin.yml"

        # 1.
        config_path_env: str | None = os.environ.get("KIWI_BOXED_PLUGIN_CFG")
        if config_path_env is not None and os.path.exists(config_path_env):
            return config_path_env

        # 2.
        config_path_pwd = os.path.abspath(config_name)
        if os.path.exists(config_path_pwd):
            return config_path_pwd

        # 3.
        config_path_home: pathlib.Path = pathlib.Path.home().joinpath(
            f'.config/kiwi/{config_name}'
        )
        if config_path_home.exists():
            return config_path_home.as_posix()

        # 4.
        config_path_system = f'/etc/{config_name}'
        if os.path.exists(config_path_system):
            return config_path_system

        # 5.
        return resource_filename(
            'kiwi_boxed_plugin', f'config/{config_name}'
        )

    @staticmethod
    def get_local_box_cache_dir() -> str:
        return f'{os.environ.get("HOME")}/.kiwi_boxes'

    @staticmethod
    def get_qemu_generic_setup() -> List[str]:
        return [
            '-nographic',
            '-nodefaults',
            '-snapshot'
        ]

    @staticmethod
    def get_qemu_network_setup() -> List[str]:
        return [
            '-nic',
            f'user,model=virtio,hostfwd=tcp::{Defaults.box_ssh_port_forwarded_to_host}-:22'
        ]

    @staticmethod
    def get_qemu_shared_path_setup(
        index: int, path: str, mount_tag: str, sharing_backend: str = '9p'
    ) -> List[str]:
        shared_setup: List[str] = []
        if sharing_backend == '9p':
            shared_setup = Defaults.get_qemu_shared_path_setup_9p(
                index, path, mount_tag
            )
        if sharing_backend == 'virtiofs':
            shared_setup = Defaults.get_qemu_shared_path_setup_virtiofs(
                index, path, mount_tag
            )
        return shared_setup

    @staticmethod
    def get_qemu_shared_path_setup_9p(
        index: int, path: str, mount_tag: str
    ) -> List[str]:
        return [
            '-fsdev',
            'local,security_model=mapped,id=fsdev{0},path={1}'.format(
                index, path
            ),
            '-device',
            'virtio-9p-pci,id=fs{0},fsdev=fsdev{0},mount_tag={1}'.format(
                index, mount_tag
            )
        ]

    @staticmethod
    def get_qemu_shared_path_setup_virtiofs(
        index: int, path: str, mount_tag: str
    ) -> List[str]:
        virtiofsd_lookup_paths = ['/usr/lib/virtiofsd', '/usr/libexec']
        virtiofsd = Path.which(
            'virtiofsd', virtiofsd_lookup_paths
        )
        if not virtiofsd:
            raise KiwiBoxPluginVirtioFsError(
                'virtiofsd not found in: {0}'.format(virtiofsd_lookup_paths)
            )
        try:
            virtiofsd_process = subprocess.Popen(
                [
                    virtiofsd,
                    '--socket-path=/tmp/vhostqemu_{0}'.format(index),
                    '--shared-dir', os.path.abspath(path),
                    '--sandbox', 'namespace',
                    '--cache', 'always',
                    '--allow-direct-io',
                    '--posix-acl',
                    '--xattr'
                ], close_fds=True
            )
        except Exception as issue:
            raise KiwiBoxPluginVirtioFsError(
                'Failed to start virtiofsd: {0}'.format(issue)
            )
        VIRTIOFSD_PROCESS_LIST.append(virtiofsd_process)
        return [
            '-chardev',
            'socket,id=char{0},path=/tmp/vhostqemu_{0}'.format(index),
            '-device',
            'vhost-user-fs-pci,queue-size=1024,chardev=char{0},tag={1}'.format(
                index, mount_tag
            )
        ]

    @staticmethod
    def get_qemu_console_setup() -> List[str]:
        return [
            '-device', 'virtio-serial',
            '-chardev', 'stdio,id=virtiocon0',
            '-device', 'virtconsole,chardev=virtiocon0'
        ]

    @staticmethod
    def get_qemu_storage_setup(
        image_file: str, snapshot: bool = True
    ) -> List[str]:
        return [
            '-drive',
            'file={0},if=virtio,driver=qcow2,cache=off,snapshot={1}'.format(
                image_file, 'on' if snapshot else 'off'
            )
        ]
