#!/bin/bash

./data.sh | ./py_send_nsca -H 127.0.0.1 -c /etc/nagios/send_nsca.cfg -p 5667 -v