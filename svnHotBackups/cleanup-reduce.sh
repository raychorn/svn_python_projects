#!/bin/bash

if [ -f /root/bin/PYTHONPATH ]; then
	. /root/bin/PYTHONPATH
else
	echo "Cannot locate /root/bin/PYTHONPATH"
fi

DIRNAME=$1
REDUCE=$2
if [ -d $DIRNAME ]; then
	if [ ${#REDUCE} == "0" ]; then
		/root/bin/python /root/svnHotBackups/cleanup-backups.py --repo-path=$DIRNAME
	else
		/root/bin/python /root/svnHotBackups/cleanup-backups.py --repo-path=$DIRNAME --reduce
	fi
else
	echo "$(DIRNAME) does not exists"
	if [ ${#REDUCE} == "0" ]; then
		/root/bin/python /root/svnHotBackups/cleanup-backups.py
	else
		/root/bin/python /root/svnHotBackups/cleanup-backups.py --reduce
	fi
fi

