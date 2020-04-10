# Copyright (c) 2020 SUSE Software Solutions Germany GmbH.  All rights reserved.
#
# This file is part of kiwi-boxed-build.
#
# kiwi-boxed-build is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kiwi-boxed-build is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kiwi-boxed-build.  If not, see <http://www.gnu.org/licenses/>
#
import os
import logging
from collections import namedtuple
from kiwi.command import Command
from kiwi.utils.checksum import Checksum
from kiwi.solver.repository import SolverRepository
from kiwi.system.uri import Uri
from kiwi.path import Path

from kiwi_boxed_plugin.box_config import BoxConfig
from kiwi_boxed_plugin.defaults import Defaults

log = logging.getLogger('kiwi')


class BoxDownload:
    """
    **Implements download of box file(s)**

    Reads the box configuration file and provides an interface
    to download the box files according to the configuration
    """
    def __init__(self, boxname):
        self.box_config = BoxConfig(boxname)
        self.box_dir = os.sep.join(
            [Defaults.get_local_box_cache_dir(), boxname]
        )
        self.vm_setup_type = namedtuple(
            'vm_setup_type', [
                'system', 'kernel', 'initrd'
            ]
        )
        self.system = None
        self.kernel = None
        self.initrd = None
        Path.create(self.box_dir)

    def fetch(self, update_check=True):
        download = update_check
        repo_source = self.box_config.get_box_source()
        if repo_source:
            repo = SolverRepository(
                Uri(repo_source, 'rpm-md')
            )
            packages_file = self.box_config.get_box_packages_file()
            if update_check and packages_file:
                local_packages_file = os.sep.join(
                    [self.box_dir, packages_file]
                )
                repo.download_from_repository(
                    packages_file, local_packages_file
                )
                if self._remote_content_unchanged(local_packages_file):
                    download = False
                else:
                    self._create_packages_checksum(local_packages_file)

            for box_file in self.box_config.get_box_files():
                local_box_file = os.sep.join([self.box_dir, box_file])
                if not os.path.exists(local_box_file):
                    download = True
                if download:
                    log.info('Downloading {0}'.format(box_file))
                    repo.download_from_repository(
                        box_file, local_box_file
                    )
                if box_file.endswith('.qcow2'):
                    self.system = local_box_file
                if box_file.endswith('.tar.xz'):
                    self.kernel = self._extract_kernel_from_tarball(
                        local_box_file
                    )
                    self.initrd = self._extract_initrd_from_tarball(
                        local_box_file
                    )
        return self.vm_setup_type(
            system=self.system,
            kernel=self.kernel,
            initrd=self.initrd
        )

    def _create_packages_checksum(self, filename):
        checksum = Checksum(filename)
        with open(filename + '.sha256', 'w') as shasum:
            shasum.write(checksum.sha256())

    def _extract_kernel_from_tarball(self, tarfile):
        Command.run(
            [
                'tar', '-C', self.box_dir, '--transform', 's/.*/kernel/',
                '--wildcards', '-xf', tarfile, '*.kernel'
            ]
        )
        return os.sep.join([self.box_dir, 'kernel'])

    def _extract_initrd_from_tarball(self, tarfile):
        Command.run(
            [
                'tar', '-C', self.box_dir, '--transform', 's/.*/initrd/',
                '--wildcards', '-xf', tarfile, '*.initrd.xz'
            ]
        )
        return os.sep.join([self.box_dir, 'initrd'])

    def _remote_content_unchanged(self, filename):
        shasum_file = filename + '.sha256'
        checksum = Checksum(filename)
        return checksum.matches(
            checksum.sha256(), shasum_file
        )
