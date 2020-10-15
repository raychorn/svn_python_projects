#!/bin/bash

web1="webservice1.py"

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

if [ -f "$web1" ]; then 
	echo "$web1 exists."
else
	echo "$web1 does not exist so there is nothing to do."
	exit 1
fi

$python $web1 127.0.0.1:9991

