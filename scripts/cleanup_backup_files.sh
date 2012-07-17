#!/bin/sh

echo "Recursively removing *~ files from"
pwd
find ./ -name '*~' -exec rm '{}' \; -print -or -name ".*~" -exec rm {} \; -print
