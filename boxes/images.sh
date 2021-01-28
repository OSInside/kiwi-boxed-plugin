#!/bin/bash

run_kiwi=/usr/local/bin/run_kiwi

tail -n +9 "$0" >"${run_kiwi}" && chmod 755 "${run_kiwi}"

exit $?
# The code of interest starts here
#!/bin/bash

set -x

exec &>/dev/console

function run_build {
    # """
    # Run kiwi and the bundler
    # """
    local options
    local logfile=/bundle/result.log
    rm -rf /result
    options=$(cut -f2 -d\" /proc/cmdline)
    options="${options} --description /description --target-dir /result"
    if kiwi-ng --logfile "${logfile}" ${options}; then
        kiwi-ng result bundle --id 0 --target-dir /result --bundle-dir /bundle
    fi
}

function wait_network {
    # """
    # even though this program is called in a systemd unit that
    # requires the network-online target there could be a delay
    # in the network online status between the host and the guest.
    # This means the guest could be online while the host/guest
    # network negotiation is still not done.
    # """
    local sleep_timeout=2
    local retry_count=5
    local check=0
    echo "Waiting for link up on lan0..."
    while true;do
        if ip link ls lan0 | grep -qi "state UP"; then
            # interface link is up
            break
        fi
        if [ "${check}" -eq "${retry_count}" ];then
            # interface link did not came up
            exit 1
        fi
        echo "Waiting for link up on lan0..."
        check=$((check + 1))
        sleep "${sleep_timeout}"
    done
}

function mount_shared_path {
    # """
    # mount shared host path identified by given mount tag
    # """
    local path=$1
    local tag=$2
    local backend
    if mountpoint -q "${path}"; then
        return
    fi
    mkdir -p "${path}"
    backend=$(sed -s "s@.*sharing-backend=_\(.*\)_.*@\1@" /proc/cmdline)
    if [ "${backend}" = "virtiofs" ];then
        mount -t virtiofs "${tag}" "${path}"
    else
        mount -t 9p -o "trans=virtio,version=9p2000.L" "${tag}" "${path}"
    fi
}

function finish {
    if ! grep -q kiwi-no-halt /proc/cmdline; then
        halt -p
    fi
}

# main
trap finish EXIT

wait_network

if ! mount_shared_path "/description" "kiwidescription"; then
    exit 1
fi

if ! mount_shared_path "/bundle" "kiwibundle"; then
    exit 1
fi

if grep -q custom-mount /proc/cmdline; then
    custom_path=$(sed -s "s@.*custom-mount=_\(.*\)_.*@\1@" /proc/cmdline)
    if ! mount_shared_path "${custom_path}" "custompath"; then
        exit 1
    fi
fi

if grep -q kiwi-version /proc/cmdline; then
    kiwi_version=$(sed -s "s@.*kiwi-version=_\(.*\)_.*@\1@" /proc/cmdline)
    if ! pip3 install kiwi=="${kiwi_version}"; then
        exit 1
    fi
fi

run_build
