#!/usr/bin/env python
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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import inspect
import logging

import bb
from bb import host_os
from bb.utils import executable
from bb.utils import typecheck

class CompilerParameters(executable.ExecutableOptions):
  """A :class:`CompilerParameters` object represents the settings and options
  for an :class:`Compiler` interface.
  """

  COMPILER_CLASS = None

class CompilerMetaclass(type):

  def __new__(metaclass, name, bases, dictionary):
    class_ = type.__new__(metaclass, name, bases, dictionary)
    # Initialize CompilerParameters class (aka Parameters attribute)
    Parameters = getattr(class_, "Parameters", None)
    if not Parameters or \
          (Parameters and Parameters in [base.Parameters for base in bases]):
      class_.Parameters = type("%sParameters" % class_.__name__,
                               (CompilerParameters,), {})
      class_.Parameters.COMPILER_CLASS = class_
    return class_

class Compiler(executable.ExecutableWrapper, executable.OptionsReaderInterface):
  """The base compiler class."""

  Parameters = None

  OPTION_HANDLERS = {
    "sources": "add_sources"
  }

  __metaclass__ = CompilerMetaclass

  def __init__(self, verbose=0, sources=[], dry_run=False):
    executable.ExecutableWrapper.__init__(self)
    self._verbose = 0
    self._dry_run = False
    # A common output directory for objects, libraries, etc.
    self._output_dir = ""
    self._output_filename = ""
    self._sources = []
    if verbose:
      self.set_verbosity_level(verbose)
    if dry_run:
      self.set_dry_run_mode(dry_run)
    if sources:
      self.add_sources(sources)

  def set_verbosity_level(self, level):
    self._verbose = level

  def get_verbosity_level(self):
    return self._verbose

  def get_sources(self):
    """Returns list of sources."""
    return self._sources

  def add_sources(self, sources):
    """Adds sources from the list."""
    if not typecheck.is_sequence(sources):
      raise TypeError("Sources must be a sequence.")
    for source in sources:
      self.add_source(source)

  def add_source(self, source):
    """Adds a source to the list of sources. In the case when source is a path,
    it will be normalized by using :func:`os.path.abspath`.
    """
    if typecheck.is_string(source):
      if not host_os.path.exists(source):
        if self.get_processing_options():
          filename = self.get_processing_options().__file__
          options_dir = host_os.path.dirname(filename)
          alternative_source = host_os.path.join(options_dir, source)
          if host_os.path.exists(alternative_source):
            return self.add_source(alternative_source)
        raise Exception("Source doesn't exist: %s" % source)
      source = host_os.path.abspath(source)
      logging.debug("Add source `%s'" % source)
      if not source in self._sources:
        self._sources.append(source)
      return source
    elif typecheck.is_callable(source):
      result = source()
      if not result:
        return
      elif typecheck.is_list(result):
        self.add_sources(result)
      else:
        self.add_source(result)
    else:
      raise TypeError("Unknown source type '%s' of '%s'" %
                      (type(source), source))

  def enable_dry_run_mode(self):
    """Enables dry run mode."""
    self._dry_run = True

  def disable_dry_run_mode(self):
    """Disables dry run mode."""
    self._dry_run = False

  def set_dry_run_mode(self, true_or_false):
    if not typecheck.is_bool(true_or_false):
      raise TypeError("'true_or_false' has to be boolean")
    self._dry_run = true_or_false

  def is_dry_run_mode_enabled(self):
    return self._dry_run

  def get_language(self, *arg_list, **arg_dict):
    raise NotImplemented

  def compile(self, *arg_list, **arg_dict):
    raise NotImplemented

  def set_output_filename(self, filename):
    """Set output file name."""
    self._output_filename = filename

  def get_output_filename(self):
    """Returns output file name."""
    return self._output_filename

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
