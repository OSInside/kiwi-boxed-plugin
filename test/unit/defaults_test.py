import importlib
from importlib.resources import as_file
from kiwi_boxed_plugin.defaults import Defaults
from kiwi_boxed_plugin.exceptions import KiwiBoxPluginTargetPathError
from pytest import raises
from unittest.mock import (
    patch,
    call
)
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
        with as_file(importlib.resources.files('kiwi_boxed_plugin')) as path:
            config_file = f'{path}/config/kiwi_boxed_plugin.yml'
        assert Defaults.get_plugin_config_file() == config_file

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

    @patch('pathlib.Path')
    def test_create_build_target_dir(self, mock_Path):
        Defaults.create_build_target_dir('some')
        assert mock_Path.call_args_list == [
            call('some'),
            call('some/result.log'),
        ]
        mock_Path.side_effect = Exception('some error')
        with raises(KiwiBoxPluginTargetPathError):
            Defaults.create_build_target_dir('some')
