#!/bin/bash
#
# Run all the test required before commiting bbos builder code
#
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

seperator() {
    echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
}

# Output banner
clear
seperator
echo "BBOS Test Runner!"
seperator

# You need to have pychecker installed to do a pycheck
which pychecker > /dev/null
if [ "$?" -eq "0" ]; then
    echo
    echo "PYCHECKER RESULTS. PLEASE REVIEW AND CLEANUP WARNINGS."
    seperator
    echo
    find ../bbos -name \*.py | xargs pychecker 2> /dev/null
    echo
else
    echo "YOU MUST INSTALL PYCHECKER TO RUN THE PYCHECKER TEST"
fi

# Run the bbos builder library regressions
which python > /dev/null
if [ "$?" -eq "0" ]; then
    echo
    echo "REGRESSION TEST RESULTS. PLEASE FIX FAILURES."
    seperator
    echo
    python ../bbos/builder/regression.py
    echo
else
    echo "YOU MUST INSTALL PYTHON TO RUN PYTHON PREGRESSION TESTS"
fi
seperator