#!/bin/bash
export PYTHONPATH=/usr/lib/python2.7/dist-packages

export PASSPHRASE=Peekab00
export AWS_ACCESS_KEY_ID=AKIAI52A6BTLWZHHDLCA
export AWS_SECRET_ACCESS_KEY=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

BUCKET=$1
FOLDER=$2
FILE=$3
 
f=$(which aws)
echo $f
pid=$(ps aux | grep $f | grep -v grep | awk '{print $2}' | tail -n 1)
echo ${pid}
if [ ${#pid} == "0" ]; then
	echo aws put __vyperlogix_svn_backups__/backups/$FILE $FOLDER/$BUCKET/$FILE
	aws put __vyperlogix_svn_backups__/backups/$FILE $FOLDER/$BUCKET/$FILE
else
	echo "Already running aws - Cannot run more than one instance at a time !!!"
fi

export PASSPHRASE=
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=