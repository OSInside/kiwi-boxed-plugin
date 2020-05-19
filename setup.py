#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup

from kiwi_boxed_plugin.version import __version__


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
