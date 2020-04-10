#!/bin/bash

# due to the Release setup in the prjconf the names of the images
# do not change its name. Thus we can do a simple mapping in the
# plugin. The update check should be based on the contents of the
# .packages file
uri=https://download.opensuse.org/repositories/Virtualization:/Appliances:/SelfContained:/fedora/images

kernel=Fedora-Box.x86_64-1.1.2-Kernel-BuildBox.tar.xz
image=Fedora-Box.x86_64-1.1.2-System-BuildBox.qcow2

mkdir -p fedora
pushd fedora

curl --progress-bar -L --output kernel.tar.xz ${uri}/${kernel}
curl --progress-bar -L --output system.qcow2 ${uri}/${image}

popd

tar -C fedora \
    --transform "s/.*/kernel/" \
    --wildcards -xf fedora/kernel.tar.xz "*.kernel"

tar -C fedora \
    --transform "s/.*/initrd/" \
    --wildcards -xf fedora/kernel.tar.xz "*.initrd.xz"
