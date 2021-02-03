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
import platform

from kiwi_boxed_plugin.plugin_config import PluginConfig
from kiwi_boxed_plugin.exceptions import (
    KiwiBoxPluginBoxNameError,
    KiwiBoxPluginArchNotFoundError
)


class BoxConfig:
    """
    **Implements reading of box configuration:**
    """
    def __init__(self, boxname, arch=None):
        self.arch = arch or platform.machine()

        plugin_config = PluginConfig()

        self.box_config = self._get_box_config(
            plugin_config.get_config(), boxname
        )
        if not self.box_config:
            raise KiwiBoxPluginBoxNameError(
                'Box: {0} not found'.format(boxname)
            )
        self.box_arch_config = self._get_box_arch_config(
            self.box_config, self.arch
        )

    def get_box_arch(self):
        return self.arch

    def get_box_memory_mbytes(self):
        return self.box_config.get('mem_mb')

    def get_box_processors(self):
        return self.box_config.get('processors')

    def get_box_console(self):
        return self.box_config.get('console')

    def get_box_kernel_cmdline(self):
        return ' '.join(self.box_arch_config.get('cmdline'))

    def get_box_source(self):
        return self.box_arch_config.get('source')

    def get_box_packages_file(self):
        return self.box_arch_config.get('packages_file')

    def get_box_packages_shasum_file(self):
        return self.box_arch_config.get('packages_file') + '.sha256'

    def get_box_files(self):
        source_files = []
        for vm_file in self.box_arch_config.get('boxfiles'):
            source_files.append(vm_file)
        return source_files

    def use_initrd(self):
        return bool(self.box_arch_config.get('use_initrd'))

    def _get_box_config(self, plugin_config, name):
        for box in plugin_config:
            if box.get('name') == name:
                return box

    def _get_box_arch_config(self, box_config, arch):
        for box_arch in box_config.get('arch'):
            if box_arch.get('name') == arch:
                return box_arch
        raise KiwiBoxPluginArchNotFoundError(
            f'No box configuration found for architecture: {arch}'
        )
