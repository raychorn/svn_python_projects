from vyperlogix.py2exe import setup

__target__ = r'C:\@vm1\dirwatcher'

minion = setup.CopyFilesToTarget(__target__)

from __version__ import __version__
setup.do_setup(
    program_name='dirwatcher',
    company_name='VyperLogix Corp.',
    product_name='VyperLogix Windows Directory Watcher',
    description='VyperLogix Windows Directory Watcher',
    product_version=__version__,
    icon='VyperLogixCorp.ico',
    callback=minion.callback,
    dist_dir='./dist',
    packages=[],
    packagedir={},
    datafiles=[],
    data_files=[],
    compiled_excludes=[],
    dll_excludes=["MSVCR90.dll", "MSVCP90.dll", "msvcm90.dll"]
)
