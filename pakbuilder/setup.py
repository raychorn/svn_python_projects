from vyperlogix.py2exe import setup

__target__ = r'C:\@vm1\pakbuilder'

minion = setup.CopyFilesToTarget(__target__)

from pakbuilder import __version__
setup.do_setup(
    program_name='pakbuilder',
    company_name='VyperLogix Corp.',
    product_name='VyperLogix VCOPS PAK Builder',
    description='VCOPS PAK Builder for Windows is protected by (c). Copyright 2014, Vyper Logix Corp., See the LICENSE file for Licensing Details.',
    product_version=__version__,
    icon='VyperLogixCorp.ico',
    callback=minion.callback,
    collector=setup.VyperLogixLibraryDocsZipsCollector,
    dist_dir='./dist',
    packages=['paramiko'],
    packagedir={ 'Crypto':'C:/Python27/Lib/site-packages/Crypto',
                 'paramiko':'C:/Python27/Lib/site-packages/paramiko-1.10.1-py2.7.egg/paramiko'
                 },
    datafiles=[ ('.', ['buildpakfile.cmd']), ('.', ['remotedebugger.cmd']) ],
    data_files=[],
    compiled_excludes=['boto','requests','web','simplejson','json','wsgiref']
)
