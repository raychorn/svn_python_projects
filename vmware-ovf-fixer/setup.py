from vyperlogix.py2exe import setup
setup.do_setup(
    program_name='vmware_ovf_fixer',
    company_name='VyperLogix Corp.',
    product_name='VyperLogix VmWare OVF Fixer',
    description='VyperLogix VmWare OVF Fixer - corrects an OVF after export so it can be Deployed.',
    product_version='1.0.0.0',
    icon='VyperLogixCorp.ico',
    dist_dir='./dist',
    packages=[],
    packagedir={},
    datafiles=[ ('./docs', ['README.txt']) ],
    #data_files=[('Microsoft.VC90.CRT', '*.*')],
    compiled_excludes=['boto','requests','web','simplejson','json','wsgiref']
)
