#!/bin/sh
#
# Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
#

ROOT=$(readlink -f $0)
ROOT_DIR=`dirname $ROOT`

# XXX: The BB package will not be installed to the python's search
# path by using setup.py script. Only a single link to the package
# will be created.

BB_PACKAGE_NAME=bb
BB_PACKAGE_DIR=$ROOT_DIR/$BB_PACKAGE_NAME
PYTHON_SEARCH_PATH=/usr/local/lib/python2.6/dist-packages

if [ -d $PYTHON_SEARCH_PATH/$BB_PACKAGE_NAME ]; then
	rm -df $PYTHON_SEARCH_PATH/$BB_PACKAGE_NAME
fi

ln -vs "$BB_PACKAGE_DIR" $PYTHON_SEARCH_PATH/$BB_PACKAGE_NAME
