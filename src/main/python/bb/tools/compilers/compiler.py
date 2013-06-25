# http://www.bionicbunny.org/
# Copyright (c) 2012-2013 Sladeware LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Oleksandr Sviridenko

import inspect

from bb.utils import logging
from bb.utils import executable
from bb.utils import typecheck
from bb.utils import path_utils

logger = logging.get_logger("bb")

# TODO: add sources. When compile() is calling, translate sources to files.
class Compiler(executable.ExecutableWrapper):
  """The base compiler class."""

  default_output_filename = None

  def __init__(self, verbose=0, files=[], dry_run=False):
    executable.ExecutableWrapper.__init__(self, verbose=verbose, dry_run=dry_run)
    # A common output directory for objects, libraries, etc.
    self._output_dir = ""
    self._output_filename = ""
    self._files = []
    if files:
      self.add_files(files)

  def get_files(self):
    """Returns list of source files.

    :returns: A list of strings.
    """
    return self._files

  def add_files(self, pathes):
    """Adds files from the list.

    :param pathes: A list of strings.
    """
    if not typecheck.is_sequence(pathes):
      raise TypeError("'files' must be a sequence.")
    for path in pathes:
      self.add_file(path)

  def add_file(self, path):
    """Adds file to the list of files. The path will be normalized by using
    :func:`os.path.abspath`.

    :param path: A string that represents file path.

    :returns: A normalized string path.

    :raises: TypeError
    """
    if typecheck.is_string(path):
      if not path_utils.exists(path):
        caller_frame = inspect.getouterframes(inspect.currentframe(), 2)
        filename = inspect.getsourcefile(caller_frame[2][0])
        possible_dir = path_utils.dirname(filename)
        alternative_path = path_utils.join(possible_dir, path)
        if path_utils.exists(alternative_path):
          return self.add_file(alternative_path)
      path = path_utils.abspath(path)
      if not path_utils.exists(path):
        raise Exception("Path doesn't exist: %s" % path)
      if not path in self._files:
        self._files.append(path)
      return path
    elif typecheck.is_callable(path):
      result = path()
      if not result:
        return
      elif typecheck.is_list(result):
        self.add_files(result)
      else:
        self.add_file(result)
    elif not path:
      return None
    else:
      raise TypeError("Unknown path type '%s' of '%s'" % (type(path), path))

  def get_language(self, *arg_list, **arg_dict):
    raise NotImplementedError

  def compile(self, *arg_list, **arg_dict):
    """Start compilation process."""
    raise NotImplementedError

  def set_output_filename(self, path):
    """Set output file name."""
    if not typecheck.is_string(path):
      raise TypeError("'path' must be a string")
    self._output_filename = path

  def get_output_filename(self):
    """Returns output file name."""
    default_filename = self.__class__.default_output_filename
    return self._output_filename or default_filename

  def get_output_dir(self):
    """Returns output directory."""
    return self._output_dir

  def set_output_dir(self, output_dir):
    """Sets output directory."""
    if not output_dir or not typecheck.is_string(output_dir):
      raise TypeError("'output_dir' must be a string or None")
    else:
      self._output_dir = output_dir

  def _setup_compile(self, output_dir):
    if output_dir is None:
      outputdir = self._output_dir
    elif not typecheck.is_string(output_dir):
      raise TypeError("'output_dir' must be a string or None")
