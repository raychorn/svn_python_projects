#!/bin/bash

if [ -f /root/bin/PYTHONPATH ]; then
	. /root/bin/PYTHONPATH
fi

python ./root-daemon-att.py 0.0.0.0:1234


