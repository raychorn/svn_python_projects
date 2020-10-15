longdesc = '''
This is the standard VyperLogix.Com Pyax Distro.
See also: http://www.pypi.info
CREATIVE COMMONS PUBLIC LICENSE (http://creativecommons.org/licenses/by-nc/3.0/) Restricted to non-commercial educational use only.
'''

import ez_setup
ez_setup.use_setuptools()

import os, sys
try:
    from setuptools import setup
    kw = {
    }
    
except ImportError:
    from distutils.core import setup
    kw = {}
    
from setuptools import find_packages
_packages = [p for p in find_packages()]
setup(
    name = "VyperLogixPyaxLib",
    version = "1.0",
    packages = _packages,
    description = "VyperLogix.Com Standard Pyax Distro",
    author = "VyperLogix.Com",
    author_email = "support@vyperlogix.com",
    url = "http://VyperLogix.Com",
    download_url = 'http://www.pypi.info',
    license = 'CREATIVE COMMONS PUBLIC LICENSE (http://creativecommons.org/licenses/by-nc/3.0/) Restricted to non-commercial educational use only.',
    platforms = 'Posix; Windows',
    classifiers = [ 'Development Status :: 5 - Production/Stable',
                    'Intended Audience :: Developers',
                    'License :: OSI Approved :: GPL (Restricted to Non-Commercial Educational Use Only).',
                    'Operating System :: OS Independent',
                    'Topic :: Internet' ],
    long_description = longdesc,
    **kw
)

