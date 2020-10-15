#!/usr/bin/env bash

echo "BEGIN: stop-WebServerProxy"

if [ -f /var/run/WebServerProxy.pid ]; then
	x=$(cat /var/run/WebServerProxy.pid)
	kill -9 $x
	rm -f /var/run/WebServerProxy.pid
else
	echo "Nothing to do !!!"
fi

echo "END! stop-WebServerProxy"



