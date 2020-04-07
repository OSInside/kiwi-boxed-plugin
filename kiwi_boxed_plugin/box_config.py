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
import yaml

from kiwi.system.uri import Uri

from kiwi_boxed_plugin.defaults import Defaults
from kiwi_boxed_plugin.exceptions import KiwiBoxPluginConfigError

log = logging.getLogger('kiwi-boxed-plugin')


class BoxConfig:
    """
    **Implements reading of box configuration file:**

    2. /etc/boxes.yml

    The KIWI boxed plugin box configuration file is a yaml
    formatted file containing information about available
    virtual disk images usable as build boxes
    """
    def __init__(self, boxname):
        self.box_data = None
        box_config_file = Defaults.get_box_config_file()
        if os.path.exists(box_config_file):
            log.info('Reading box config file: {0}'.format(box_config_file))
            try:
                with open(box_config_file, 'r') as config:
                    self.box_config_data = yaml.safe_load(config).get(boxname)
            except Exception as issue:
                raise KiwiBoxPluginConfigError(issue)

    def get_box_memory_mbytes(self):
        return self.box_config_data.get('mem_mb')

    def get_box_root(self):
        return self.box_config_data.get('root')

    def get_box_console(self):
        return self.box_config_data.get('console')

    def get_box_kernel_cmdline(self):
        return self.box_config_data.get('cmdline')

    def get_box_files(self):
        source_files = []
        source_uri = self.box_config_data.get('source')
        if source_uri:
            kiwi_uri = Uri(source_uri)
            for vm_file in self.box_config_data.get('boxfiles'):
                source_files.append(
                    kiwi_uri.translate(check_build_environment=False) + vm_file
                )
        return source_files
