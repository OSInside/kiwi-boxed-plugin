#!/bin/bash

# load.sh provided those (fetcher in the plugin)
image=fedora/system.qcow2
kernel=fedora/kernel
initrd=fedora/initrd

# user specified data
description_dir=/home/ms/Project/kiwi-descriptions/fedora/x86_64/fedora-30.0-JeOS
bundle_dir=/tmp/mytest

mkdir -p "${bundle_dir}"

# no description and target-dir, this comes from shared folders and is
# setup in the run_kiwi script inside the VM 
kiwi_options="--type iso system build"

# For debugging the VM pass "kiwi-no-halt", this will prevent reboot
qemu-kvm -m 8096 \
    -nographic \
    -nodefaults \
    -snapshot \
    -kernel "${kernel}" \
    -initrd "${initrd}" \
    -append "root=/dev/vda1 console=hvc0 rd.plymouth=0 kiwi=\"${kiwi_options}\"" \
    -drive file="${image}",if=virtio,driver=qcow2,snapshot=on \
    -netdev user,id=user0 \
    -device virtio-net-pci,netdev=user0 \
    -fsdev local,security_model=mapped,id=fsdev0,path="${description_dir}" \
    -device virtio-9p-pci,id=fs0,fsdev=fsdev0,mount_tag=kiwidescription \
    -fsdev local,security_model=mapped,id=fsdev1,path="${bundle_dir}" \
    -device virtio-9p-pci,id=fs1,fsdev=fsdev1,mount_tag=kiwibundle \
    -device virtio-serial -chardev stdio,id=virtiocon0 \
    -device virtconsole,chardev=virtiocon0
