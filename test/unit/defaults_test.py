from pkg_resources import resource_filename

from kiwi_boxed_plugin.defaults import Defaults


class TestDefaults:
    def test_get_plugin_config_file(self):
        assert Defaults.get_plugin_config_file() == resource_filename(
            'kiwi_boxed_plugin', 'config/kiwi_boxed_plugin.yml'
        )
