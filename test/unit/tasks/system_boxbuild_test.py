import sys

from mock import (
    Mock, patch
)
from kiwi_boxed_plugin.tasks.system_boxbuild import SystemBoxbuildTask


class TestSystemBoxbuildTask:
    def setup(self):
        sys.argv = [
            sys.argv[0],
            '--profile', 'foo', '--type', 'oem',
            'system', 'boxbuild',
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
        self.task.command_args['--box-debug'] = False
        self.task.command_args['--kiwi-version'] = None
        self.task.command_args['<kiwi_build_command_args>'] = [
            '--', '--description', 'foo',
            '--target-dir', 'xxx'
        ]

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

    @patch('kiwi_boxed_plugin.tasks.system_boxbuild.BoxBuild')
    def test_process_system_boxbuild(self, mock_BoxBuild):
        self._init_command_args()
        self.task.command_args['boxbuild'] = True
        self.task.command_args['--box'] = 'suse'
        box_build = Mock()
        mock_BoxBuild.return_value = box_build
        self.task.process()
        mock_BoxBuild.assert_called_once_with(
            boxname='suse', ram=None, arch=None
        )
        box_build.run.assert_called_once_with(
            [
                '--type', 'oem', '--profile', 'foo', 'system', 'build',
                '--description', 'foo', '--target-dir', 'xxx'
            ], True, True, False, None
        )
