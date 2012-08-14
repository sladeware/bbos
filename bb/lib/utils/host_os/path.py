#!/usr/bin/env python
#
# Copyright (c) 2012 Sladeware LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import types

import bb

# cache for by mkpath() -- in addition to cheapening redundant calls
_path_created = {}

def mkpath(name, mode=0777, verbose=0, dry_run=0):
    """Create a directory and any missing ancestor directories. If the directory
    already exists (or if `name` is the empty string, which means the current
    directory, which of course exists), then do nothing. Raise :class:`OSError`
    if unable to create some directory along the way (eg. some sub-path exists,
    but is a file rather than a directory). If 'verbose' is true, print a
    one-line summary of each mkdir to stdout. Return the list of directories
    actually created.
    """
    global _path_created

    # Detect a common bug -- name is None
    if not isinstance(name, types.StringTypes):
        raise types.TypeError("mkpath: 'name' must be a string (got %r)" \
                                  % (name, ))

    # XXX: what's the better way to handle verbosity? print as we
    # create each directory in the path (the current behaviour), or
    # only announce the creation of the whole path? (quite easy to do
    # the latter since we're not using a recursive algorithm)

    name = bb.host_os.path.normpath(name)
    created_dirs = []
    if bb.host_os.path.isdir(name) or name == '':
        return created_dirs
    if _path_created.get(bb.host_os.path.abspath(name)) \
            and bb.host_os.path.exists(bb.host_os.path.abspath(name)):
        return created_dirs

    (head, tail) = bb.host_os.path.split(name)
    tails = [tail] # stack of lone dirs to create

    while head and tail and not bb.host_os.path.isdir(head):
        #print "splitting '%s': " % head,
        (head, tail) = bb.host_os.path.split(head)
        #print "to ('%s','%s')" % (head, tail)
        tails.insert(0, tail) # push next higher dir onto stack

    #print "stack of tails:", tails

    # now 'head' contains the deepest directory that already exists
    # (that is, the child of 'head' in 'name' is the highest directory
    # that does *not* exist)
    for d in tails:
        #print "head = %s, d = %s: " % (head, d),
        head = bb.host_os.path.join(head, d)
        abs_head = bb.host_os.path.abspath(head)

        if _path_created.get(abs_head) and bb.host_os.path.exists(abs_head):
            continue

        if not dry_run:
            try:
                bb.host_os.mkdir(head)
                created_dirs.append(head)
            except OSError, exc:
                raise OSError("could not create '%s': %s" % (head, exc[-1]))

        _path_created[abs_head] = 1
    return created_dirs
