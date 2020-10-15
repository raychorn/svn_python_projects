from vyperlogix.py2exe import setup

__target__ = r'C:\@vm1\yalidator'

minion = setup.CopyFilesToTarget(__target__)

from yalidator import __version__
setup.do_setup(
    program_name='yalidator',
    company_name='VyperLogix',
    product_name='VyperLogix YAML Validator Utility',
    description='Yalidator for Windows is protected by (c). Copyright 2014, VyperLogix., See the LICENSE file for Licensing Details.',
    product_version=__version__,
    icon='VyperLogixCorp.ico',
    callback=minion.callback,
    collector=setup.VyperLogixLibraryDocsZipsCollector,
    dist_dir='./dist',
    packages=[],
    packagedir={},
    datafiles=[ ('.', ['run.cmd']) ],
    data_files=[],
    compiled_excludes=[]
)
