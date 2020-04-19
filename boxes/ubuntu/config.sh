#!/bin/bash

set -x

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

#=====================================
# Enable Shared Description directory
#-------------------------------------
mkdir -p /description
systemctl enable description.automount

#==================================
# Enable Shared Bundle Directory
#----------------------------------
mkdir -p /bundle
systemctl enable bundle.automount

#======================================
# Activate kiwi service
#--------------------------------------
baseInsertService kiwi

#======================================
# lvmetad sucks for building lvm images
#--------------------------------------
systemctl disable lvm2-lvmetad
systemctl mask lvm2-lvmetad
systemctl disable lvm2-lvmetad.socket
systemctl mask lvm2-lvmetad.socket

#======================================
# Create systemd resolver link
#--------------------------------------
ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf
