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

    def test_process_system_boxbuild(self):
        self._init_command_args()
        self.task.command_args['boxbuild'] = True
        self.task.process()
