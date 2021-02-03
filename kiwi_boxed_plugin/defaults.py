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
from kiwi.path import Path
from pkg_resources import resource_filename
import subprocess

from kiwi_boxed_plugin.exceptions import KiwiBoxPluginVirtioFsError

VIRTIOFSD_PROCESS_LIST = []


class Defaults:
    """
    **Implements default values**

    Provides static methods for default values and state information
    """
    @staticmethod
    def get_plugin_config_file():
        return resource_filename(
            'kiwi_boxed_plugin', 'config/kiwi_boxed_plugin.yml'
        )

    @staticmethod
    def get_local_box_cache_dir():
        return '/var/tmp/kiwi/boxes'

    @staticmethod
    def get_qemu_generic_setup():
        return [
            '-nographic',
            '-nodefaults',
            '-snapshot'
        ]

    @staticmethod
    def get_qemu_network_setup():
        return [
            '-netdev', 'user,id=user0',
            '-device', 'virtio-net-pci,netdev=user0'
        ]

    @staticmethod
    def get_qemu_shared_path_setup(
        index, path, mount_tag, sharing_backend='9p'
    ):
        if sharing_backend == '9p':
            return Defaults.get_qemu_shared_path_setup_9p(
                index, path, mount_tag
            )
        else:
            return Defaults.get_qemu_shared_path_setup_virtiofs(
                index, path, mount_tag
            )

    @staticmethod
    def get_qemu_shared_path_setup_9p(index, path, mount_tag):
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
    def get_qemu_shared_path_setup_virtiofs(index, path, mount_tag):
        virtiofsd_lookup_paths = ['/usr/lib', '/usr/libexec']
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
                    '-o', 'allow_root',
                    '-o', 'source={0}'.format(os.path.abspath(path)),
                    '-o', 'cache=always'
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
    def get_qemu_console_setup():
        return [
            '-device', 'virtio-serial',
            '-chardev', 'stdio,id=virtiocon0',
            '-device', 'virtconsole,chardev=virtiocon0'
        ]

    @staticmethod
    def get_qemu_storage_setup(image_file, snapshot=True):
        return [
            '-drive',
            'file={0},if=virtio,driver=qcow2,cache=off,snapshot={1}'.format(
                image_file, 'on' if snapshot else 'off'
            )
        ]
