import sys

from mock import (
    Mock, patch
)
from kiwi_boxed_plugin.tasks.system_boxbuild import SystemBoxbuildTask


class TestSystemBoxbuildTask:
    def setup(self):
        sys.argv = [
            sys.argv[0], 'system', 'boxbuild',
            '--box', 'suse', '--box-memory', '4', '--',
            '--description', '../data/description',
            '--target-dir', '../data/target_dir'
        ]
        self.task = SystemBoxbuildTask()

    def _init_command_args(self):
        self.task.command_args = {}
        self.task.command_args['help'] = False
        self.task.command_args['boxbuild'] = False
        self.task.command_args['--list-boxes'] = False
        self.task.command_args['--box'] = None

    @patch('kiwi_boxed_plugin.tasks.system_boxbuild.Help')
    def test_process_system_boxbuild_help(self, mock_kiwi_Help):
        Help = Mock()
        mock_kiwi_Help.return_value = Help
        self._init_command_args()
        self.task.command_args['help'] = True
        self.task.command_args['boxbuild'] = True
        self.task.process()
        Help.show.assert_called_once_with(
            'kiwi::system::boxbuild'
        )

    @patch('kiwi_boxed_plugin.tasks.system_boxbuild.PluginConfig')
    def test_process_system_boxbuild_list_boxes(self, mock_PluginConfig):
        plugin = Mock()
        mock_PluginConfig.return_value = plugin
        self._init_command_args()
        self.task.command_args['boxbuild'] = True
        self.task.command_args['--list-boxes'] = True
        self.task.process()
        plugin.dump_config.assert_called_once_with()

    @patch('kiwi_boxed_plugin.tasks.system_boxbuild.BoxDownload')
    def test_process_system_boxbuild(self, mock_BoxDownload):
        self._init_command_args()
        self.task.command_args['boxbuild'] = True
        self.task.command_args['--box'] = 'suse'
        self.task.process()
