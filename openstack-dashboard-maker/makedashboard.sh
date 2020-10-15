#!/bin/bash

MAKE_DASHBOARD="make-dashboard.py"
DASHBOARD="/Volumes/Macintosh JetDrive HD/@Vyper Logix Corp/@Projects/openstack-projects/horizon/openstack_dashboard"

python=$(which python | awk '{print $1}' | tail -n 1)
if [ -f "$python" ]; then 

	ret=`$python -c 'import sys; print("%i" % (sys.hexversion>0x02070000 and sys.hexversion<0x03000000))'`
	if [ $ret -eq 0 ]; then
		echo "we require python version 2.7"
		exit 1
	else 
		echo "python version is acceptable."
	fi
	
else
    echo "Cannot find python. Aborting."
	exit 1
fi

if [ -f "$MAKE_DASHBOARD" ]; then 
	echo "$MAKE_DASHBOARD exists."
else
	echo "$MAKE_DASHBOARD does not exist so there is nothing to do."
	exit 1
fi

if [ -d "$DASHBOARD" ]; then 
	echo "$DASHBOARD exists."
else
	echo "$DASHBOARD does not exist so there is nothing to do."
	exit 1
fi

$python $MAKE_DASHBOARD -i "$DASHBOARD" -t -v

#-i "/Users/raychorn/Documents/@accenture (AT&T)/@git/dnsaas/openstack_dashboard" -t -v -n sample1
