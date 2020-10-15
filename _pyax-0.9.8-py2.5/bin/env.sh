#####
# Sets up additional environment for export script(s)
# intended to be sourced by the various launcher scripts
#
# Author:    Kevin Shuk
# Date:      2005-09-16
# Copyright: (c) 2005 Kevin Shuk, All Rights Reserved
#####
BASEDIR=${SCRIPTDIR}/..

SRCDIR=${BASEDIR}/pyax
BINDIR=${BASEDIR}/bin
CONFIGDIR=${BASEDIR}/config
TESTDIR=${BASEDIR}/tests
DOCDIR=${BASEDIR}/doc
export LIBDIR CONFIGDIR DOCDIR BINDIR TESTDIR

if [ -n $PYTHONPATH ]; then
    PYTHONPATH=$PYTHONPATH:$BASEDIR
else
    PYTHONPATH=$BASEDIR
fi

if [ -n $PYTHON ]; then
	PYTHON=`which python`
fi

export PYTHON PYTHONPATH
