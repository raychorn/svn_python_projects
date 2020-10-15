#!/bin/bash
export PYTHONPATH=/usr/lib/python2.7/dist-packages

export PASSPHRASE=Peekab00
export AWS_ACCESS_KEY_ID=AKIAI52A6BTLWZHHDLCA
export AWS_SECRET_ACCESS_KEY=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

BUCKET=$2
NAME=$1
if [ ${#NAME} == "0" ]; then
	echo aws ls __vyperlogix_svn_backups__/backups
	aws ls __vyperlogix_svn_backups__/backups
else
	p=$(aws ls __vyperlogix_svn_backups__/$BUCKET | grep $NAME)
	echo $p
fi

export PASSPHRASE=
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=