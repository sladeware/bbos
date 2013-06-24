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

"""The mapping of hardware resources to software runtime components such as
processes, threads, queues and pools is determined at compile time. Thereby
permitting system integrators to cleanly separate the concept of what the
software does and where it does it. This mapping is represented by class
:class:`Mapping`.

Compile time mapping is critical for tuning a system based on application
requirements. It is useful when faced with an existing software application that
must run on a new or updated hardware platform, thus requiring re-tuning of the
application. Equally important is the flexibility afforded by compile time
mapping to system integrators that need to incorporate new software features as
applications inevitably grow in complexity.
"""

import json

from bb.app.object import Object
from bb.app.os import OS, Thread, Port
from bb.app.hardware.devices.processors import Processor
from bb.app.thread_distributors import ThreadDistributor, RoundrobinThreadDistributor
from bb.utils import typecheck
from bb.utils import logging

logger = logging.get_logger("bb")

class Mapping(Object):
  """The mapping of hardware resources to software runtime components such as
  processes, threads, queues and pools is determined at compile time.

  .. note::

    On this moment device drivers for controlled devices will not be
    added automatically as threads. They should be added manually.

  :param name: A string that represents mapping's name.
  :param processor: A
    :class:`~bb.app.hardware.devices.processors.processor.Processor` instance.
  :param os_class: A :class:`~bb.app.os.os.OS` class that will be used
    in os generation process.
  :param threads: A list of :class:`~bb.app.os.thread.Thread` instances.
  :param thread_distributor: A :class:`ThreadDistributor` instance that will
    distribute threads. By default :class:`RoundrobinThreadDistributor` instance
    will be used.
  """

  processor = None
  os_class = OS
  name_format = "M%d"

  def __init__(self, name=None, processor=None, os_class=None, threads=[],
               thread_distributor=None):
    Object.__init__(self)
    self._name = None
    self._threads = dict()
    self._ports = dict()
    self._os_class = None
    self._max_message_size = 0
    self._is_simulation_mode = False
    self._processor = None
    self._thread_distributor = None
    if not thread_distributor:
      thread_distributor = RoundrobinThreadDistributor()
    self.set_thread_distributor(thread_distributor)
    if name:
      self.set_name(name)
    if os_class or getattr(self.__class__, "os_class", None):
      self.set_os_class(os_class or self.__class__.os_class)
    if processor or self.__class__.processor:
      self.set_processor(processor or self.__class__.processor)
    if threads:
      self.register_threads(threads)

  def __str__(self):
    return '%s[name=%s,processor=%s,thread_distributor=%s,is_simulation_mode=%s]' \
        % (self.__class__.__name__,
           self._name,
           self._processor and self._processor.__class__.__name__ or None,
           self._thread_distributor and \
             self._thread_distributor.__class__.__name__ or None,
           self._is_simulation_mode)

  def __build__(self):
    return self.gen_os()

  def __call__(self, *args, **kwargs):
    """The mapping instance call eq to gen_os()."""
    return self.gen_os(*args, **kwargs)

  def set_max_message_size(self, size):
    """Manually set max message size.

    .. warning::

       Be careful, some messages may not fit this size when set manually.

    :param size: Max message size in bytes.
    """
    self._max_message_size = size

  def get_max_message_size(self):
    """Returns max message payload size in bytes."""
    return self._max_message_size

  def set_name(self, name):
    """Set mapping name.

    :param name: A string that will represent mapping name.
    """
    if not typecheck.is_string(name):
      raise TypeError("name must be string")
    self._name = name

  def get_name(self):
    """Returns mapping's name."""
    return self._name

  def set_thread_distributor(self, distributor):
    """Sets thread-distributor that will be used in OS generation process."""
    if not isinstance(distributor, ThreadDistributor):
      raise TypeError("Distributor must be derived from ThreadDistributor.")
    self._thread_distributor = distributor

  def get_thread_distributor(self):
    """Returns thread distributor.

    :returns: A :class:`ThreadDistributor` instance.
    """
    return self._thread_distributor

  def register_thread(self, thread, name=None):
    """Registers thread by its name. The name has to be unique within this
    mapping. If thread doesn't have a name and it wasn't provided, mapping will
    try to use its name format to generate one.

    If the thread has a port, this port will be registered by thread's name.

    .. seealso:: :func:`~bb.app.os.thread.Thread.get_name_format`

    .. todo::

      Improve name generation within a mapping; it has to be unique.

    :param thread: A :class:`~bb.app.os.thread.Thread` instance.
    :param name: Another name to register `thread`.

    :returns: A :class:`~bb.app.os.thread.Thread` instance.

    :raises: :class:`TypeError`
    """
    if not isinstance(thread, Thread):
      raise TypeError("Must be derived from bb.app.os.Thread: %s", thread)
    if name and not typecheck.is_string(name):
      raise TypeError()
    if name:
      thread.set_name(name)
    else:
      if thread.get_name() is None:
        frmt = thread.get_name_format()
        if not frmt:
          logger.warning("Thread %s doesn't have a name and the format cannot"
                         "be obtained to generate one." % thread)
          return
        thread.set_name(frmt % self.get_num_threads())
      name = thread.get_name()
    if thread.has_port():
      self.register_port(thread.get_port(), name)
    self._threads[name] = thread
    return thread

  def get_thread(self, name):
    if not typecheck.is_string(name):
      raise TypeError("'name' must be a string")
    return self._threads.get(name, None)

  def register_threads(self, threads):
    """Register threads.

    :param threads: A list of :class:`Thread` instances.
    :raises: :class:`TypeError`
    """
    if not typecheck.is_list(threads):
      raise TypeError()
    for thread in threads:
      self.register_thread(thread)

  def get_num_threads(self):
    """Returns number of threads within this mapping."""
    return len(self.get_threads())

  def get_threads(self):
    """Returns complete list of threads handled by this mapping."""
    return self._threads.values()

  def enable_simulation_mode(self):
    """Enables simulation mode."""
    self._is_simulation_mode = True

  def disable_simulation_mode(self):
    """Disables simulation mode."""
    self._is_simulation_mode = False

  def is_simulation_mode(self):
    """Returns whether or not this mapping is in simulation mode.

    :returns: ``True`` or ``False``.
    """
    return self._is_simulation_mode

  def get_processor(self):
    """Returns controlled processor.

    :returns: A :class:`~bb.app.hardware.devices.processors.processor.Processor`
      instance.
    """
    return self._processor

  def set_processor(self, processor):
    """Sets processor. The driver that controles this device will be added
    automatically.
    """
    if not isinstance(processor, Processor):
      raise TypeError("'processor' has to be derived from Processor class.")
    self._processor = processor
    driver = processor.get_driver()
    if not driver:
      logger.warning("Processor %s doesn't have a driver" % processor)
      return
    self.register_thread(driver)

  def is_processor_defined(self):
    """Returns whether or not a processor was defined. Returns ``True`` if the
    :class:`~bb.app.hardware.devices.processors.processor.Processor` instance
    was defined, or ``False`` otherwise.

    :returns: ``True`` or ``False``.
    """
    return not not self.get_processor()

  def set_os_class(self, os_class):
    """Sets OS class that will be used by :func:`gen_os` to generate OS
    instance.
    """
    if not issubclass(os_class, OS):
      raise TypeError("Must be derived from bb.app.os.OS class: %s"
                      % os_class)
    self._os_class = os_class

  def get_os_class(self):
    return self._os_class

  def gen_os(self):
    """Generates OS based on mapping analysis.

    :returns: An :class:`~bb.app.os.os.OS` derived instance.
    """
    logger.info("Process mapping %s" % self.get_name())
    processor = self.get_processor()
    if not processor:
      raise Exception("Processor wasn't defined")
    if not self.get_num_threads():
      raise Exception("Mapping doesn't have threads. Nothing to do.")
    distributor = self.get_thread_distributor()
    if not distributor:
      raise Exception("Thread-distributor wasn't defined")
    logger.info("Generate OS")
    distribution = distributor(self.get_threads(), processor)
    for core, threads in distribution.items():
      if not threads:
        continue
      kernel_class = self._os_class.kernel_class
      kernel = kernel_class(core=core, threads=threads)
      core.set_kernel(kernel)
    os = self._os_class(processor=processor,
                        max_message_size=self.get_max_message_size(),
                        ports=self.get_ports())
    # A few simple verifications
    if not os.get_num_kernels():
      raise Exception("OS should have atleast one kernel.")
    processor.set_os(os)
    return os

  def register_port(self, port, name):
    """Registers port within this mapping by the given name.

    :param port: A :class:`Port` derived instance.
    :param name: A string that represents name to which this port will be
      associated.

    :raises: TypeError
    """
    if not typecheck.is_string(name):
      raise TypeError("name must be a string")
    if not isinstance(port, Port):
      raise TypeError("port must be derived from Port")
    self._ports[name] = port

  def get_ports(self):
    """Returns a list of ports registered within this mapping.

    :returns: A list of :class:`~bb.app.os.port.Port` instances.
    """
    return self._ports.values()

  def serialize(self):
    return json.dumps({
      'name': self.get_name(),
      'os': json.loads(self.gen_os().serialize())
    })
