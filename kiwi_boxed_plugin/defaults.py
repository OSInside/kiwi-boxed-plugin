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
from pkg_resources import resource_filename


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
            '-machine', 'accel=kvm',
            '-cpu', 'host',
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
    def get_qemu_shared_path_setup(index, path, mount_tag):
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
    def get_qemu_console_setup():
        return [
            '-device', 'virtio-serial',
            '-chardev', 'stdio,id=virtiocon0',
            '-device', 'virtconsole,chardev=virtiocon0'
        ]

    @staticmethod
    def get_qemu_storage_setup(image_file):
        return [
            '-drive',
            'file={0},if=virtio,driver=qcow2,cache=off,snapshot=on'.format(
                image_file
            )
        ]
