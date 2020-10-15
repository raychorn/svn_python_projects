from vyperlogix.py2exe import setup

__target__ = r'C:\@vm1\windows-sample-service'

minion = setup.CopyFilesToTarget(__target__)

setup.do_setup(
    program_name='aservice',
    company_name='VyperLogix Corp.',
    product_name='VyperLogix Windows Sample Service',
    description='VyperLogix Windows Sample Service',
    product_version='1.0.0.0',
    icon='VyperLogixCorp.ico',
    service_module='aservice',
    cmdline_style=setup.CommandLineTypes.py2exe,
    datafiles=[ 
        ('.', ['install.cmd']), 
        ('.', ['remove.cmd']), 
        ('.', ['start.cmd']), 
        ('.', ['stop.cmd']), 
        ('.', ['restart.cmd']), 
        ('Microsoft.VC90.CRT', ['Microsoft.VC90.CRT.manifest']), 
        ('Microsoft.VC90.CRT', ['msvcm90.dll']), 
        ('Microsoft.VC90.CRT', ['msvcp90.dll']), 
        ('Microsoft.VC90.CRT', ['msvcr90.dll']), 
    ],
    initialize_datafiles=True,
    callback=minion.callback
)
