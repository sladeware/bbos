# -*- coding: utf-8; -*-
#
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
# Author: Oleksandr Sviridenko <info@bionicbunny.org>

"""This module describes BB application."""

from __future__ import absolute_import

import inspect
import types
import os
import json

from bb.utils import typecheck
from bb.utils import path_utils
from bb.app.imc_network import Network
from bb.app.object import Object
from bb.app.mapping import Mapping

__all__ = ['Application']

class Application(Object):
  """Base class for those who needs to maintain global application state.

  Normally you don't need to subclass this class.

  By default root application directory name will be taken as application name.
  You can change that later with help of :func:`set_name` method.

  .. todo::

     Connect b3 build directory and application build directory.

  :param name: A string that represents application name.
  :param home_dir: represents root directory for the application.
  :param init_home_dir: if `home_dir` was specified and it's not existed home
         directory, the new directory will be initialized if `init_home_dir` is
         `True`.
  """

  settings_dirname = ".bbapp"

  def __init__(self, name=None, home_dir=None, init_home_dir=False, settings_dir=None):
    Object.__init__(self)
    self._name = None
    self._network = Network()
    self._home_dir = None
    self._build_dir = None
    self._settings_dir = None
    if settings_dir:
      if not path_utils.exists(settings_dir):
        raise IOError()
      self._settings_dir = settings_dir
    if home_dir:
      if not self.is_home_dir(home_dir) and init_home_dir:
        self.init_home_dir(home_dir)
      self._set_home_dir(home_dir)
    if name:
      self.set_name(name)
    elif self.get_home_dir():
      self.set_name(path_utils.basename(self.get_home_dir()))
    else:
      raise NotImplementedError()

  def get_name(self):
    """Returns application name."""
    return self._name

  def set_name(self, name):
    """Set application name.

    :param name: A string.
    """
    if not typecheck.is_string(name):
      raise TypeError()
    self._name = name

  def __str__(self):
    return "%s[home_dir='%s',num_mappings=%d]" \
        % (self.__class__.__name__, self.get_home_dir(),
           self.get_num_mappings())

  @classmethod
  def init_home_dir(cls, home_dir):
    """Initializes passed home directory if such wasn't already initialized.

    :returns: Path to home directory.
    """
    if not path_utils.exists(home_dir):
      raise IOError("'%s' doesn't exist" % home_dir)
    if not self._settings_dir:
      self._settings_dir = path_utils.join(home_dir, self.settings_dirname)
      path_utils.mkpath(settings_dir)
    return home_dir

  @classmethod
  def is_home_dir(cls, path):
    """Returns whether or not a given path is application home directory.

    :returns: `True` or `False`.
    :raises: :class:`TypeError`, :class:`IOError`
    """
    if not typecheck.is_string(path):
      raise TypeError("'path' has to be a string")
    elif not path_utils.exists(path):
      raise IOError("'%s' path doesn't exist" % path)
    return cls.settings_dirname in os.listdir(path)

  @classmethod
  def find_home_dir(cls, path):
    """Finds top directory of an application by a given path and returns home
    path. Returns `None` if home direcotry cannot be identified.

    :param path: Path to directory.

    :returns: Path as string or `None`.
    """
    if not typecheck.is_string(path):
      raise TypeError("'path' must be a string")
    elif not len(path):
      raise TypeError("'path' is empty")
    path = path_utils.realpath(path)
    if path_utils.isfile(path):
      (path, _) = path_utils.split(path)
    while path is not os.sep:
      if os.path.exists(path) and os.path.isdir(path):
        if cls.is_home_dir(path):
          return path
      (path, _) = path_utils.split(path)
    return None

  @classmethod
  def identify_home_dir(cls):
    for record in inspect.stack():
      (frame, filename, lineno, code_ctx, _, index) = record
      path = path_utils.dirname(path_utils.abspath(filename))
      home_dir = cls.find_home_dir(path)
      if home_dir:
        return home_dir
    return cls.find_home_dir(path_utils.realpath(os.curdir)) or os.getcwd()

  def _set_home_dir(self, home_dir):
    """Set application home directory. There should be no other applications
    registered to this home directory.

    :param home_dir: A string that represents path to home directory. The path
       should exists.

    :raises: :class:`IOError`
    """
    if not path_utils.exists(home_dir):
      raise IOError("`%s' doesn't exist" % home_dir)
    self._home_dir = home_dir

  def get_home_dir(self):
    """Returns home directory.

    :returns: A string that represents path to home directory.
    """
    return self._home_dir

  def get_settings_dir(self):
    return self._settings_dir

  def set_build_dir(self, path, make=False):
    """Sets path to the build directory. The build directory will be used to
    store temporary/autogenerated and compiled build-files.

    :param path: Build-directory name.
    :param make: Whether or not the path needs to be created.
    """
    if not path_utils.exists(path):
      if not make:
        raise IOError("`%s' doesn't exist" % path)
      path_utils.mkpath(path)
    self._build_dir = path

  def get_build_dir(self):
    """Returns build directory"""
    return self._build_dir

  def get_network(self):
    """Returns network that represents all the mappings and their relations
    within this application.
    """
    return self._network

  def gen_default_mapping_name(self, mapping):
    """Generates a name for a given mapping. This name will be unique within
    this application. This technique is used by the mapping itself for
    registration.

    :param mapping: A :class:`~bb.app.mapping.Mapping` instance.

    :returns: A string represented mapping's name.

    :raises: TypeError
    """
    if not isinstance(mapping, Mapping):
      raise TypeError()
    frmt = mapping.__class__.name_format
    return frmt % self.get_num_mappings()

  def get_mappings(self):
    """Returns list of mappings registered by this application.

    :returns: A list of :class:`Mapping` instances.
    """
    return self._network.get_nodes()

  def get_num_mappings(self):
    """Returns number of mappings controlled by this application."""
    return len(self.get_mappings())

  def has_mapping(self, mapping):
    if not isinstance(mapping, Mapping):
      raise TypeError("Mapping must be derived from bb.app.mapping.Mapping")
    return self._network.has_node(mapping)

  def add_mapping(self, mapping):
    """Registers a mapping and adds it to the application network.

    :param mapping: A :class:`Mapping` instance.

    :returns: Whether or not the mapping was added.
    """
    if self.has_mapping(mapping):
      return False
    self._network.add_node(mapping)
    return True

  def add_mappings(self, mappings):
    """Adds mappings. See also :func:`add_mapping`.

    :param mappings: A list of :class:`Mapping` instances.
    """
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

  def remove_mappings(self):
    for mapping in self.get_mappings():
      self.remove_mapping(mapping)

  def serialize(self):
    return json.dumps({
      'name': self.get_name(),
      'mappings': [json.loads(mapping.serialize()) for mapping in self.get_mappings()]
    })
