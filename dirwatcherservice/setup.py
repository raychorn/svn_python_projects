from vyperlogix.py2exe import setup

from dirwatcherservice import __version__
setup.do_setup(
    program_name='dirwatcherservice',
    company_name='VyperLogix Corp.',
    product_name='VyperLogix Directory Watcher Service',
    description='VyperLogix Directory Watcher Service',
    product_version=__version__,
    icon='VyperLogixCorp.ico',
    dist_dir='./dist',
    packages=[],
    packagedir={},
    datafiles=[],
    data_files=[],
    compiled_excludes=[],
    dll_excludes=["MSVCR90.dll", "MSVCP90.dll", "msvcm90.dll"]
)
