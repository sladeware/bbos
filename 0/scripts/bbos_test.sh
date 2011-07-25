#!/bin/bash
#
# Run all the test required before commiting bbos
#
# Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
#

BBOS_ROOT=`dirname $0`/..
export PYTHONPATH=$BBOS_ROOT:$PYTHONPATH

PYCHECKER_ERROR_LIMIT=1000
PYCHECKER_FILTER=""

# Separator for separate things :)
seperator() {
    echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
}

# Output banner
seperator
echo "BBOS Test Runner!"
seperator

# You need to have pychecker installed to do a pycheck
CNT=1
which pychecker > /dev/null
if [ "$?" -eq "0" ]; then
    echo
    echo "[$CNT] PYCHECKER RESULTS. PLEASE REVIEW AND CLEANUP WARNINGS."
    seperator
    echo
    find $BBOS_ROOT -name \*.py | \
	xargs pychecker --no-argsused --limit=$PYCHECKER_ERROR_LIMIT 2> /dev/null
    echo
else
    echo "YOU MUST INSTALL PYCHECKER TO RUN THE PYCHECKER TEST"
fi
