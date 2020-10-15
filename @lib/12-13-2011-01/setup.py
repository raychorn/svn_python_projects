longdesc = '''
This is the standard VyperLogix.Com Python Library Distro.
See also: http://www.pypi.info
CREATIVE COMMONS PUBLIC LICENSE (http://creativecommons.org/licenses/by-nc/3.0/) Restricted to non-commercial educational use only.
'''

# To-Do: Compile All files, if required, prior to building the egg.

import ez_setup
ez_setup.use_setuptools()

import os, sys
try:
    from setuptools import setup
    kw = {
    }
# 'install_requires': 'paramiko >= 1.7',
# 'install_requires': 'pycrypto >= 1.9',
    
except ImportError:
    from distutils.core import setup
    kw = {}
    
from setuptools import find_packages
#_root = 'Z:\\python projects\\@lib'
#_root_name = _root.split(os.sep)
#_packages = [os.sep.join([_root,p]) for p in find_packages(_root)]
#_x = [os.sep.join(_root_name[0:-1]),_root_name[-1]]
#_packages.append(os.sep.join(_x))
_packages = [p for p in find_packages()]
setup(
    name = "VyperLogixLib",
    version = "1.0",
    packages = _packages,
    description = "VyperLogix.Com Standard Python Library Distro",
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

