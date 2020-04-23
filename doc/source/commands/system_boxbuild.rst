kiwi-ng system boxbuild
=======================

SYNOPSIS
--------

.. code:: bash

   kiwi-ng [global options] service <command> [<args>]

   kiwi-ng system boxbuild -h | --help
   kiwi-ng system boxbuild --box=<name>
       [--box-memory=<vmgb>]
       [--box-debug]
       [--no-update-check]
       [--x86_64]
       <kiwi_build_command_args>...
   kiwi-ng system boxbuild --list-boxes
   kiwi-ng system boxbuild help

DESCRIPTION
-----------

build an image in a self contained environment. The `boxbuild`
command uses KVM to start a virtual machine and run the kiwi
build command inside of that virtual machine. The provided
`--description` and `--target-dir` options are setup as shared
folders between the host and the guest. No other data will be
shared with the host which also allows for cross distribution
builds. The boxbuild command provides the following additional
features over the standard build command:

* Build images independent of the host.
* Build images as normal user not as root.
* Build cross distribution images on one host.
* Build in predefined build VMs called boxes which includes
  all components needed to build appliances.

For running the build process in a virtual machine it's required
to provide VM images that are suitable to perform this job. We
call the VM images `boxes` and they contain kiwi itself as well
as all other components needed to build appliances. Those boxes
are hosted in the Open Build Service and are publicly available
on the `Subprojects` tab at:
https://build.opensuse.org/project/show/Virtualization:Appliances:SelfContained

As a user you don't need to work with the boxes because this
is all done by the plugin. The `boxbuild` command knows where to
fetch the box and also cares for an update of the box when it
has changed.

OPTIONS
-------

--box=<name>

  Name of the virtual machine that should be used for
  the build process.

--list-boxes

  show available build boxes.

--box-memory=<vmgb>

  Number of GBs to reserve as main memory for the virtual
  machine. By default 8GB will be used.

--no-update-check

  Skip check for available box update. The option has no
  effect if the selected box does not yet exist on the host.

--x86_64

  Select box for the x86_64 architecture. If no architecture
  is selected the host architecture is used for selecting
  the box. The selected box architecture also specifies the
  target architecture for the image build with that box.

--box-debug

  In debug mode the started virtual machine will be kept open

<kiwi_build_command_args>...

  List of command parameters as supported by the kiwi-ng
  build command. The information given here is passed
  along to the kiwi-ng system build command running in
  the virtual machine. See the Example below how to provide
  options to the build command correctly.

EXAMPLE
-------

.. code:: bash

   $ git clone https://github.com/OSInside/kiwi-descriptions

   $ kiwi --type vmx system boxbuild --box suse -- \
       --description kiwi-descriptions/suse/x86_64/suse-tumbleweed-JeOS \
       --target-dir /tmp/myimage
