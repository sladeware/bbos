#!/bin/bash
#
# Run all the test required before commiting bbos builder code
#
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

BBOS_ROOT=`dirname $0`/..
export PYTHONPATH=$BBOS_ROOT:$PYTHONPATH

DEMO=$BBOS_ROOT/demos/hello_world/demo
BBOS_H=$BBOS_ROOT/demos/hello_world/bbos.h

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
ls -l $BBOS_H
ls -l $DEMO
echo
seperator

# Show the hello world header file
CNT=4
echo
echo "[$CNT] SHOWING YOU THE BBOS HEADER THAT WAS GENERATED IN CASE YOU THINK IT IS WRONG"
seperator
cat $BBOS_H
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
$DEMO | head &
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
    find $BBOS_ROOT -name \*.py | xargs pychecker 2> /dev/null
    echo
else
    echo "YOU MUST INSTALL PYCHECKER TO RUN THE PYCHECKER TEST"
fi
seperator
