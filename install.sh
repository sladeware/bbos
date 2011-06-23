#!/bin/sh

ROOT=$(readlink -f $0)
ROOT_DIR=`dirname $ROOT`

rm /usr/bin/bb
ln -vs "$ROOT_DIR/tools/scripts/bbtouch.py" /usr/bin/bb

