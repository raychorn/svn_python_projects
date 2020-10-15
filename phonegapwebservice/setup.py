import os
from vyperlogix.py2exe import setup

__target__ = r'C:\@vm1\phonegapwebservice'

minion = setup.CopyFilesToTarget(__target__)

setup.do_setup(
    program_name='phonegapwebservice',
    company_name='VyperLogix Corp.',
    product_name='VyperLogix PhoneGap Web Service',
    description='VyperLogix PhoneGap Web Service',
    product_version='1.0.0.0',
    icon='VyperLogixCorp.ico',
    callback=minion.callback,
    packages=['paramiko','OpenSSL'],
    packagedir={ 'Crypto':'C:/Python27/Lib/site-packages/Crypto',
                 'OpenSSL':'C:/Python27/Lib/site-packages/OpenSSL',
                 'paramiko':'C:/Python27/Lib/site-packages/paramiko-1.10.1-py2.7.egg/paramiko'
                 },
    datafiles=[ 
        ('.', ['server.crt']), 
        ('.', ['server.key.insecure']), 
    ],
)
