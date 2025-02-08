from unittest.mock import patch
from pytest import raises

from kiwi_boxed_plugin.box_config import BoxConfig
from kiwi_boxed_plugin.exceptions import (
    KiwiBoxPluginConfigError,
    KiwiBoxPluginBoxNameError,
    KiwiBoxPluginArchNotFoundError
)


class TestBoxConfig:
    @patch('kiwi_boxed_plugin.defaults.Defaults.get_plugin_config_file')
    @patch('platform.machine')
    def setup(self, mock_platform_machine, mock_get_plugin_config_file):
        mock_platform_machine.return_value = 'x86_64'
        mock_get_plugin_config_file.return_value = \
            '../data/kiwi_boxed_plugin.yml'
        self.box_config = BoxConfig('suse')

    @patch('kiwi_boxed_plugin.defaults.Defaults.get_plugin_config_file')
    @patch('platform.machine')
    def setup_method(
        self, cls, mock_platform_machine, mock_get_plugin_config_file
    ):
        self.setup()

    @patch('yaml.safe_load')
    @patch('kiwi_boxed_plugin.defaults.Defaults.get_plugin_config_file')
    def test_setup_raises_on_load_config(
        self, mock_get_plugin_config_file, mock_yaml_safe_load
    ):
        mock_get_plugin_config_file.return_value = \
            '../data/kiwi_boxed_plugin.yml'
        mock_yaml_safe_load.side_effect = Exception
        with raises(KiwiBoxPluginConfigError):
            BoxConfig('suse')

    @patch('kiwi_boxed_plugin.defaults.Defaults.get_plugin_config_file')
    def test_setup_raises_on_unsupported_arch(
        self, mock_get_plugin_config_file
    ):
        mock_get_plugin_config_file.return_value = \
            '../data/kiwi_boxed_plugin.yml'
        with raises(KiwiBoxPluginArchNotFoundError):
            BoxConfig('suse', 'artificial_arch')

    @patch('kiwi_boxed_plugin.defaults.Defaults.get_plugin_config_file')
    def test_setup_raises_box_not_found(self, mock_get_plugin_config_file):
        mock_get_plugin_config_file.return_value = \
            '../data/kiwi_boxed_plugin.yml'
        with raises(KiwiBoxPluginBoxNameError):
            self.box_config = BoxConfig('foo', 'x86_64')

    def test_get_box_arch(self):
        assert self.box_config.get_box_arch() == 'x86_64'

    def test_get_box_memory_mbytes(self):
        assert self.box_config.get_box_memory_mbytes() == '8096M'

    def test_get_box_console(self):
        assert self.box_config.get_box_console() == 'hvc0'

    def test_get_box_kernel_cmdline(self):
        assert self.box_config.get_box_kernel_cmdline() == \
            'root=/dev/vda1 rd.plymouth=0'

    def test_get_box_source(self):
        assert self.box_config.get_box_source() == \
            'obs://Virtualization:Appliances:SelfContained:suse/images'

    def test_get_box_packages_file(self):
        assert self.box_config.get_box_packages_file() == \
            'SUSE-Box.x86_64-1.42.1-System-BuildBox.report'

    def test_get_box_packages_shasum_file(self):
        assert self.box_config.get_box_packages_shasum_file() == \
            'SUSE-Box.x86_64-1.42.1-System-BuildBox.report.sha256'

    def test_get_box_files(self):
        assert self.box_config.get_box_files() == [
            'SUSE-Box.x86_64-1.42.1-Kernel-BuildBox.tar.xz',
            'SUSE-Box.x86_64-1.42.1-Kernel-BuildBox.tar.xz.sha256',
            'SUSE-Box.x86_64-1.42.1-System-BuildBox.qcow2',
            'SUSE-Box.x86_64-1.42.1-System-BuildBox.qcow2.sha256'
        ]
