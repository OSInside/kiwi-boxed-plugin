# Copyright (c) 2024 SUSE LLC.  All rights reserved.
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
import typer
import itertools
from pathlib import Path
from typing import (
    Annotated, Optional, List, Union, no_type_check
)

typers = {
    'boxbuild': typer.Typer(
        add_completion=False, invoke_without_command=True
    )
}

system = typers['boxbuild']


@no_type_check
@system.command(
    context_settings={
        'allow_extra_args': True,
        'ignore_unknown_options': True
    }
)
def kiwi(
    ctx: typer.Context
):
    """
    List of command parameters as supported by the kiwi-ng
    build command. The information given here is passed
    along to the kiwi-ng system build command running in
    the virtual machine or container.
    """
    Cli = ctx.obj
    args = ctx.args
    for option in list(set(args)):
        if type(option) is not str or not option.startswith('-'):
            continue
        k: List[Union[str, List]] = [option]
        v = []
        indexes = [n for n, x in enumerate(args) if x == option]
        if len(indexes) > 1:
            for index in indexes:
                v.append(args[index + 1])
            for index in sorted(indexes, reverse=True):
                del args[index + 1]
                del args[index]
            k.append(v)
            args += k
    Cli.subcommand_args['boxbuild']['system_build'] = \
        dict(itertools.zip_longest(*[iter(args)] * 2))
    Cli.global_args['command'] = 'boxbuild'
    Cli.global_args['system'] = True
    Cli.cli_ok = True


