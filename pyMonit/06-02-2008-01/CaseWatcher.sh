#!/usr/bin/env bash
#
# if 'bash' gives us bash v1, try to relaunch script bash v2 by name
BASHVER=`echo $BASH_VERSION | cut -b 1 -`
if [ $BASHVER = "1" ]; then
    exec bash2 $0 $*
fi

PATH=/opt/ActivePython-2.5/bin:$PATH
export PATH

PYTHONPATH=${PATH}:/root/@utils/eggs/VyperLogixLib-1.0-py2.5.egg:/root/@utils/eggs/CaseWatcher_1_0.egg
export PYTHONPATH

cd /var/log/CaseWatcher/CaseWatcher
python /root/@utils/CaseWatcher/CaseWatcherList2.pyc --verbose --smtpserver=tide2.magma-da.com:8025 --cwd=/var/log/CaseWatcher/CaseWatcher --logging=logging.WARNING --console_logging=logging.INFO --username=molten_admin@magma-da.com --password=u2cansleeprWI2X9JakDlxjcuAofhggFbaf
