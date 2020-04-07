import logging
from mock import (
    patch, Mock
)
from pytest import (
    raises, fixture
)

from kiwi_boxed_plugin.box_config import BoxConfig
from kiwi_boxed_plugin.exceptions import KiwiBoxPluginConfigError


class TestBoxConfig:
    @fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    @patch('kiwi_boxed_plugin.defaults.Defaults.get_box_config_file')
    def setup(self, mock_get_box_config_file):
        mock_get_box_config_file.return_value = '../data/boxes.yml'
        with self._caplog.at_level(logging.INFO):
            self.box_config = BoxConfig('suse')

    @patch('yaml.safe_load')
    @patch('kiwi_boxed_plugin.defaults.Defaults.get_box_config_file')
    def test_setup_raises(self, mock_get_box_config_file, mock_yaml_safe_load):
        mock_get_box_config_file.return_value = '../data/boxes.yml'
        mock_yaml_safe_load.side_effect = Exception
        with raises(KiwiBoxPluginConfigError):
            BoxConfig('suse')

    def test_get_box_memory_mbytes(self):
        assert self.box_config.get_box_memory_mbytes() == 4096

    def test_get_box_root(self):
        assert self.box_config.get_box_root() == '/dev/vda1'

    def test_get_box_console(self):
        assert self.box_config.get_box_console() == 'hvc0'

    def test_get_box_kernel_cmdline(self):
        assert self.box_config.get_box_kernel_cmdline() == 'rd.plymouth=0'

    @patch('kiwi_boxed_plugin.box_config.Uri')
    def test_get_box_files(self, mock_Uri):
        kiwi_uri = Mock()
        kiwi_uri.translate.return_value = 'translated'
        mock_Uri.return_value = kiwi_uri
        source = kiwi_uri.translate.return_value
        assert self.box_config.get_box_files() == [
            source + 'SUSE-Box.x86_64-1.42.1-Kernel-BuildBox.tar.xz',
            source + 'SUSE-Box.x86_64-1.42.1-System-BuildBox.qcow2'
        ]
