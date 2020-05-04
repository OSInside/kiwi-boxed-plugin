import logging
from mock import patch
from pytest import (
    raises, fixture
)

from kiwi_boxed_plugin.box_config import BoxConfig
from kiwi_boxed_plugin.exceptions import (
    KiwiBoxPluginConfigError,
    KiwiBoxPluginBoxNameError
)


class TestBoxConfig:
    @fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    @patch('kiwi_boxed_plugin.defaults.Defaults.get_plugin_config_file')
    @patch('platform.machine')
    def setup(self, mock_platform_machine, mock_get_plugin_config_file):
        mock_platform_machine.return_value = 'x86_64'
        mock_get_plugin_config_file.return_value = \
            '../data/kiwi_boxed_plugin.yml'
        with self._caplog.at_level(logging.INFO):
            self.box_config = BoxConfig('suse')

    @patch('yaml.safe_load')
    @patch('kiwi_boxed_plugin.defaults.Defaults.get_plugin_config_file')
    def test_setup_raises(
        self, mock_get_plugin_config_file, mock_yaml_safe_load
    ):
        mock_get_plugin_config_file.return_value = \
            '../data/kiwi_boxed_plugin.yml'
        mock_yaml_safe_load.side_effect = Exception
        with raises(KiwiBoxPluginConfigError):
            BoxConfig('suse')

    @patch('kiwi_boxed_plugin.defaults.Defaults.get_plugin_config_file')
    def test_setup_raises_box_not_found(self, mock_get_plugin_config_file):
        mock_get_plugin_config_file.return_value = \
            '../data/kiwi_boxed_plugin.yml'
        with raises(KiwiBoxPluginBoxNameError):
            self.box_config = BoxConfig('foo', 'x86_64')

    def test_get_box_arch(self):
        assert self.box_config.get_box_arch() == 'x86_64'

    def test_get_box_memory_mbytes(self):
        assert self.box_config.get_box_memory_mbytes() == 8096

    def test_get_box_root(self):
        assert self.box_config.get_box_root() == '/dev/vda1'

    def test_get_box_console(self):
        assert self.box_config.get_box_console() == 'hvc0'

    def test_get_box_kernel_cmdline(self):
        assert self.box_config.get_box_kernel_cmdline() == 'rd.plymouth=0'

    def test_get_box_source(self):
        assert self.box_config.get_box_source() == \
            'obs://Virtualization:Appliances:SelfContained:suse/images'

    def test_get_box_packages_file(self):
        assert self.box_config.get_box_packages_file() == \
            'SUSE-Box.x86_64-1.42.1-System-BuildBox.packages'

    def test_get_box_packages_shasum_file(self):
        assert self.box_config.get_box_packages_shasum_file() == \
            'SUSE-Box.x86_64-1.42.1-System-BuildBox.packages.sha256'

    def test_get_box_files(self):
        assert self.box_config.get_box_files() == [
            'SUSE-Box.x86_64-1.42.1-Kernel-BuildBox.tar.xz',
            'SUSE-Box.x86_64-1.42.1-System-BuildBox.qcow2'
        ]
