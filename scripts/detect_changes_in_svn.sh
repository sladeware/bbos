#!/bin/bash
#
# Detect changes in the svn repository and kick off
# processing as required
#

cd /home/slade/bbos/src/bbos

TMP=/tmp/.bbos_head
BBOS_HEAD=$(svn log -r HEAD | awk '/^r[0-9]+/ {print $1}')

SUBJECT="New BBOS Revision"
TO_ADDR="slade@computer.org mail.d2rk@gmail.com"

if [ -e "$TMP" ];
then
    LAST_BBOS_HEAD=$(cat "$TMP")
    if [ "$BBOS_HEAD" != "$LAST_BBOS_HEAD" ];
    then
        echo "Emailing $TO_ADDR about $BBOS_HEAD"
	svn log -v -r HEAD | nail -s "$SUBJECT $BBOS_HEAD" "$TO_ADDR";
    fi;
fi;

echo "$BBOS_HEAD" > "$TMP"
