#! /usr/bin/env python

"""Installation script for pyax.
Run it with
 './setup.py install', or
 './setup.py --help' for more options
"""

import os
import sys

import pyax

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
##
# META INFORMATION FOR SETUP

META_INFO = {'name':         'pyax',
             'version':      pyax.__version__,
             'author':       'Kevin Shuk, Canonical Ltd',
             'author_email': 'surf@canonical.com',
             'url':          'http://www.launchpad.net/pyax',
             'description':  'Salesforce API library for Python',
             'license':      'GNU GPL v2',
            }

PKG_DATA = {'packages':    ['pyax', 
                            'pyax.collections',
                            'pyax.datatype',
                            'pyax.sobject']
}

ARGS = {}

ARGS.update(META_INFO)
ARGS.update(PKG_DATA)

setup(**ARGS)