#!/bin/bash
#
# Run all the test required before commiting bbos builder code
#
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

BBOS_ROOT=`dirname $0`/..
export PYTHONPATH=$BBOS_ROOT:$PYTHONPATH

DEMO=$BBOS_ROOT/demos/hello_world/demo
DEMO_COG=$BBOS_ROOT/demos/hello_world/demo_cog
BBOS_H=$BBOS_ROOT/demos/hello_world/bbos.h

BBOS_H_MD5SUM="dcf6a9ec5db9c6fe57f8c50590d90e3f"

PYCHECKER_ERROR_LIMIT=1000
PYCHECKER_FILTER="bbos/security/crypto/asn1.py"

seperator() {
    echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
}

# Output banner
seperator
echo "BBOS Test Runner!"
seperator

# Run the bbos builder library regressions
CNT=1
which python > /dev/null
if [ "$?" -eq "0" ]; then
    echo
    echo "[$CNT] REGRESSION TEST RESULTS. PLEASE FIX FAILURES."
    seperator
    echo
    python $BBOS_ROOT/bbos/builder/regression.py
    echo
else
    echo "YOU MUST INSTALL PYTHON TO RUN PYTHON PREGRESSION TESTS"
fi
seperator

# Build hello world (we know python is installed)
CNT=2
echo
echo "[$CNT] GENERATING AND BUILDING HELLO WORLD. PLEASE FIX FAILURES"
seperator
echo
date
echo
python $BBOS_ROOT/scripts/bbos_builder.py -a $BBOS_ROOT/demos/hello_world/bbos.py 2> /dev/null
echo
seperator

# List the results so we know it worked
CNT=3
echo
echo "[$CNT] LISTING THE RESULTS SO YOU KNOW THE BBOS BUILDER WORKED"
seperator
echo
ls -l $BBOS_H
ls -l $DEMO
ls -l $DEMO_COG
rm $DEMO_COG
echo
seperator

# Show the hello world header file
CNT=4
echo
echo "[$CNT] CHECKING MD5SUM OF THE BBOS HEADER THAT WAS GENERATED"
seperator
echo
which md5sum > /dev/null
if [ "$?" -eq "0" ]; then
    M=`md5sum $BBOS_H`
    MD5SUM=${M% *}
    if [ $BBOS_H_MD5SUM = $MD5SUM ]; then
	echo "MD5SUM CHECK OK"
    else
	echo "WARNING!!! MD5SUM MISMATCH"
    fi
else
    echo "YOU MUST INSTALL MD5SUM TO SEE MD5 MATCH RESULTS. CATTING BBOS.H INSTEAD."
    cat $BBOS_H
fi
rm $BBOS_H
echo
seperator

# Run hello world
CNT=5
echo
echo "[$CNT] RUNNING HELLO WORLD. PLEASE FIX FAILURES."
seperator
echo
chmod +x $DEMO
$DEMO | head -n 6&
sleep 1
kill %1
rm $DEMO
echo
seperator

# You need to have pychecker installed to do a pycheck
CNT=6
which pychecker > /dev/null
if [ "$?" -eq "0" ]; then
    echo
    echo "[$CNT] PYCHECKER RESULTS. PLEASE REVIEW AND CLEANUP WARNINGS."
    seperator
    echo
    find $BBOS_ROOT -name \*.py | \
	xargs pychecker --limit=$PYCHECKER_ERROR_LIMIT 2> /dev/null | \
	grep -v $PYCHECKER_FILTER
    echo
else
    echo "YOU MUST INSTALL PYCHECKER TO RUN THE PYCHECKER TEST"
fi
seperator
