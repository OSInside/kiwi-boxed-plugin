#!/bin/bash

# due to the Release setup in the prjconf the names of the images
# do not change its name. Thus we can do a simple mapping in the
# plugin. The update check should be based on the contents of the
# .packages file
uri=https://download.opensuse.org/repositories/Virtualization:/Appliances:/SelfContained/images

kernel=SUSE-Box.x86_64-1.42.1-Kernel-BuildBox.tar.xz
image=SUSE-Box.x86_64-1.42.1-System-BuildBox.qcow2

mkdir -p binaries
pushd binaries

curl --progress-bar -L --output kernel.tar.xz ${uri}/${kernel}
curl --progress-bar -L --output system.qcow2 ${uri}/${image}

popd

tar -C binaries \
    --transform "s/.*/kernel/" \
    --wildcards -xf binaries/kernel.tar.xz "*.kernel"
