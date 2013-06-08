# http://www.bionicbunny.org/
# Copyright (c) 2012-2013 Sladeware LLC
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
#
# Author: Oleksandr Sviridenko

import inspect
import os
from os.path import *
import types

from bb.utils import typecheck

# cache for by mkpath() -- in addition to cheapening redundant calls
_path_created = {}

def absjoin(*args):
  return abspath(join(*args))

def localpath(*args):
  caller_frame = inspect.getouterframes(inspect.currentframe(), 1)
  filename = inspect.getsourcefile(caller_frame[1][0])
  return join(dirname(filename), *args)

def remove_tree(directory, dry_run=False):
  """Recursively removes an entire directory tree.

  Any errors are ignored (apart from being reported to stdout if 'verbose'
  is true).
  """
  global _path_created

  def _build_tuple(path, cmdtuples):
    """Helper for remove_tree()."""
    for f in os.listdir(path):
      real_f = join(path,f)
      if isdir(real_f) and not islink(real_f):
        _build_tuple(real_f, cmdtuples)
      else:
        cmdtuples.append((os.remove, real_f))
    cmdtuples.append((os.rmdir, path))

  if dry_run:
    return
  cmdtuples = []
  _build_tuple(directory, cmdtuples)
  for cmd in cmdtuples:
    try:
      cmd[0](cmd[1])
      # remove dir from cache if it's already there
      abspath = abspath(cmd[1])
      if abspath in _path_created:
        del _path_created[abspath]
    except (IOError, OSError), exc:
      print exc, "error removing %s: " % directory

def touch(name, mode=0777, recursive=False):
  if typecheck.is_list(name):
    name = join(*name)
  if not typecheck.is_string(name):
    raise TypeError()
  if not typecheck.is_int(mode):
    raise TypeError()
  if not typecheck.is_bool(recursive):
    raise TypeError()
  if recursive:
    mkpath(dirname(name), mode=mode)
  open(name, "w").close()
  return name

def mkpath(name, mode=0777, verbose=0, dry_run=False):
  """Creates a file/directory and any missing ancestor directories. If the
  directory already exists (or if `name` is the empty string, which means the
  current directory, which of course exists), then do nothing. Raises
  :class:`OSError` if unable to create some directory along the way (eg. some
  sub-path exists, but is a file rather than a directory). If 'verbose' is true,
  print a one-line summary of each mkdir to stdout.

  :raises: OSError
  """
  global _path_created
  if not isinstance(name, types.StringTypes):
    raise TypeError("'name' must be a string (got %r)" % (name, ))
  # XXX: what's the better way to handle verbosity? print as we
  # create each directory in the path (the current behaviour), or
  # only announce the creation of the whole path? (quite easy to do
  # the latter since we're not using a recursive algorithm)
  name = normpath(name)
  created_dirs = []
  if isdir(name) or name == '':
    return created_dirs
  if _path_created.get(abspath(name)) \
        and exists(abspath(name)):
    return created_dirs
  (head, tail) = split(name)
  tails = [tail] # stack of lone dirs to create
  while head and tail and not isdir(head):
    (head, tail) = split(head)
    tails.insert(0, tail) # push next higher dir onto stack
  # now 'head' contains the deepest directory that already exists
  # (that is, the child of 'head' in 'name' is the highest directory
  # that does *not* exist)
  for d in tails:
    head = join(head, d)
    abs_head = abspath(head)
    if _path_created.get(abs_head) and exists(abs_head):
      continue
    if not dry_run:
      try:
        os.mkdir(head)
        created_dirs.append(head)
      except OSError, exc:
        raise OSError("could not create '%s': %s" % (head, exc[-1]))
    _path_created[abs_head] = 1
  return created_dirs
