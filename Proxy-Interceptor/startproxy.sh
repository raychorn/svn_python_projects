#!/bin/bash

proxy="proxy.py"

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

if [ -f "$proxy" ]; then 
	echo "$proxy exists."
else
	echo "$proxy does not exist so there is nothing to do."
	exit 1
fi

$python $proxy -l 127.0.0.1:9990 -r 127.0.0.1:9991 -d 1 -b 100

