#!/bin/sh

SCRIPT=$(readlink -f $0)
SCRIPTS_DIR=`dirname $SCRIPT`

ln -vs "$SCRIPTS_DIR/bb.py" /usr/bin/bb

