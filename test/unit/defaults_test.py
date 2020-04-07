from kiwi_boxed_plugin.defaults import Defaults


class TestDefaults:
    def test_get_box_config_file(self):
        assert Defaults.get_box_config_file() == '/etc/boxes.yml'
