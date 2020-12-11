from mock import (
    patch, Mock
)

from kiwi_boxed_plugin.box_build import BoxBuild


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

    @patch('os.environ')
    @patch('os.system')
    @patch('kiwi_boxed_plugin.box_build.Path.create')
    def test_run(self, mock_path_create, mock_os_system, mock_os_environ):
        self.build.run(
            [
                '--type', 'oem', 'system', 'build',
                '--description', 'desc', '--target-dir', 'target'
            ],
            keep_open=True,
            kiwi_version='9.22.1'
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
            ' kiwi-no-halt kiwi-version=_9.22.1_" '
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
            '-initrd initrd '
            '-smp 4'
        )
