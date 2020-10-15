#!/usr/bin/env bash
# Runs on river.magma-da.com
# if 'bash' gives us bash v1, try to relaunch script bash v2 by name
BASHVER=`echo $BASH_VERSION | cut -b 1 -`
if [ $BASHVER = "1" ]; then
    exec bash2 $0 $*
fi

PATH=/home/sfscript/@misc/python25/bin:$PATH
export PATH

PYTHONPATH=${PATH}:/home/sfscript/src/sfapi2/sflib:/home/sfscript/@misc/script_deployments/eggs/VyperLogixLib-1.0-py2.5.egg
export PYTHONPATH

python pyMonit.pyo --port=8080 --logging=logging.WARNING --retention=1000
