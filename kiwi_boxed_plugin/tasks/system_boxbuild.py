"""
usage: kiwi-ng system boxbuild -h | --help
       kiwi-ng system boxbuild --boxname=<name> --buildparams=<params>
           [--host-bridge-interface=<interface>]

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
        along 1:1 to the kiwi-ng system build command
        running in the virtual machine.

    --host-bridge-interface=<interface>
        Name of the bridge interface on the host that allows for
        outgoing connections.
        
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
