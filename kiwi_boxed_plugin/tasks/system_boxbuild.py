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
"""
usage: kiwi-ng system boxbuild -h | --help
       kiwi-ng system boxbuild --boxname=<name> --buildparams=<params>

commands:
    boxbuild
        build a system image in a self contained virtual machine

options:
    --boxname=<name>
        Name of the virtual machine that should be used for
        the build process. Available machines can be looked
        up at: https://build.opensuse.org/project/show/Virtualization:Appliances:SelfContained

    --buildparams=<params>
        List of command parameters as supported by the kiwi-ng
        build command. The information given here is passed
        along to the kiwi-ng system build command running in
        the virtual machine.
"""
from kiwi.tasks.base import CliTask
from kiwi.help import Help

class SystemBoxbuildTask(CliTask):
    def process(self):
        self.manual = Help()
        if self.command_args.get('help') is True:
            return self.manual.show('kiwi::system::boxbuild')

        print(
            'https://genius.com/Frankie-goes-to-hollywood-relax-lyrics'
        )
