import logging
import yaml
from mock import patch
from pytest import (
    raises, fixture
)

from kiwi_boxed_plugin.plugin_config import PluginConfig
from kiwi_boxed_plugin.exceptions import KiwiBoxPluginConfigError


class TestPluginConfig:
    @fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    @patch('kiwi_boxed_plugin.defaults.Defaults.get_plugin_config_file')
    def setup(self, mock_get_plugin_config_file):
        mock_get_plugin_config_file.return_value = \
            '../data/kiwi_boxed_plugin.yml'
        with self._caplog.at_level(logging.INFO):
            self.plugin_config = PluginConfig()

    def test_get_config(self):
        assert self.plugin_config.get_config() == {
            'suse': {
                'mem_mb': 4096,
                'root': '/dev/vda1',
                'console': 'hvc0',
                'cmdline': 'rd.plymouth=0',
                'x86_64': {
                    'source': 'obs://Virtualization:Appliances:SelfContained:'
                    'suse/images',
                    'packages_file': 'SUSE-Box.x86_64-1.42.1-System-BuildBox'
                    '.packages',
                    'boxfiles': [
                        'SUSE-Box.x86_64-1.42.1-Kernel-BuildBox.tar.xz',
                        'SUSE-Box.x86_64-1.42.1-System-BuildBox.qcow2'
                    ]
                }
            }
        }

    def test_dump_config(self):
        assert self.plugin_config.dump_config() == yaml.dump(
            self.plugin_config.get_config()
        )

    @patch('yaml.safe_load')
    def test_setup_raises(self, mock_yaml_safe_load):
        mock_yaml_safe_load.side_effect = Exception
        with raises(KiwiBoxPluginConfigError):
            PluginConfig()
