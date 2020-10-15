from vyperlogix.py2exe import setup
setup.do_setup(
    program_name='gps-fences',
    company_name='VyperLogix Corp. for Zubie',
    product_name='VyperLogix GPS Fences',
    description='VyperLogix GPS Fences',
    product_version='1.0.0.0',
    icon='VyperLogixCorp.ico',
    dist_dir='./dist',
    packages=['geopy','json'],
    packagedir={
        'geopy':'C:\\Python27\\Lib\\site-packages\\geopy-0.97-py2.7.egg',
        'json':'C:\\Python27\\lib\\json'
    },
    datafiles=[ ('./docs', ['README.txt']) ],
    data_files=[('Microsoft.VC90.CRT', '*.*')],
    compiled_excludes=['boto','requests','web','simplejson','wsgiref']
)
