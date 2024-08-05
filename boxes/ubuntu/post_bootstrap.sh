#!/bin/bash

set -ex

# Intermediate C locale setup
export LANG=C.UTF-8
export LANGUAGE=

# Intermediate Noninteractive debconf
echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Download packages for which we need the script code
apt-get -q -c /kiwi_apt.conf -y --no-install-recommends install \
    "-oDebug::pkgDPkgPm=1" "-oDPkg::Pre-Install-Pkgs::=cat >/tmp/postpacks" \
base-passwd

# Run package scripts for core OS packages which provides
# mandatory setup code in their pre/post scripts
export DPKG_ROOT=/
while read -r package;do
    pushd "$(dirname "${package}")" || exit 1
    if [ "$(basename "${package}")" = "base-passwd.deb" ];then
        # Required to create passwd, groups, the root user...
        dpkg -e "${package}"
        test -e DEBIAN/preinst && bash DEBIAN/preinst install
        test -e DEBIAN/postinst && bash DEBIAN/postinst
        rm -rf DEBIAN
    fi
    popd || exit 1
done < /tmp/postpacks
rm -f /tmp/postpacks
