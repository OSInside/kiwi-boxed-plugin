from pkg_resources import resource_filename
from kiwi_boxed_plugin.defaults import Defaults
from mock import patch, Mock
import os


class TestDefaults:
    def test_get_plugin_config_file(self):
        assert Defaults.get_plugin_config_file() == resource_filename(
            'kiwi_boxed_plugin', 'config/kiwi_boxed_plugin.yml'
        )

    @patch("os.path.exists", lambda f: True)
    @patch.dict(os.environ, KIWI_BOXED_PLUGIN_CFG="aarchderwelt.conf")
    def test_get_plugin_config_file_env(self):
        assert Defaults.get_plugin_config_file() == "aarchderwelt.conf", \
            "aarch64 aonfiguration from the environment variable do not match"

    @patch("os.path.abspath", lambda f: "/highway/to/hell.conf")
    @patch("os.path.exists", lambda f: True)
    def test_get_plugin_config_file_currdir(self):
        assert Defaults.get_plugin_config_file() == "/highway/to/hell.conf", \
            "Should contain absolute path to the config"
