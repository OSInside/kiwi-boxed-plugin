#!/bin/bash

# load.sh provided those (fetcher in the plugin)
image=suse/system.qcow2
kernel=suse/kernel

# user specified data
description_dir=/home/ms/Project/kiwi-descriptions/suse/x86_64/suse-leap-15.1-JeOS
bundle_dir=/tmp/mytest

maxmem=4G

mkdir -p "${bundle_dir}"

# no description and target-dir, this comes from shared folders and is
# setup in the run_kiwi script inside the VM 
kiwi_options="--type vmx system build"

# For debugging the VM pass "kiwi-no-halt", this will prevent reboot
qemu-kvm \
    -m ${maxmem} \
    -cpu host \
    -nographic \
    -nodefaults \
    -snapshot \
    -kernel "${kernel}" \
    -append "root=/dev/vda1 console=hvc0 rd.plymouth=0 kiwi=\"${kiwi_options}\"" \
    -drive file="${image}",if=virtio,driver=qcow2,cache=off,snapshot=on \
    -netdev user,id=user0 \
    -device virtio-net-pci,netdev=user0 \
    -fsdev local,security_model=mapped,id=fsdev0,path="${description_dir}" \
    -device virtio-9p-pci,id=fs0,fsdev=fsdev0,mount_tag=kiwidescription \
    -fsdev local,security_model=mapped,id=fsdev1,path="${bundle_dir}" \
    -device virtio-9p-pci,id=fs1,fsdev=fsdev1,mount_tag=kiwibundle \
    -device virtio-serial -chardev stdio,id=virtiocon0 \
    -device virtconsole,chardev=virtiocon0
