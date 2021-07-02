#!/bin/bash
test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile

#======================================
# Setup baseproduct link
#--------------------------------------
suseSetupProduct

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
suseInsertService kiwi

#======================================
# lvmetad sucks for building lvm images
#--------------------------------------
systemctl disable lvm2-lvmetad
systemctl mask lvm2-lvmetad
systemctl disable lvm2-lvmetad.socket
systemctl mask lvm2-lvmetad.socket
