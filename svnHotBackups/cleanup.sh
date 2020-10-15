#!/bin/bash

if [ -f /root/bin/PYTHONPATH ]; then
	. /root/bin/PYTHONPATH
else
	echo "Cannot locate /root/bin/PYTHONPATH"
fi

DIRNAME=$1
if [ -d $DIRNAME ]; then
	/root/bin/python /root/svnHotBackups/cleanup-backups.py --repo-path=$DIRNAME
else
	echo "$(DIRNAME) does not exists"
	/root/bin/python /root/svnHotBackups/cleanup-backups.py
fi

