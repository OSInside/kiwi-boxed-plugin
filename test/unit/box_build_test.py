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
        self.box.fetch.return_value = self.vm_setup
        mock_BoxDownload.return_value = self.box
        self.build = BoxBuild('suse', 'x86_64')

    @patch('kiwi_boxed_plugin.box_build.Command.call')
    @patch('os.environ')
    def test_run(self, mock_os_environ, mock_Command_call):
        self.build.run(
            {
                '--type': 'vmx',
                'system': None,
                'build': None,
                '--description': 'desc',
                '--target-dir': 'target'
            }
        )
        mock_Command_call.assert_called_once_with(
            [
                'qemu-system-x86_64',
                '-machine', 'accel=kvm',
                '-cpu', 'host',
                '-nographic',
                '-nodefaults',
                '-snapshot',
                '-kernel', 'kernel',
                '-append', 'append kiwi="--type vmx system build"',
                '-drive', 'file=system,if=virtio,driver=qcow2,'
                'cache=off,snapshot=on',
                '-netdev', 'user,id=user0',
                '-device', 'virtio-net-pci,netdev=user0',
                '-device', 'virtio-serial',
                '-chardev', 'stdio,id=virtiocon0',
                '-device', 'virtconsole,chardev=virtiocon0',
                '-fsdev', 'local,security_model=mapped,id=fsdev0,path=desc',
                '-device', 'virtio-9p-pci,id=fs0,fsdev=fsdev0,'
                'mount_tag=kiwidescription',
                '-fsdev', 'local,security_model=mapped,id=fsdev1,path=target',
                '-device', 'virtio-9p-pci,id=fs1,fsdev=fsdev1,'
                'mount_tag=kiwibundle'
            ], {'TMPDIR': '/var/tmp/kiwi/boxes'}
        )
