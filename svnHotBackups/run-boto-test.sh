#!/bin/bash

if [ -f /root/bin/PYTHONPATH ]; then
	. /root/bin/PYTHONPATH
fi

pid=$(ps aux | grep boto-test.py | grep -v grep | awk '{print $2}' | tail -n 1)

if [ ${#pid} == "0" ]; then
	/root/bin/python /root/svnHotBackups/boto-test.py 

else
	echo "Running boto-test.py - Cannot run more than one instance at a time !!!"
fi

