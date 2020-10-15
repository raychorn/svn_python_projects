from vyperlogix.py2exe import setup

__target__ = r'C:\@vm2\simple-message-bus'

minion = setup.CopyFilesToTarget(__target__,isZIP=True)

#callback=minion.callback,

setup.do_setup(
    program_name='simple-message-bus',
    company_name='VyperLogix Corp.',
    product_name='VyperLogix Simple Message Bus Demo',
    description='VyperLogix Simple Message Bus Demo',
    product_version='1.0.0.0',
    minion=minion,
    icon='VyperLogixCorp.ico',
    dist_dir='./dist',
    packages=[],
    extra_packages=['win32con', 'win32file'],
    extra_modules=[],
    packagedir={},
    datafiles=[ ('./docs', ['README.txt']), ('.', ['stop.cmd']), ('./bin', ['run1.cmd']), ('./bin', ['run2.cmd']) ],
    data_files=[('Microsoft.VC90.CRT', '*.*')],
    compiled_excludes=['boto','requests','web','wsgiref']
)
