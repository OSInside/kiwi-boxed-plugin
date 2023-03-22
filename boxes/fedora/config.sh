#!/bin/bash

set -ex

test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile

#======================================
# Setup default target, multi-user
#--------------------------------------
baseSetRunlevel 3

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
baseInsertService sshd
baseInsertService kiwi

#======================================
# Fedora uses systemd-resolved for DNS
#--------------------------------------
systemctl enable systemd-resolved
