from kiwi_boxed_plugin.defaults import Defaults


class TestDefaults:
    def test_get_plugin_config_file(self):
        assert Defaults.get_plugin_config_file() == \
            '/etc/kiwi_boxed_plugin.yml'
