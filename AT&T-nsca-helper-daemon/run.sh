#!/bin/bash

if [ -f /root/bin/PYTHONPATH ]; then
	. /root/bin/PYTHONPATH
fi

python ./nsca-helper-daemon.py 0.0.0.0:15667


