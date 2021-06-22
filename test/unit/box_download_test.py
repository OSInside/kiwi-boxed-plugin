import io
from mock import (
    patch, Mock, MagicMock, call
)

from kiwi_boxed_plugin.box_download import BoxDownload


class TestBoxDownload:
    @patch('kiwi_boxed_plugin.defaults.Defaults.get_plugin_config_file')
    @patch('kiwi_boxed_plugin.box_download.Path')
    @patch('kiwi_boxed_plugin.box_download.DirFiles')
    def setup(self, mock_DirFiles, mock_Path, mock_get_plugin_config_file):
        self.box_stage = Mock()
        mock_DirFiles.return_value = self.box_stage
        mock_get_plugin_config_file.return_value = \
            '../data/kiwi_boxed_plugin.yml'
        with patch.dict('os.environ', {'HOME': 'HOME'}):
            self.box = BoxDownload('suse', 'x86_64')
        mock_Path.create.assert_called_once_with(
            'HOME/.kiwi_boxes/suse'
        )
        self.result = self.box.vm_setup_type(
            system='HOME/.kiwi_boxes/suse/'
            'SUSE-Box.x86_64-1.42.1-System-BuildBox.qcow2',
            kernel='HOME/.kiwi_boxes/suse/kernel.x86_64',
            initrd='HOME/.kiwi_boxes/suse/initrd.x86_64',
            append='console=hvc0 root=/dev/vda1 rd.plymouth=0',
            ram=8096,
            smp=4
        )

    @patch('kiwi_boxed_plugin.box_download.Command.run')
    @patch('kiwi_boxed_plugin.box_download.Uri')
    @patch('kiwi_boxed_plugin.box_download.SolverRepository.new')
    @patch('kiwi_boxed_plugin.box_download.Checksum')
    @patch('os.path.exists')
    def test_fetch_checksum_did_not_match(
        self, mock_os_path_exist, mock_Checksum, mock_SolverRepository,
        mock_Uri, mock_Command_run
    ):
        checksum = Mock()
        checksum.matches.return_value = False
        checksum.sha256.return_value = 'sum'
        mock_Checksum.return_value = checksum
        repo = Mock()
        mock_SolverRepository.return_value = repo
        mock_os_path_exist.return_value = False
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=io.IOBase)
            file_handle = mock_open.return_value.__enter__.return_value
            with patch.dict('os.environ', {'HOME': 'HOME'}):
                assert self.box.fetch(update_check=True) == self.result
            assert self.box_stage.register.call_args_list == [
                call(
                    'HOME/.kiwi_boxes/suse/'
                    'SUSE-Box.x86_64-1.42.1-System-BuildBox.report'
                ),
                call(
                    'HOME/.kiwi_boxes/suse/'
                    'SUSE-Box.x86_64-1.42.1-System-BuildBox.report.sha256'
                ),
                call(
                    'HOME/.kiwi_boxes/suse/'
                    'SUSE-Box.x86_64-1.42.1-Kernel-BuildBox.tar.xz'
                ),
                call(
                    'HOME/.kiwi_boxes/suse/'
                    'SUSE-Box.x86_64-1.42.1-System-BuildBox.qcow2'
                )
            ]
            mock_open.assert_called_once_with(
                self.box_stage.register.return_value, 'w'
            )
            file_handle.write.assert_called_once_with('sum')
            assert repo.download_from_repository.call_args_list == [
                call(
                    'SUSE-Box.x86_64-1.42.1-System-BuildBox.report',
                    self.box_stage.register.return_value
                ),
                call(
                    'SUSE-Box.x86_64-1.42.1-Kernel-BuildBox.tar.xz',
                    self.box_stage.register.return_value
                ),
                call(
                    'SUSE-Box.x86_64-1.42.1-System-BuildBox.qcow2',
                    self.box_stage.register.return_value
                )
            ]
            self.box_stage.commit.assert_called_once_with()
            assert mock_Command_run.call_args_list == [
                call(
                    [
                        'tar', '-C', 'HOME/.kiwi_boxes/suse',
                        '--transform', 's/.*/kernel.x86_64/',
                        '--wildcards', '-xf',
                        'HOME/.kiwi_boxes/suse/'
                        'SUSE-Box.x86_64-1.42.1-Kernel-BuildBox.tar.xz',
                        '*.kernel'
                    ]
                ),
                call(
                    [
                        'tar', '-C', 'HOME/.kiwi_boxes/suse',
                        '--transform', 's/.*/initrd.x86_64/',
                        '--wildcards', '-xf',
                        'HOME/.kiwi_boxes/suse/'
                        'SUSE-Box.x86_64-1.42.1-Kernel-BuildBox.tar.xz',
                        '*.initrd.xz'
                    ]
                )
            ]

    @patch('kiwi_boxed_plugin.box_download.Command.run')
    @patch('kiwi_boxed_plugin.box_download.Uri')
    @patch('kiwi_boxed_plugin.box_download.SolverRepository.new')
    @patch('kiwi_boxed_plugin.box_download.Checksum')
    @patch('os.path.exists')
    def test_fetch_checksum_matches(
        self, mock_os_path_exist, mock_Checksum, mock_SolverRepository,
        mock_Uri, mock_Command_run
    ):
        checksum = Mock()
        checksum.matches.return_value = True
        checksum.sha256.return_value = 'sum'
        mock_Checksum.return_value = checksum
        repo = Mock()
        mock_SolverRepository.return_value = repo
        mock_os_path_exist.return_value = True
        assert self.box.fetch(update_check=True) == self.result
        repo.download_from_repository.assert_called_once_with(
            'SUSE-Box.x86_64-1.42.1-System-BuildBox.report',
            self.box_stage.register.return_value
        )

    @patch('kiwi_boxed_plugin.box_download.Command.run')
    @patch('kiwi_boxed_plugin.box_download.Uri')
    @patch('kiwi_boxed_plugin.box_download.SolverRepository.new')
    @patch('kiwi_boxed_plugin.box_download.Checksum')
    @patch('os.path.exists')
    def test_fetch_update_check_disabled(
        self, mock_os_path_exist, mock_Checksum, mock_SolverRepository,
        mock_Uri, mock_Command_run
    ):
        mock_os_path_exist.return_value = True
        assert self.box.fetch(update_check=False) == self.result
