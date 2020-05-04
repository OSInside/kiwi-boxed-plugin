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
from cerberus import Validator
import logging
import yaml

from kiwi_boxed_plugin.plugin_config_schema import schema
from kiwi_boxed_plugin.defaults import Defaults
from kiwi_boxed_plugin.exceptions import KiwiBoxPluginConfigError

log = logging.getLogger('kiwi')


class PluginConfig:
    """
    **Implements reading of box plugin config file:**

    /etc/kiwi_boxed_plugin.yml

    The KIWI boxed plugin box configuration file is a yaml
    formatted file containing information about available
    virtual disk images usable as build boxes
    """
    def __init__(self):
        self.config_data = None
        plugin_config_file = Defaults.get_plugin_config_file()
        log.info('Reading box plugin config file: {0}'.format(
            plugin_config_file)
        )
        try:
            with open(plugin_config_file, 'r') as config:
                self.config_data = yaml.safe_load(config)
        except Exception as issue:
            raise KiwiBoxPluginConfigError(issue)
        validator = Validator(schema)
        validator.validate(self.config_data, schema)
        if validator.errors:
            raise KiwiBoxPluginConfigError(
                'Failed to validate {0}: {1}'.format(
                    plugin_config_file, validator.errors
                )
            )

    def get_config(self):
        """
        Return config data dictionary
        """
        return self.config_data.get('box')

    def dump_config(self):
        """
        Return config dump as pretty string for the console
        """
        return yaml.dump(self.config_data.get('box'))
