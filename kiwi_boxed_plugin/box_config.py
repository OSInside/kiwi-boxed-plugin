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
from typing import (
    List, Dict
)

from kiwi_boxed_plugin.plugin_config import PluginConfig
from kiwi_boxed_plugin.exceptions import (
    KiwiBoxPluginBoxNameError,
    KiwiBoxPluginArchNotFoundError
)


class BoxConfig:
    """
    **Implements reading of box configuration:**
    """
    def __init__(self, boxname: str, arch: str = '') -> None:
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

    def get_box_arch(self) -> str:
        return self.arch

    def get_box_memory_mbytes(self) -> str:
        return self.box_config.get('mem_mb') or ''

    def get_box_processors(self) -> str:
        return self.box_config.get('processors') or ''

    def get_box_console(self) -> str:
        return self.box_config.get('console') or ''

    def get_box_kernel_cmdline(self) -> str:
        return ' '.join(self.box_arch_config.get('cmdline') or '')

    def get_box_source(self) -> str:
        return self.box_arch_config.get('source') or ''

    def get_box_packages_file(self) -> str:
        return self.box_arch_config.get('packages_file') or ''

    def get_box_packages_shasum_file(self) -> str:
        packages_file = self.box_arch_config.get('packages_file') or ''
        if packages_file:
            packages_file += '.sha256'
        return packages_file

    def get_box_files(self) -> List[str]:
        source_files = []
        for vm_file in self.box_arch_config.get('boxfiles') or []:
            source_files.append(vm_file)
        return source_files

    def use_initrd(self) -> bool:
        return bool(self.box_arch_config.get('use_initrd'))

    def _get_box_config(
        self, plugin_config: List[Dict], name: str
    ) -> Dict:
        for box in plugin_config:
            if box.get('name') == name:
                return box
        return {}

    def _get_box_arch_config(
        self, box_config: Dict, arch: str
    ) -> Dict:
        for box_arch in box_config.get('arch') or []:
            if box_arch.get('name') == arch:
                return box_arch
        raise KiwiBoxPluginArchNotFoundError(
            f'No box configuration found for architecture: {arch}'
        )
