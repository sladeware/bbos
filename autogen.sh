#!/bin/sh
#
# Copyright (c) 2012 Sladeware LLC
#

set -ex
autoreconf -v -f -i
rm -rf autom4te.cache
exit 0