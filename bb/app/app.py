#!/usr/bin/env python
#
# http://bionicbunny.org/
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

It combines all of the build systems of all of the defined processes. Therefore
the application includes the models of processes, their communication, hardware
description, simulation and build specifications. At the same time the processes
inside of an application can be segmented into `clusters`, or a group of CPUs.
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
from bb.utils import typecheck
from bb.application.mapping import Mapping
from bb.application.imc_network import Network
from bb.utils import pyimport
from bb.application.binary import Binary
from bb.application.images import OSImage

APPS_BY_DIRS = {}

class Application(bb.Object):
  """Base class for those who need to maintain global application state.

  Normally no need to subclass this application.
  """

  def __init__(self):
    self._network = Network()
    self._home_dir = Application.get_home_dir()
    self._build_scripts = []

  def __str__(self):
    return "%s[num_mappings=%d]" % (self.__class__.__name__,
                                    self.get_num_mappings())

  @classmethod
  def identify_instance(klass, object_=None):
    """Identifies and return last active instance. If `object_` was provided,
    returns instance that keeps this object.
    """
    home_dir = object_ and klass.find_home_dir(inspect.getsourcefile(object_)) \
        or klass.get_home_dir()
    return APPS_BY_DIRS.setdefault(home_dir, klass())

  @classmethod
  def identify_instance_or_die(klass, *args, **kwargs):
    app = klass.identify_instance(*args, **kwargs)
    if not app:
      raise NotImplementedError()
    return app

  @classmethod
  def find_home_dir(klass, path):
    """Find top directory of an application by a given path."""
    if not typecheck.is_string(path):
      raise TypeError("'path' must be a string")
    if bb.host_os.path.isfile(path):
      (path, _) = bb.host_os.path.split(path)
    while path is not bb.host_os.sep:
      if ".bb" in bb.host_os.listdir(path):
        return path
      (path, _) = bb.host_os.path.split(path)
    return None

  @instancemethod
  def get_home_dir(self):
    return self._home_dir

  @classmethod
  def get_home_dir(klass):
    for record in inspect.stack():
      (frame, filename, lineno, code_ctx, _, index) = record
      path = bb.host_os.path.dirname(bb.host_os.path.abspath(filename))
      if path.startswith(bb.host_os.env["BB_PACKAGE_PATH"]):
        continue
      home_dir = klass.find_home_dir(path)
      if home_dir:
        return home_dir
    return klass.find_home_dir(bb.host_os.path.realpath(bb.host_os.curdir))

  def get_network(self):
    return self._network

  def get_mappings(self):
    return self._network.get_nodes()

  def get_num_mappings(self):
    return len(self.get_mappings())

  def has_mapping(self, mapping):
    if not isinstance(mapping, Mapping):
      raise TypeError("Mapping must be derived from " \
                      "bb.application.mapping.Mapping")
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
    if not typecheck.is_list(mappings):
      raise TypeError("'mappings' must be list")
    for mapping in mappings:
      self.add_mapping(mapping)

  def remove_mapping(self, mapping):
    if not isinstance(mapping, Mapping):
      raise TypeError("Must be bb.application.mapping.Mapping")
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
    if self._build_scripts and not force:
      return
    search_pathes = (bb.host_os.env["BB_PACKAGE_PATH"], self.get_home_dir())
    for search_path in search_pathes:
      for root, dirnames, filenames in bb.host_os.walk(search_path):
        for filename in fnmatch.filter(filenames, '*_build.py'):
          # TODO(team): fix this
          if "bb/runtime/" in root:
            continue
          self._build_scripts.append(bb.host_os.path.join(root, filename))
    # Check for default old fashion build.py
    path = bb.host_os.path.join(self.get_home_dir(), "build.py")
    if not bb.host_os.path.exists(path):
      logging.warning("Build script `%s' doesn't exist" % path)
    else:
      self._build_scripts.append(path)
    # Load build-scripts
    logging.debug("Found %d build script(s)" % len(self._build_scripts))
    for path in self._build_scripts:
      importer = pyimport.get_importer()
      name = importer.get_loader().get_module_fullname(path)
      logging.debug("Import `%s' as `%s'" % (path, name))
      mod = imp.load_source(name, path)

  def build(self):
    self.import_build_scripts()
    images = self.extract_images()
    logging.info("%d image(s) to build" % len(images))
    for image in images:
      binary = image.build()

def _home_import_hook():
  def hook(self, name, globals_=None, locals_=None, from_=None, level=-1):
    if name.startswith("bb.application.home") and from_:
      home_mod = __import__("bb.application.home", globals(), locals(), [], -1)
      for _ in from_:
        try:
          path = bb.host_os.path.join(Application.get_home_dir(), "%s.py" % _)
          mod = imp.load_source(".".join([name, _]), path)
        except IOError, e:
          raise ImportError("Module `%s' doesn't exist" % (path))
        setattr(home_mod, _, mod)
      return home_mod
    return pyimport.ModuleImporter.import_module(self, name, globals_, locals_,
                                                 from_, level)
    return None
  # Update importer and install fixed importer
  importer = pyimport.get_importer()
  importer.import_module = types.MethodType(hook, importer,
                                            pyimport.ModuleImporter)
  pyimport.install_importer(importer)

_home_import_hook()
