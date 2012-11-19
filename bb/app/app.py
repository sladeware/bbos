#!/usr/bin/env python
#
# http://bionicbunny.org/
# Copyright (c) 2012 Sladeware LLC
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

"""This module describes BB application. An application is defined by a BB model
and is comprised of a set of processes running on a particular system topology
to perform work meeting the application's requirements. Each process correnspond
to the appropriate :class:`bb.application.mapping.Mapping` instance from
`mappings`.
"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import inspect
import imp
import fnmatch
import logging
import sys
import types

import bb
from bb import host_os
from bb.app.object import Object
from bb.app.builder import Builder, builder_class_factory
from bb.app.mapping import Mapping
from bb.app.imc_network import Network
from bb.app.binary import Binary
from bb.app.images import OSImage
from bb.app.shell import Shell
from bb.utils import pyimport
from bb.utils import typecheck

APPS_BY_DIRS = {}

class Application(bb.Object):
  """Base class for those who needs to maintain global application state.

  Normally you don't need to subclass this class.
  """

  DEFAULT_BUILD_DIR_NAME = "build"

  def __init__(self):
    self._network = Network()
    self._home_dir = Application.get_home_dir()
    self._build_dir = None
    self._build_scripts = []
    self._builders = {}
    self._shell = Shell()
    default_build_dir = host_os.path.join(self._home_dir,
                                          self.DEFAULT_BUILD_DIR_NAME)
    self.set_build_dir(default_build_dir, make=True)

  def __str__(self):
    return "%s[num_mappings=%d]" % (self.__class__.__name__,
                                    self.get_num_mappings())

  def get_shell(self):
    """Returns :class:`Shell` instance that represents shell of this
    application.
    """
    return self._shell

  def set_build_dir(self, path, make=False):
    """Sets path to the build directory."""
    if not host_os.path.exists(path):
      if not make:
        raise Exception("`%s' doesn't exist" % path)
      host_os.path.mkpath(path)
    self._build_dir = path

  def get_build_dir(self):
    return self._build_dir

  @classmethod
  def identify_instance(klass, obj=None):
    """Identifies and returns last active instance. If `obj` was provided,
    returns instance that keeps this object.
    """
    home_dir = obj and klass.find_home_dir(inspect.getsourcefile(obj)) \
        or klass.get_home_dir()
    return APPS_BY_DIRS.setdefault(home_dir, klass())

  @classmethod
  def identify_instance_or_die(klass, *args, **kwargs):
    """Throws exception if instance cannot be defined. See
    :func:`identify_instance`.
    """
    app = klass.identify_instance(*args, **kwargs)
    if not app:
      raise NotImplementedError()
    return app

  @classmethod
  def find_home_dir(klass, path):
    """Finds top directory of an application by a given path and returns path.
    """
    if not typecheck.is_string(path):
      raise TypeError("'path' must be a string")
    if host_os.path.isfile(path):
      (path, _) = host_os.path.split(path)
    while path is not host_os.sep:
      if ".bb" in host_os.listdir(path):
        return path
      (path, _) = host_os.path.split(path)
    return None

  @instancemethod
  def get_home_dir(self):
    return self._home_dir

  @classmethod
  def get_home_dir(klass):
    """Returns home directory"""
    for record in inspect.stack():
      (frame, filename, lineno, code_ctx, _, index) = record
      path = host_os.path.dirname(host_os.path.abspath(filename))
      if path.startswith(host_os.env["BB_PKG_DIR"]):
        continue
      home_dir = klass.find_home_dir(path)
      if home_dir:
        return home_dir
    return klass.find_home_dir(host_os.path.realpath(host_os.curdir))

  @classmethod
  def get_builder(klass, obj):
    return klass.identify_instance_or_die().get_builder(obj)

  @instancemethod
  def get_builder(self, obj):
    """Returns :class:`bb.app.builder.Builder` for the given
    `bb.app.object.Object`.
    """
    if obj in self._builders:
      return self._builders[obj]
    if typecheck.is_class(obj):
      if not issubclass(obj, Object):
        return None
      builder_class = builder_class_factory(obj)
      return self._builders.setdefault(obj, builder_class(obj))
    class_builder = self.get_builder(obj.__class__)
    if not class_builder:
      return None
    insts_builder = class_builder.clone()
    insts_builder.set_object(obj)
    self._builders[obj] = insts_builder
    return insts_builder

  def get_network(self):
    return self._network

  def get_mappings(self):
    return self._network.get_nodes()

  def get_num_mappings(self):
    """Returns number of mappings controlled by this application."""
    return len(self.get_mappings())

  def has_mapping(self, mapping):
    if not isinstance(mapping, Mapping):
      raise TypeError("Mapping must be derived from " \
                      "bb.app.mapping.Mapping")
    return self._network.has_node(mapping)

  def add_mapping(self, mapping):
    """Registers a mapping and adds it to the application network. Returns
    whether or not the mapping was added.
    """
    if self.has_mapping(mapping):
      return False
    self._network.add_node(mapping)
    return True

  def add_mappings(self, mappings):
    """Adds all mappings from list `mappings`. See :func:`add_mapping`."""
    if not typecheck.is_list(mappings):
      raise TypeError("'mappings' must be list")
    for mapping in mappings:
      self.add_mapping(mapping)

  def remove_mapping(self, mapping):
    if not isinstance(mapping, Mapping):
      raise TypeError("'mapping' must be derived from %s" % Mapping.__class__)
    if not self.has_mapping(mapping):
      return False
    self._network.remove_node(mapping)
    return True

  def remove_all_mappings(self):
    for mapping in self.get_mappings():
      self.remove_mapping(mapping)

  def get_mapping(self, name):
    if not typecheck.is_string(name):
      raise TypeError("must be a string")
    # Search for the mapping with specified name in the network
    for mapping in self.get_mappings():
      if mapping.get_name() == name:
        return mapping
    return None

  def get_binaries(self):
    pass

  def extract_images(self):
    """Analyses application and creates
    :class:`bb.app.image.Image`s. Returs list of images."""
    images = []
    logging.info("Process application")
    if not self.get_num_mappings():
      logging.debug("Application doesn't have any mapping")
      return
    for mapping in self.get_mappings():
      logging.info("Process mapping '%s'" % mapping.get_name())
      if not mapping.get_num_threads():
        logging.warning("Mapping", mapping.get_name(), "doesn't have threads."
                        "Skip this mapping.")
        continue
      logging.info("Generate OS")
      os = mapping.gen_os()
      # TODO(team): make different information available in different
      # verbose modes.
      logging.info("  processor = %s" % os.get_processor())
      logging.info("  num threads = %s" % os.get_num_threads())
      logging.info("  threads = [")
      for thread in os.get_threads():
        logging.info("   %s" % thread)
      logging.info("  ]")
      logging.info("  num messages = %d" % len(os.get_messages()))
      logging.info("  messages = [")
      for message in os.get_messages():
        logging.info("   %s" % str(message))
      logging.info("  ]")
      logging.info("  max message size = %s byte(s)" % os.get_max_message_size())
      if not os.get_num_kernels():
        raise Exception("OS should have atleast one kernel.")
      images.append(OSImage(os))
    return images

  def import_build_scripts(self, force=False):
    """Imports `_build.py` scripts."""
    if self._build_scripts and not force:
      return
    search_pathes = (host_os.env["BB_PKG_DIR"], self.get_home_dir())
    for search_path in search_pathes:
      for root, dirnames, filenames in host_os.walk(search_path):
        for filename in fnmatch.filter(filenames, '*_build.py'):
          # TODO(team): fix this
          if "bb/runtime/" in root:
            continue
          self._build_scripts.append(host_os.path.join(root, filename))
    # Check for default old fashion build.py
    path = host_os.path.join(self.get_home_dir(), "build.py")
    if not host_os.path.exists(path):
      logging.warning("Build script `%s' doesn't exist" % path)
    else:
      self._build_scripts.append(path)
    # Load build-scripts
    logging.debug("Found %d build script(s)" % len(self._build_scripts))
    ok = True
    for path in self._build_scripts:
      importer = pyimport.get_importer()
      name = importer.get_loader().get_module_fullname(path)
      logging.debug("Import `%s' as `%s'" % (path, name))
      try:
        mod = imp.load_source(name, path)
      except ImportError, e:
        ok = False
        logging.critical("Cannot import build-script `%s': %s" % (name, e))
    if not ok:
      exit(0)

  def build(self):
    """Builds this application."""
    self.import_build_scripts()
    images = self.extract_images()
    logging.info("%d image(s) to build" % len(images))
    for image in images:
      logging.info("Build %s" % image)
      binary = image.build()

def _home_import_hook():
  """Handles imports from fake `bb.app.home` package."""
  get_globals = globals
  get_locals = locals
  def hook(self, name, globals=None, locals=None, fromlist=None, level=-1):
    if name.startswith("bb.app.home") and fromlist:
      home_mod = __import__("bb.app.home", get_globals(), get_locals(),
                            [], -1)
      for _ in fromlist:
        try:
          _ = _.split(".")
          _ = host_os.path.join(*_)
          path = host_os.path.join(Application.get_home_dir(), "%s.py" % _)
          mod = imp.load_source(".".join([name, _]), path)
        except IOError, e:
          raise ImportError("Module `%s' doesn't exist" % (path))
        setattr(home_mod, _, mod)
      return home_mod
    return pyimport.ModuleImporter.import_module(self, name, globals, locals,
                                                 fromlist, level)
  # Update importer and install fixed importer
  importer = pyimport.get_importer()
  importer.import_module = types.MethodType(hook, importer,
                                            pyimport.ModuleImporter)
  pyimport.install_importer(importer)

_home_import_hook()

# Add bb primitives
setattr(bb, "get_app", Application.identify_instance)
setattr(bb, "get_bldr", Application.get_builder)
