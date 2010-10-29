#!/bin/bash
#
# Detect changes in the svn repository and kick off
# processing as required
#

# The BBOS root directory
BBOS_ROOT="/home/slade/bbos/src/bbos"

# The temp directory
TMP=/tmp/.bbos_head

# The lock file we are using to enforce that only one instance runs
LOCK_FILE=/tmp/.bbos_lock

# Get the date for the timestamp in the lock file
LOCK_DATE=$(date)

# New BBOS revision Email subject
SUBJECT="New BBOS Revision"

# The email addresses of developers we send email to
TO_ADDR="slade@computer.org mail.d2rk@gmail.com"

# The temp file we use for our email
TMP_OUTPUT=/tmp/.detect_changes_in_svn_tmp

# This is processing done when the SVN repo is updated
conditional_processing() {
    # Email the update info to developers
    echo "Emailing $TO_ADDR about $BBOS_HEAD"
    svn log -v -r HEAD > $TMP_OUTPUT
    scripts/run_tests.sh >> $TMP_OUTPUT
    cat $TMP_OUTPUT | nail -s "$SUBJECT $BBOS_HEAD" "$TO_ADDR"
    rm $TMP_OUTPUT
}

# Call this when exiting to clear the lock file
bbos_exit() {
    # Remove the lock file
    LOCK_FILE_DATE=$(cat "$LOCK_FILE")
    if [ "$LOCK_FILE_DATE" == "$LOCK_DATE" ];
    then
	rm $LOCK_FILE
    fi

    exit
}

# Exit if we are already running
if [ -e "$LOCK_FILE" ];
then
    echo "Lock file exists. Exiting."
    bbos_exit
fi

# Create the lock file
echo "$LOCK_DATE" > "$LOCK_FILE"

# Go into the BBOS SVN root directory
cd $BBOS_ROOT

# Use svn log to determine the current head revision number
BBOS_HEAD=$(svn log -r HEAD | awk '/^r[0-9]+/ {print $1}')
if [ "$BBOS_HEAD" == "" ];
then
    echo "Problem with SVN access ($BBOS_HEAD). Exiting."
    bbos_exit
fi

# Detect update to SVN repository
if [ -e "$TMP" ];
then
    LAST_BBOS_HEAD=$(cat "$TMP")
    # If the repository has been updated then ...
    if [ "$BBOS_HEAD" != "$LAST_BBOS_HEAD" ];
    then
        # Do processing conditional on SVN repo update
	conditional_processing
    fi
fi

# Update the file storing the latest repository head
echo "$BBOS_HEAD" > "$TMP"

bbos_exit