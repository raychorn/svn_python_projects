from vyperlogix.py2exe import setup

__target__ = r'C:\@vm2\proxy'

minion = setup.CopyFilesToTarget(__target__,isZIP=True)

setup.do_setup(
    program_name='proxy',
    company_name='VyperLogix Corp.',
    product_name='VyperLogix Reverse Proxy',
    description='VyperLogix Reverse Proxy',
    product_version='1.0.0.0',
    minion=minion,
    icon='VyperLogixCorp.ico',
    dist_dir='./dist',
    packages=[],
    extra_packages=[],
    extra_modules=[],
    packagedir={},
    datafiles=[ ('./docs', ['README.txt']) ],
    data_files=[('Microsoft.VC90.CRT', '*.*')],
    compiled_excludes=['boto','requests','web','wsgiref']
)
