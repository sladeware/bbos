#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.app import Object
from bb.os.kernel import get_running_kernel
import sys, inspect

__all__ = ["MemPool"]

class Pointer(object):
  def __init__(self):
    object.__init__(self)

class MemoryChunk(object):
  """This class represents a memory chunk."""
  def __del__(self):
    if memspace is None:
      print "WARNING: memory chunk %s was returned without free()" % self

class MemorySpace(object):
    def __init__(self, total_space=0):
        self.__total_space = total_space
        self.__free_space = total_space
        self.__pointers = {}
        self.__chunks = []
        self.__s = {}

    def alloc(self, size):
        pointer = Pointer()
        chunk = MemoryChunk()
        self.__s[id(pointer)] = pointer
        self.__pointers[id(pointer)] = chunk
        self.__chunks.append(id(chunk))
        return pointer

    def free(self, pointer):
        chunk = self.__pointers[id(pointer)]
        del self.__pointers[id(pointer)]
        del self.__s[id(pointer)]
        self.__chunks.remove(id(chunk))
        del chunk        

memspace = MemorySpace(2 * 1024)

def malloc(size):
    """Subroutine for performing dynamic memory allocation."""
    assert size > 0, "The size of required memory chunks should be >0"
    return memspace.alloc(size)

def free(pointer):
    memspace.free(pointer)

class List(object):
    def __init__(self, lst):
        self.__list = lst

    def __getitem__(self, key):
        return self.__list[key]

    def __setitem__(self, key, value):
        self.__list[key] = value
        return value

import types

def mwrite(pointer, value):
  assert not pointer is None, "Can not write to NULL pointer"
  assert isinstance(pointer, Pointer), "Not a pointer class"
  skip_members = ('__module__', '__weakref__')
  if hasattr(pointer, '__bases__'):
    for name, method in inspect.getmembers(pointer):
      if not name in skip_members:
        delattr(pointer,name)
  # We will have a trouble by trying to change the type of an object
  # (by assigning to __bases__) when the new type wasn't compatible with the
  # old one. This happens when the underlying C data structure isn't the same
  # for both types. Thus we will replace them on the new types.
  if type(value) is types.ListType:
      value = List(value)
  # Start working with pointer
  pointer.__bases__ = (value.__class__,)
  for name, method in inspect.getmembers(value):
    if name in skip_members:
      continue
    setattr(pointer, name, method)

class MemPool(Object):
  def __init__(self, num_chunks=0, chunk_size=0):
    """Note that if number of chunks num_chunks is 0, it means that memory pool
    is unlimited. If chunk size chunk_size is 0, it means that chunk size is
    not important so we will not track this value."""
    Object.__init__(self)
    assert (chunk_size >= 0), "Chunk size must be greater than zero"
    assert (num_chunks >= 0), "Number of chunks can not be negative"
    self.__chunk_size = chunk_size
    self.__num_chunks = num_chunks
    self.__pointers = {}

  def malloc(self):
    if self.__num_chunks and self.count_chunks() >= self.__num_chunks:
      return None
    pointer = malloc(self.__chunk_size)
    self.__pointers[id(pointer)] = None
    return pointer

  def is_from(self, pointer):
    """Returns True if chunk was allocated from this pool. Returns False if 
    chunk was allocated from some other pool."""
    if id(pointer) in self.__pointers:
      return True
    return False 

  def count_chunks(self):
    return len(self.__pointers)

  def get_chunk_size(self):
    return self.__chunk_size

  def free(self, pointer):
    if not self.is_from(pointer):
      print "WARNING: %s can not be free by this pool" % pointer
      return
    del self.__pointers[id(pointer)]
    free(pointer)

if __name__ == '__main__':
  #string = malloc()
  #mwrite(string, 'Hello') # equalet of *string = 'Hello'
  #mwrite(string, 'Ji')
  ##free(string)
  pool = MemPool(2, 3)
  string1 = pool.malloc()
  string2 = pool.malloc()
  string3 = pool.malloc()
  mwrite(string1, 'Hi')
  #string.set('Hello')
  pool.free(string1)
  pool.free(string2)
  pool.free(string3)
  exit()

