#!/usr/bin/env bash
#
# if 'bash' gives us bash v1, try to relaunch script bash v2 by name
BASHVER=`echo $BASH_VERSION | cut -b 1 -`
if [ $BASHVER = "1" ]; then
    exec bash2 $0 $*
fi

PATH=/opt/ActivePython-2.5/bin:$PATH
export PATH

PYTHONPATH=${PATH}:/home/zope/molten-svn/MoltenWatcher/eggs/VyperLogixLib-1.0-py2.5.egg:/home/zope/molten-svn/MoltenWatcher/eggs/VyperLogixMagmaLib-1.0-py2.5.egg:/home/zope/molten-svn/MoltenWatcher/eggs/VyperLogixPyaxLib-1.0-py2.5.egg:/home/zope/molten-svn/MoltenWatcher/eggs/SQLAlchemy-0.5.2-py2.5.egg:/home/zope/molten-svn/MoltenWatcher/eggs/psyco-1.6-py2.5-linux-i686.egg:/home/zope/molten-svn/MoltenWatcher/eggs/paramiko-1.7.4-py2.5.egg

export PYTHONPATH

cd /home/zope/molten-svn/MoltenWatcher 
python /home/zope/molten-svn/MoltenWatcher/fetch_data_from_server.pyc --no-test --verbose --no-help --server=admin@64.106.247.200:22
