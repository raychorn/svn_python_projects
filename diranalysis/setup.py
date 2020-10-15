from vyperlogix.py2exe import setup
setup.do_setup(
    program_name='delete-folder',
    company_name='VyperLogix Corp.',
    product_name='VyperLogix Delete Folder',
    description='VyperLogix Delete Folder',
    product_version='1.0.0.0',
    icon='VyperLogixCorp.ico',
    dist_dir='./dist',
    packages=['paramiko'],
    packagedir={ 'Crypto':'C:/Python27/Lib/site-packages/Crypto',
                 'paramiko':'C:/Python27/Lib/site-packages/paramiko-1.10.1-py2.7.egg/paramiko'
                 },
    #datafiles=[ ('./docs', ['README.txt']) ],
    #data_files=[('Microsoft.VC90.CRT', '*.*')],
    compiled_excludes=['boto','requests','web','simplejson','json','wsgiref']
)
