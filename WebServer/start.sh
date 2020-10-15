#!/bin/bash

echo "BEGIN: start-WebServerProxy"

if [ -f /var/run/WebServerProxy.pid ]; then
	rm -f /var/run/WebServerProxy.pid
	echo "Nothing to do !!!"
else
	nohup /home/ubuntu/python/stackless/run2.sh > /home/ubuntu/python/stackless/nohup2.out 2>&1&
	sleep 5
	ps aux | grep WebServerProxy.py | grep -v grep | awk '{print $2}' | tail -n 1 > /var/run/WebServerProxy.pid
fi

echo "END! start-WebServerProxy"
