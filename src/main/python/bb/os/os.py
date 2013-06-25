#!/usr/bin/env python

import json

from bb.utils import typecheck

class Message(object):
  pass

class Port(object):
  pass

class Thread(object):
  pass

class Scheduler(object):
  pass

class Kernel(object):
  pass

class OS(object):

  def __init__(self, max_message_size=0):
    self._ports = []
    self._threads = []
    self._max_message_size = 0
    if max_message_size:
      self.set_max_message_size(max_message_size)

  @classmethod
  def build_from_json(cls, os_model):
    if typecheck.is_string(os_model):
      os_model = json.loads(os_model)
    os = cls(max_message_size=os_model.get('max_message_size', 0))
    for message_model in os_model.get('messages', []):
      pass

  def add_thread(self, thread):
    pass

  def get_running_thread(self):
    return None

  def request_message(self):
    return None

  def set_max_message_size(self, size):
    self._max_message_size = size

  def send_message(self, msg):
    if not isinstance(msg, Message):
      raise TypeError()
    pass

  def receive_message(self):
    return None

  def receive_message_from(self, pid):
    pass

  def delete_message(self, msg):
    if not isinstance(msg, Message):
      raise TypeError()
    pass
