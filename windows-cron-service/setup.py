from vyperlogix.py2exe import setup

__target__ = r'C:\@vm1\windows-cron-service'

minion = setup.CopyFilesToTarget(__target__)

setup.do_setup(
    program_name='cronservice',
    company_name='VyperLogix Corp.',
    product_name='VyperLogix Windows Cron Service',
    description='VyperLogix Windows Cron Service',
    product_version='1.0.0.0',
    icon='VyperLogixCorp.ico',
    service_module='cronservice',
    cmdline_style=setup.CommandLineTypes.custom,
    cmdline_extra='--json "./service_config.json"',
    packages=['paramiko','OpenSSL'],
    packagedir={ 'Crypto':'C:/Python27/Lib/site-packages/Crypto',
                 'OpenSSL':'C:/Python27/Lib/site-packages/OpenSSL',
                 'paramiko':'C:/Python27/Lib/site-packages/paramiko-1.10.1-py2.7.egg/paramiko'
                 },
    datafiles=[ 
        ('.', ['install.cmd']), 
        ('.', ['remove.cmd']), 
        ('.', ['start.cmd']), 
        ('.', ['stop.cmd']), 
        ('.', ['restart.cmd']), 
        ('.', ['favicon.ico']), 
        ('.', ['crossdomain.xml']), 
        ('.', ['service_config.json']), 
        ('.', ['server.crt']), 
        ('.', ['server.key.insecure']), 
        ('Microsoft.VC90.CRT', ['Microsoft.VC90.CRT.manifest']), 
        ('Microsoft.VC90.CRT', ['msvcm90.dll']), 
        ('Microsoft.VC90.CRT', ['msvcp90.dll']), 
        ('Microsoft.VC90.CRT', ['msvcr90.dll']), 
    ],
    initialize_datafiles=True,
    callback=minion.callback
)
