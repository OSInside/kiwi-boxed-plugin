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
systemctl enable sshd
systemctl enable kiwi

#======================================
# lvmetad sucks for building lvm images
#--------------------------------------
systemctl disable lvm2-lvmetad
systemctl mask lvm2-lvmetad
systemctl disable lvm2-lvmetad.socket
systemctl mask lvm2-lvmetad.socket

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
        cat >>/etc/bashrc <<-EOF

		journalctl -u kiwi -f
		EOF
        chmod 755 /etc/bashrc

        # Disable services not useful in a container
        systemctl disable sshd
        systemctl disable systemd-networkd
        systemctl disable systemd-resolved

        # Mask services not useful in a container
        systemctl mask sys-kernel-config.mount
        systemctl mask sys-kernel-debug.mount
        systemctl mask sys-kernel-tracing.mount
        systemctl mask systemd-resolved
        systemctl mask systemd-networkd
        systemctl mask systemd-modules-load
    fi
done
