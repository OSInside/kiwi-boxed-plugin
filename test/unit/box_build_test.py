from mock import (
    patch, Mock, call
)
from pytest import raises

from kiwi_boxed_plugin.box_build import BoxBuild
import kiwi_boxed_plugin.defaults as defaults

from kiwi_boxed_plugin.exceptions import KiwiBoxPluginVirtioFsError


class TestBoxBuild:
    @patch('kiwi_boxed_plugin.box_build.BoxDownload')
    def setup(self, mock_BoxDownload):
        self.box = Mock()
        self.vm_setup = Mock()
        self.vm_setup.kernel = 'kernel'
        self.vm_setup.append = 'append'
        self.vm_setup.system = 'system'
        self.vm_setup.initrd = 'initrd'
        self.vm_setup.ram = 4096
        self.vm_setup.smp = 4
        self.box.fetch.return_value = self.vm_setup
        mock_BoxDownload.return_value = self.box
        self.build = BoxBuild(
            boxname='suse', arch='x86_64'
        )
        self.build_arm = BoxBuild(
            boxname='universal', arch='aarch64',
            machine='virt', cpu='cortex-a57'
        )

    @patch('os.environ')
    @patch('os.system')
    @patch('kiwi_boxed_plugin.box_build.Path.create')
    def test_run_with_9p_sharing(
        self, mock_path_create, mock_os_system, mock_os_environ
    ):
        self.build.run(
            [
                '--type', 'oem', 'system', 'build',
                '--description', 'desc', '--target-dir', 'target'
            ],
            keep_open=True,
            kiwi_version='9.22.1',
            custom_shared_path='/var/tmp/repos'
        )
        mock_path_create.assert_called_once_with('target')
        mock_os_system.assert_called_once_with(
            'qemu-system-x86_64 '
            '-m 4096 '
            '-machine accel=kvm '
            '-cpu host '
            '-nographic '
            '-nodefaults '
            '-snapshot '
            '-kernel kernel '
            '-append "append kiwi=\\"--type oem system build\\"'
            ' kiwi-no-halt kiwi-version=_9.22.1_'
            ' custom-mount=_/var/tmp/repos_'
            ' sharing-backend=_9p_" '
            '-drive file=system,if=virtio,driver=qcow2,cache=off,snapshot=on '
            '-netdev user,id=user0 '
            '-device virtio-net-pci,netdev=user0 '
            '-device virtio-serial '
            '-chardev stdio,id=virtiocon0 '
            '-device virtconsole,chardev=virtiocon0 '
            '-fsdev local,security_model=mapped,id=fsdev0,path=desc '
            '-device virtio-9p-pci,id=fs0,fsdev=fsdev0,mount_tag='
            'kiwidescription '
            '-fsdev local,security_model=mapped,id=fsdev1,path=target '
            '-device virtio-9p-pci,id=fs1,fsdev=fsdev1,mount_tag='
            'kiwibundle '
            '-fsdev local,security_model=mapped,id=fsdev2,path=/var/tmp/repos '
            '-device virtio-9p-pci,id=fs2,fsdev=fsdev2,mount_tag='
            'custompath '
            '-initrd initrd '
            '-smp 4'
        )

    @patch('os.environ')
    @patch('os.system')
    @patch('kiwi_boxed_plugin.box_build.Path.create')
    def test_run_cross_arch_aarch64_on_x86_64(
        self, mock_path_create, mock_os_system, mock_os_environ
    ):
        self.build_arm.run(
            [
                '--type', 'oem', 'system', 'build',
                '--description', 'desc', '--target-dir', 'target'
            ],
            keep_open=True,
            kiwi_version='9.22.1',
            custom_shared_path='/var/tmp/repos'
        )
        mock_path_create.assert_called_once_with('target')
        mock_os_system.assert_called_once_with(
            'qemu-system-aarch64 '
            '-m 4096 '
            '-machine virt '
            '-cpu cortex-a57 '
            '-nographic '
            '-nodefaults '
            '-snapshot '
            '-kernel kernel '
            '-append "append kiwi=\\"--type oem system build\\"'
            ' kiwi-no-halt kiwi-version=_9.22.1_'
            ' custom-mount=_/var/tmp/repos_'
            ' sharing-backend=_9p_" '
            '-drive file=system,if=virtio,driver=qcow2,cache=off,snapshot=on '
            '-netdev user,id=user0 '
            '-device virtio-net-pci,netdev=user0 '
            '-device virtio-serial '
            '-chardev stdio,id=virtiocon0 '
            '-device virtconsole,chardev=virtiocon0 '
            '-fsdev local,security_model=mapped,id=fsdev0,path=desc '
            '-device virtio-9p-pci,id=fs0,fsdev=fsdev0,mount_tag='
            'kiwidescription '
            '-fsdev local,security_model=mapped,id=fsdev1,path=target '
            '-device virtio-9p-pci,id=fs1,fsdev=fsdev1,mount_tag='
            'kiwibundle '
            '-fsdev local,security_model=mapped,id=fsdev2,path=/var/tmp/repos '
            '-device virtio-9p-pci,id=fs2,fsdev=fsdev2,mount_tag='
            'custompath '
            '-initrd initrd '
            '-smp 4'
        )

    @patch('os.environ')
    @patch('os.system')
    @patch('subprocess.Popen')
    @patch('kiwi_boxed_plugin.box_build.Path.create')
    @patch('kiwi_boxed_plugin.defaults.Path.which')
    def test_run_with_virtiofs_sharing_raises(
        self, mock_path_which, mock_path_create, mock_subprocess_Popen,
        mock_os_system, mock_os_environ
    ):
        self.build.sharing_backend = 'virtiofs'
        mock_path_which.return_value = None
        with raises(KiwiBoxPluginVirtioFsError):
            self.build.run(
                [
                    '--type', 'oem', 'system', 'build',
                    '--description', 'desc', '--target-dir', 'target'
                ]
            )
        mock_path_which.return_value = 'virtiofsd'
        mock_subprocess_Popen.side_effect = Exception
        with raises(KiwiBoxPluginVirtioFsError):
            self.build.run(
                [
                    '--type', 'oem', 'system', 'build',
                    '--description', 'desc', '--target-dir', 'target'
                ]
            )

    @patch('os.environ')
    @patch('os.system')
    @patch('os.path.abspath')
    @patch('subprocess.Popen')
    @patch('kiwi_boxed_plugin.box_build.Path.create')
    @patch('kiwi_boxed_plugin.defaults.Path.which')
    def test_run_with_virtiofs_sharing(
        self, mock_path_which, mock_path_create, mock_subprocess_Popen,
        mock_os_path_abspath, mock_os_system, mock_os_environ
    ):
        def abs_path(arg):
            return 'abspath/{0}'.format(arg)

        def new_process(self, **args):
            return Mock()

        mock_path_which.return_value = '/usr/libexec/virtiofsd'
        mock_os_path_abspath.side_effect = abs_path
        mock_subprocess_Popen.side_effect = new_process
        self.build.sharing_backend = 'virtiofs'
        self.build.run(
            [
                '--type', 'oem', 'system', 'build',
                '--description', 'desc', '--target-dir', 'target'
            ],
            keep_open=True,
            kiwi_version='9.22.1',
            custom_shared_path='var/tmp/repos'
        )
        mock_path_create.assert_called_once_with('target')
        mock_os_system.assert_called_once_with(
            'qemu-system-x86_64 '
            '-m 4096 '
            '-machine accel=kvm '
            '-cpu host '
            '-nographic '
            '-nodefaults '
            '-snapshot '
            '-kernel kernel '
            '-append "append kiwi=\\"--type oem system build\\"'
            ' kiwi-no-halt kiwi-version=_9.22.1_'
            ' custom-mount=_var/tmp/repos_'
            ' sharing-backend=_virtiofs_" '
            '-drive file=system,if=virtio,driver=qcow2,cache=off,snapshot=on '
            '-netdev user,id=user0 '
            '-device virtio-net-pci,netdev=user0 '
            '-device virtio-serial '
            '-chardev stdio,id=virtiocon0 '
            '-device virtconsole,chardev=virtiocon0 '
            '-chardev socket,id=char0,path=/tmp/vhostqemu_0 '
            '-device vhost-user-fs-pci,queue-size=1024,chardev=char0,tag='
            'kiwidescription '
            '-chardev socket,id=char1,path=/tmp/vhostqemu_1 '
            '-device vhost-user-fs-pci,queue-size=1024,chardev=char1,tag='
            'kiwibundle '
            '-chardev socket,id=char2,path=/tmp/vhostqemu_2 '
            '-device vhost-user-fs-pci,queue-size=1024,chardev=char2,tag='
            'custompath '
            '-object '
            'memory-backend-file,id=mem,size=4096,mem-path=/dev/shm,share=on '
            '-numa node,memdev=mem '
            '-initrd initrd '
            '-smp 4'
        )
        assert mock_subprocess_Popen.call_args_list == [
            call(
                [
                    '/usr/libexec/virtiofsd',
                    '--socket-path=/tmp/vhostqemu_0',
                    '-o', 'allow_root',
                    '-o', 'source=abspath/desc',
                    '-o', 'cache=always'
                ], close_fds=True
            ),
            call(
                [
                    '/usr/libexec/virtiofsd',
                    '--socket-path=/tmp/vhostqemu_1',
                    '-o', 'allow_root',
                    '-o', 'source=abspath/target',
                    '-o', 'cache=always'
                ], close_fds=True
            ),
            call(
                [
                    '/usr/libexec/virtiofsd',
                    '--socket-path=/tmp/vhostqemu_2',
                    '-o', 'allow_root',
                    '-o', 'source=abspath/var/tmp/repos',
                    '-o', 'cache=always'
                ], close_fds=True
            )
        ]
        for virtiofsd_process in defaults.VIRTIOFSD_PROCESS_LIST:
            virtiofsd_process.terminate.assert_called_once_with()
