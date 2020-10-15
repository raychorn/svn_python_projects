from vyperlogix.py2exe import setup
setup.do_setup(
    program_name='remove-oldest-files',
    company_name='VyperLogix Corp.',
    product_name='VyperLogix Remove Oldest Files',
    description='VyperLogix Remove Oldest Files',
    product_version='1.0.0.0',
    icon='VyperLogixCorp.ico',
    packages=[],
    packagedir={},
    datafiles=[],
    data_files=[],
    dist_dir='./dist/remove-oldest-files',
    compiled_excludes=['boto','requests','web','simplejson','json','wsgiref','paramiko','Crypto','M2Crypto']
)
