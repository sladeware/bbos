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

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import bb
from bb.lib.utils import typecheck
from bb.tools.compilers import Compiler

class EventManager(object):
  def __init__(self):
    self._event_listeners = list()

  def add_event_listener(self, event_listener):
    self._event_listeners.append(event_listener)

  @classmethod
  def event(klass, event):
    def _(self, *args, **kargs):
      for listener in self._event_listeners:
        action = getattr(listener, "on_" + event.__name__, None)
        if action:
          action()
      return event(self, *args, **kargs)
    return _

class Toolchain(EventManager):
  class EventListener(object):
    pass

  def __init__(self, sources=[], verbose=False, compiler=None, loader=None):
    EventManager.__init__(self)
    if not typecheck.is_sequence(sources):
      raise Exception("Must be sequence")
    self._verbose = verbose
    self._sources = []
    self._compiler = None
    self._loader = None
    self._dry_run = False
    if compiler:
      self.set_compiler(compiler)
    if loader:
      self.set_loader(loader)
    # NOTE: the sources must be added at the end of initialization
    if sources:
      self.add_sources(sources)

  @classmethod
  def get_name(klass):
    return klass.__name__.lower()

  def enable_dry_run_mode(self):
    self._dry_run = True

  def disable_dry_run_mode(self):
    self._dry_run = False

  def set_dry_run_mode(self, value):
    self._dry_run = value

  def is_dry_run_mode_enabled(self):
    return self._dry_run

  def add_sources(self, sources):
    if not typecheck.is_sequence(sources):
      raise TypeError()
    for source in sources:
      self.add_source(source)

  def get_sources(self):
    return self._sources

  def add_source(self, source):
    """Add a source to the project. In the case when source is a
    path, it will be normalized by using :func:`os.path.abspath`.
    """
    if not source:
      raise Exception("WTF!")
    if typecheck.is_string(source):
      source = bb.host_os.path.abspath(source)
      if not bb.host_os.path.exists(source):
        raise Exception("Source doesn't exist: %s" % source)
      print "Add source %s" % source
      if not source in self._sources:
        self._sources.append(source)
      return source
    raise TypeError("unknown source type '%s' of '%s'"
                    % (type(source), source))

  def set_compiler(self, compiler):
    if not isinstance(compiler, Compiler):
      raise errors.UnknownCompiler
    self._compiler = compiler
    return compiler

  def get_compiler(self):
    return self._compiler

  @property
  def compiler(self):
    return self.get_compiler()

  def get_loader(self):
    return self._loader

  @property
  def loader(self):
    return self.get_loader()

  #@EventManager.event
  def build(self, sources=[], output_dir=None, verbose=0, dry_run=None,
            *args, **kvargs):
    """Start building process."""
    # Control verbose
    if not typecheck.is_int(verbose):
      raise TypeError('verbose must be an int')
    self.verbose = verbose
    if sources:
      self.add_sources(sources)
    if output_dir:
      self.compiler.set_output_dir(output_dir)
    # Control dry run mode
    if not dry_run is None:
      self.set_dry_run_mode(dry_run)
    print 'Building...'
    if self.compiler:
      self.compiler.check_executables()
      self.compiler.dry_run = self.is_dry_run_mode_enabled()
      if self.verbose:
        self.compiler.verbose = self.verbose
    # Run specific build process
    if not len(self.get_sources()):
      print "Nothing to build"
      return
    self._build(*args, **kvargs)

  def _build(self, *args, **kvargs):
    raise NotImplementedError