@system.callback(
    help='build a system image in a self contained VM or container',
    subcommand_metavar='kiwi [OPTIONS]'
)
def boxbuild(
    ctx: typer.Context,
    box: Annotated[
        Optional[str], typer.Option(
            help='<name> Name of the box to use for the build process.'
        )
    ] = None,
    list_boxes: Annotated[
        Optional[bool], typer.Option(
            '--list-boxes',
            help='show available build boxes.'
        )
    ] = False,
    box_memory: Annotated[
        Optional[str], typer.Option(
            help='<vmgb> Number of GBs to reserve as main memory '
            'for the virtual machine. By default 8GB will be used.'
        )
    ] = None,
    box_console: Annotated[
        Optional[str], typer.Option(
            help='<ttyname> Name of console in the kernel settings '
            'for the virtual machine. By default set to hvc0.'
        )
    ] = None,
    box_smp_cpus: Annotated[
        Optional[int], typer.Option(
            help='<number> Number of CPUs to use in the SMP setup. '
            'By default 4 CPUs will be used.'
        )
    ] = 4,
    box_debug: Annotated[
        Optional[bool], typer.Option(
            '--box-debug',
            help='In debug mode the started virtual machine will be kept open.'
        )
    ] = False,
    container: Annotated[
        Optional[bool], typer.Option(
            '--container',
            help='Build in container instead of a VM. Options related to '
            'building in a VM will have no effect.'
        )
    ] = False,
    kiwi_version: Annotated[
        Optional[str], typer.Option(
            help='<version> Specify a KIWI version to use for '
            'the build. The referenced KIWI will be fetched from '
            'pip and replaces the box installed KIWI version. '
            'Note: If --no-snapshot is used in combination '
            'with this option, the change of the KIWI version will '
            'be permanently stored in the used box.'
        )
    ] = None,
    shared_path: Annotated[
        Optional[Path], typer.Option(
            help='<path> Optional host path to share with the box. '
            'The same path as it is present on the host will also '
            'be available inside of the box during build time.'
        )
    ] = None,
    no_update_check: Annotated[
        Optional[bool], typer.Option(
            '--no-update-check',
            help='Skip check for available box update. The option '
            'has no effect if the selected box does not yet exist '
            'on the host.'
        )
    ] = False,
    no_snapshot: Annotated[
        Optional[bool], typer.Option(
            '--no-snapshot',
            help='Run box with snapshot mode switched off. This '
            'causes the box disk file to be modified by the build '
            'process and allows to keep a persistent package cache '
            'as part of the box. The option can be used to increase '
            'the build performance due to data stored in the box '
            'which does not have to be reloaded from the network. '
            'On the contrary this option invalidates the immutable '
            'box attribute and should be used with care. On update '
            'of the box all data stored will be wiped. To prevent '
            'this combine the option with the --no-update-check option.'
        )
    ] = False,
    no_accel: Annotated[
        Optional[bool], typer.Option(
            '--no-accel',
            help='Run box without hardware acceleration. By default '
            'KVM acceleration is activated'
        )
    ] = False,
    qemu_9p_sharing: Annotated[
        Optional[bool], typer.Option(
            '--9p-sharing',
            help='Select 9p backend to use for sharing data '
            'between the host and the box.'
        )
    ] = False,
    virtiofs_sharing: Annotated[
        Optional[bool], typer.Option(
            '--virtiofs-sharing',
            help='Select virtiofsd backend to use for sharing data '
            'between the host and the box.'
        )
    ] = False,
    sshfs_sharing: Annotated[
        Optional[bool], typer.Option(
            '--sshfs-sharing',
            help='Select sshfs backend to use for sharing data '
            'between the host and the box.'
        )
    ] = False,
    ssh_key: Annotated[
        Optional[str], typer.Option(
            help='<name> Name of ssh key to authorize for '
            'connection. By default id_rsa is used.'
        )
    ] = 'id_rsa',
    ssh_port: Annotated[
        Optional[int], typer.Option(
            help='<port> Port number to use to forward the '
            'guest SSH port to the host By default 10022 is used.'
        )
    ] = 10022,
    x86_64: Annotated[
        Optional[bool], typer.Option(
            '--x86_64',
            help='Select box for the x86_64 architecture. If no '
            'architecture is selected the host architecture is '
            'used for selecting the box. The selected box '
            'architecture also specifies the target architecture '
            'for the image build with that box.'
        )
    ] = False,
    aarch64: Annotated[
        Optional[bool], typer.Option(
            '--aarch64',
            help='Select box for the aarch64 architecture. If no '
            'architecture is selected the host architecture is '
            'used for selecting the box. The selected box '
            'architecture also specifies the target architecture '
            'for the image build with that box.'
        )
    ] = False,
    machine: Annotated[
        Optional[str], typer.Option(
            help='<qemu_machine> Machine name used '
            'by QEMU. By default no specific value is used here '
            'and qemu selects its default machine type. For cross '
            'arch builds or for system architectures for which '
            'QEMU defines no default like for Arm, it is required '
            'to specify a machine name. If you do not care about '
            'reproducing the idiosyncrasies of a particular bit '
            'of hardware, the best option is to use the virt '
            'machine type.'
        )
    ] = None,
    cpu: Annotated[
        Optional[str], typer.Option(
            help='<qemu_cpu> CPU type used by QEMU. By default '
            'the host CPU type is used which is only a good '
            'selection if the host and the selected box are from '
            'the same architecture. On cross arch builds it is '
            'required to specify the CPU emulation the box should use'
        )
    ] = None
):
    Cli = ctx.obj
    Cli.subcommand_args['boxbuild'] = {
        '--box': box,
        '--list-boxes': list_boxes,
        '--box-memory': box_memory,
        '--box-console': box_console,
        '--box-smp-cpus': f'{box_smp_cpus}',
        '--box-debug': box_debug,
        '--container': container,
        '--kiwi-version': kiwi_version,
        '--shared-path': shared_path,
        '--no-update-check': no_update_check,
        '--no-snapshot': no_snapshot,
        '--no-accel': no_accel,
        '--9p-sharing': qemu_9p_sharing,
        '--virtiofs-sharing': virtiofs_sharing,
        '--sshfs-sharing': sshfs_sharing,
        '--ssh-key': ssh_key,
        '--ssh-port': f'{ssh_port}',
        '--x86_64': x86_64,
        '--aarch64': aarch64,
        '--machine': machine,
        '--cpu': cpu,
        'help': False
    }
    Cli.global_args['command'] = 'boxbuild'
    Cli.global_args['system'] = True
    Cli.cli_ok = True
