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
            break
        fi
        echo "Waiting for link up on lan0..."
        check=$((check + 1))
        sleep "${sleep_timeout}"
    done
}

wait_network

if grep -q kiwi-version /proc/cmdline; then
    kiwi_version=$(sed -s "s@.*kiwi-version=_\(.*\)_.*@\1@" /proc/cmdline)
    if pip3 install kiwi=="${kiwi_version}"; then
        run_build
    fi
else
    run_build
fi

if ! grep -q kiwi-no-halt /proc/cmdline; then
    halt -p
fi
