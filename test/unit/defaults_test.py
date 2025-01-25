from pkg_resources import resource_filename
from kiwi_boxed_plugin.defaults import Defaults
from unittest.mock import patch
import os


class MockedPath:
    def __init__(self):
        self.p: str | None = None

    def home(self):
        return self

    @staticmethod
    def exists():
        return True

    def joinpath(self, f: str):
        self.p = os.path.join("/home/zoidberg", f)
        return self

    def as_posix(self):
        return self.p


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

    @patch("pathlib.Path", MockedPath())
    def test_get_plugin_config_file_local_kiwi(self):
        assert Defaults.get_plugin_config_file() == "/home/zoidberg/.config/kiwi/kiwi_boxed_plugin.yml", \
            "Should contain local Kiwi Box config"

    @patch("os.path.exists", lambda f: f == "/etc/kiwi_boxed_plugin.yml")
    def test_get_plugin_config_file_etc(self):
        assert Defaults.get_plugin_config_file() == "/etc/kiwi_boxed_plugin.yml", \
            "Should contain Kiwi Box config in /etc dir"
