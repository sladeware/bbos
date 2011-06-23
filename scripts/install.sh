#!/bin/sh

SCRIPT=$(readlink -f $0)
SCRIPTS_DIR=`dirname $SCRIPT`

ln -vs "$SCRIPTS_DIR/bionicbunny.py" /usr/bin/bb

