schema = {
    'box': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'name': {
                    'type': 'string',
                    'required': True,
                    'empty': False
                },
                'mem_mb': {
                    'type': 'number',
                    'required': True,
                    'empty': False
                },
                'processors': {
                    'type': 'number',
                    'required': False,
                    'empty': False
                },
                'console': {
                    'type': 'string',
                    'required': True,
                    'empty': False
                },
                'arch': {
                    'required': True,
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'name': {
                                'type': 'string',
                                'allowed':
                                    ['x86_64', 's390x', 'aarch64', 'ppc64'],
                                'required': True,
                                'empty': False
                            },
                            'cmdline': {
                                'type': 'list',
                                'required': True,
                                'nullable': False
                            },
                            'source': {
                                'type': 'string',
                                'required': True,
                                'empty': False
                            },
                            'packages_file': {
                                'type': 'string',
                                'required': True,
                                'empty': False
                            },
                            'boxfiles': {
                                'type': 'list',
                                'required': True,
                                'nullable': False
                            },
                            'use_initrd': {
                                'type': 'boolean',
                                'required': True
                            }
                        }
                    }
                }
            }
        }
    }
}
