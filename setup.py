#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup
from setuptools.command import sdist as setuptools_sdist

from distutils.command import build as distutils_build
from distutils.command import install as distutils_install
from distutils.command import clean as distutils_clean

import distutils
import subprocess
import os
import sys
import platform

from kiwi_boxed_plugin.version import __version__

python_version = platform.python_version().split('.')[0]

# sys.base_prefix points to the installation prefix set during python
# compilation and sys.prefix points to the same path unless we are inside
# a venv, in which case points to the $VIRTUAL_ENV value.
is_venv = sys.base_prefix != sys.prefix if sys.version_info >= (3, 3) else False


class install(distutils_install.install):
    """
    Custom install command
    Host requirements: make
    """
    distutils_install.install.user_options += [
        ('single-version-externally-managed', None,
         "used by system package builders to create 'flat' eggs")
    ]

    sub_commands = [
        ('install_lib', lambda self:True),
        ('install_headers', lambda self:False),
        ('install_scripts', lambda self:True),
        ('install_data', lambda self:False),
        ('install_egg_info', lambda self:True),
    ]

    def initialize_options(self):
        """
        Set default values for options
        Each user option must be listed here with their default value.
        """
        distutils_install.install.initialize_options(self)
        self.single_version_externally_managed = None

    def run(self):
        """
        Run first the related plugin installation tasks and after
        that the usual Python installation
        """
        command = ['make']
        if self.root:
            command.append('buildroot={0}/'.format(self.root))
        elif is_venv:
            command.append('buildroot={0}/'.format(sys.prefix))
        command.append('python_version={0}'.format(python_version))
        command.append('install')
        self.announce(
            'Running make install target: {0}'.format(command),
            level=distutils.log.INFO
        )
        self.announce(
            subprocess.check_output(command).decode(),
            level=distutils.log.INFO
        )
        # standard installation
        distutils_install.install.run(self)


config = {
    'name': 'kiwi_boxed_plugin',
    'description': 'KIWI - Boxed Build Plugin',
    'author': 'Marcus Schaefer',
    'url': 'https://github.com/OSInside/kiwi-boxed-plugin',
    'download_url':
        'https://download.opensuse.org/repositories/'
        'Virtualization:/Appliances:/Builder',
    'author_email': 'ms@suse.com',
    'version': __version__,
    'license' : 'GPLv3+',
    'install_requires': [
        'docopt',
        'kiwi',
        'requests',
        'PyYAML',
        'cerberus'
    ],
    'packages': ['kiwi_boxed_plugin'],
    'cmdclass': {
        'install': install
    },
    'entry_points': {
        'kiwi.tasks': [
            'system_boxbuild=kiwi_boxed_plugin.tasks.system_boxbuild'
        ]
    },
    'include_package_data': True,
    'zip_safe': False,
    'classifiers': [
       # classifier: http://pypi.python.org/pypi?%3Aaction=list_classifiers
       'Development Status :: 5 - Production/Stable',
       'Intended Audience :: Developers',
       'License :: OSI Approved :: '
       'GNU General Public License v3 or later (GPLv3+)',
       'Operating System :: POSIX :: Linux',
       'Programming Language :: Python :: 3.6',
       'Programming Language :: Python :: 3.7',
       'Topic :: System :: Operating System',
    ]
}

setup(**config)
