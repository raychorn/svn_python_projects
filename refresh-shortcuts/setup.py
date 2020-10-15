from vyperlogix.py2exe import setup

__target__ = r'C:\@vm2\refresh-shortcuts'

minion = setup.CopyFilesToTarget(__target__,isZIP=True)

setup.do_setup(
    program_name='refresh-shortcuts',
    company_name='VyperLogix Corp.',
    product_name='VyperLogix Refresh Shortcuts',
    description='VyperLogix Refresh Shortcuts',
    product_version='1.0.0.0',
    callback=minion.callback,
    icon='VyperLogixCorp.ico',
    dist_dir='./dist',
    packages=[],
    extra_packages=['win32com'],
    extra_modules=["win32com.shell","win32com.mapi"],
    packagedir={},
    datafiles=[ ('./docs', ['README.txt']), ('.', ['export-json.cmd']) ],
    data_files=[('Microsoft.VC90.CRT', '*.*')],
    compiled_excludes=['boto','requests','web','wsgiref']
)
