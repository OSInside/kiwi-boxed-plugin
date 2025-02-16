import sys

from unittest.mock import (
    Mock, patch
)
from kiwi_boxed_plugin.tasks.system_boxbuild import SystemBoxbuildTask


class TestSystemBoxbuildTask:
    def setup(self):
        sys.argv = [
            sys.argv[0],
            '--debug', '--profile', 'foo', '--type', 'oem',
            'system', 'boxbuild',
            '--box', 'universal',
            '--box-memory', '4',
            '--box-console', 'ttyAMA0',
            '--box-smp-cpus', '4',
            '--',
            '--description', '../data/description',
            '--target-dir', '../data/target_dir'
        ]
        self.task = SystemBoxbuildTask()

    def setup_method(self, cls):
        self.setup()

    def _init_command_args(self):
        self.task.command_args = {}
        self.task.command_args['help'] = False
        self.task.command_args['boxbuild'] = False
        self.task.command_args['--list-boxes'] = False
        self.task.command_args['--container'] = False
        self.task.command_args['--box'] = None
        self.task.command_args['--box-debug'] = False
        self.task.command_args['--kiwi-version'] = None
        self.task.command_args['--shared-path'] = None
        self.task.command_args['--9p-sharing'] = None
        self.task.command_args['--sshfs-sharing'] = None
        self.task.command_args['--ssh-port'] = '22'
        self.task.command_args['--virtiofs-sharing'] = None
        self.task.command_args['--cpu'] = None
        self.task.command_args['--machine'] = None
        self.task.command_args['<kiwi_build_command_args>'] = [
            '--', '--description', 'foo',
            '--target-dir', 'xxx',
            '--add-package=a', '--add-package', 'b',
            '--allow-existing-root'
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

    @patch('kiwi_boxed_plugin.tasks.system_boxbuild.BoxContainerBuild')
    def test_process_system_boxbuild_container(self, mock_BoxContainerBuild):
        self._init_command_args()
        self.task.command_args['boxbuild'] = True
        self.task.command_args['--box'] = 'universal'
        self.task.command_args['--container'] = True
        box_containerbuild = Mock()
        mock_BoxContainerBuild.return_value = box_containerbuild
        self.task.process()
        mock_BoxContainerBuild.assert_called_once_with(
            boxname='universal', arch=''
        )
        box_containerbuild.run.assert_called_once_with(
            [
                '--debug', '--type', 'oem', '--profile', 'foo',
                'system', 'build',
                '--description', 'foo', '--target-dir', 'xxx',
                '--allow-existing-root',
                '--add-package', 'a', '--add-package', 'b'
            ], False, None, None
        )

    @patch('kiwi_boxed_plugin.tasks.system_boxbuild.BoxBuild')
    def test_process_system_boxbuild(self, mock_BoxBuild):
        self._init_command_args()
        self.task.command_args['boxbuild'] = True
        self.task.command_args['--box'] = 'universal'
        box_build = Mock()
        mock_BoxBuild.return_value = box_build
        self.task.process()
        mock_BoxBuild.assert_called_once_with(
            boxname='universal', ram=None, console=None, smp=None, arch='',
            machine=None, cpu='host', sharing_backend='9p',
            ssh_key='id_rsa', ssh_port='22', accel=True
        )
        box_build.run.assert_called_once_with(
            [
                '--debug', '--type', 'oem', '--profile', 'foo',
                'system', 'build',
                '--description', 'foo', '--target-dir', 'xxx',
                '--allow-existing-root',
                '--add-package', 'a', '--add-package', 'b'
            ], True, True, False, None, None
        )

    @patch('kiwi_boxed_plugin.tasks.system_boxbuild.BoxBuild')
    def test_process_system_boxbuild_for_x86_64(self, mock_BoxBuild):
        self._init_command_args()
        self.task.command_args['boxbuild'] = True
        self.task.command_args['--box'] = 'universal'
        self.task.command_args['--x86_64'] = True
        box_build = Mock()
        mock_BoxBuild.return_value = box_build
        self.task.process()
        mock_BoxBuild.assert_called_once_with(
            boxname='universal',
            ram=None, console=None, smp=None, arch='x86_64',
            machine=None, cpu='host', sharing_backend='9p',
            ssh_key='id_rsa', ssh_port='22', accel=True
        )

    @patch('kiwi_boxed_plugin.tasks.system_boxbuild.BoxBuild')
    def test_process_system_boxbuild_for_aarch64(self, mock_BoxBuild):
        self._init_command_args()
        self.task.command_args['boxbuild'] = True
        self.task.command_args['--box'] = 'universal'
        self.task.command_args['--aarch64'] = True
        box_build = Mock()
        mock_BoxBuild.return_value = box_build
        self.task.process()
        mock_BoxBuild.assert_called_once_with(
            boxname='universal',
            ram=None, console=None, smp=None, arch='aarch64',
            machine=None, cpu='host', sharing_backend='9p',
            ssh_key='id_rsa', ssh_port='22', accel=True
        )

    @patch('kiwi_boxed_plugin.tasks.system_boxbuild.BoxBuild')
    def test_process_system_boxbuild_with_sharing_backend(self, mock_BoxBuild):
        self._init_command_args()
        self.task.command_args['boxbuild'] = True
        self.task.command_args['--box'] = 'universal'
        self.task.command_args['--9p-sharing'] = True
        box_build = Mock()
        mock_BoxBuild.return_value = box_build
        self.task.process()
        mock_BoxBuild.assert_called_once_with(
            boxname='universal', ram=None, console=None, smp=None, arch='',
            machine=None, cpu='host', sharing_backend='9p',
            ssh_key='id_rsa', ssh_port='22', accel=True
        )
        self.task.command_args['--9p-sharing'] = False
        self.task.command_args['--virtiofs-sharing'] = True
        mock_BoxBuild.reset_mock()
        self.task.process()
        mock_BoxBuild.assert_called_once_with(
            boxname='universal', ram=None, console=None, smp=None, arch='',
            machine=None, cpu='host', sharing_backend='virtiofs',
            ssh_key='id_rsa', ssh_port='22', accel=True
        )
        self.task.command_args['--9p-sharing'] = False
        self.task.command_args['--virtiofs-sharing'] = False
        self.task.command_args['--sshfs-sharing'] = True
        mock_BoxBuild.reset_mock()
        self.task.process()
        mock_BoxBuild.assert_called_once_with(
            boxname='universal', ram=None, console=None, smp=None, arch='',
            machine=None, cpu='host', sharing_backend='sshfs',
            ssh_key='id_rsa', ssh_port='22', accel=True
        )
