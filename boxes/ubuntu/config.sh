#!/bin/bash
set -eux

#==================================
# Disable services
#----------------------------------
systemctl mask systemd-logind.service
systemctl mask systemd-update-utmp.service
systemctl mask auditd.service
systemctl mask systemd-update-utmp-runlevel.service
systemctl mask systemd-user-sessions.service

#======================================
# Activate kiwi service
#--------------------------------------
systemctl enable systemd-networkd
systemctl enable systemd-resolved
systemctl enable ssh
systemctl enable kiwi

#======================================
# Setup container
#--------------------------------------
for profile in ${kiwi_profiles//,/ }; do
    if [ "${profile}" = "Container" ]; then
        # Add cache dir
        mkdir -p /var/cache/kiwi

        # Setup kpartx for container build
        cat >>/etc/kiwi.yml <<-EOF

		mapper:
		  - part_mapper: kpartx
		EOF

        # Create login call
        cat >/root/.bashrc <<-EOF
		journalctl -u kiwi -f
		EOF
        chmod 755 /root/.bashrc

        # Disable services not useful in a container
        systemctl disable ssh
        systemctl disable systemd-networkd
        systemctl disable systemd-resolved

        # Mask services not useful in a container
        systemctl mask sound.target
        systemctl mask sys-kernel-config.mount
        systemctl mask sys-kernel-debug.mount
        systemctl mask sys-kernel-tracing.mount
        systemctl mask systemd-resolved
        systemctl mask systemd-networkd
        systemctl mask systemd-modules-load
    fi
done
