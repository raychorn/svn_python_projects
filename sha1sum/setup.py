from vyperlogix.py2exe import setup
setup.do_setup(
    program_name='sha1sum',
    company_name='VyperLogix Corp.',
    product_name='VyperLogix sha1sum',
    description='VyperLogix sha1sum',
    product_version='1.0.0.0',
    icon='VyperLogixCorp.ico',
    dist_dir='./dist',
    packages=[],
    packagedir={ 'Crypto':'C:/Python27/Lib/site-packages/Crypto'
                 },
    datafiles=[ ('./docs', ['README.txt']) ],
    #data_files=[('Microsoft.VC90.CRT', '*.*')],
    compiled_excludes=['boto','requests','web','simplejson','json','wsgiref']
)
