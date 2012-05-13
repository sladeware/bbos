#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import multiprocessing
import types

class Memory(object):
    def __init__(self, size=None):
        self.__size = size
        # XXX: do we need to use array or dictionary. What if the memory size
        # will be a few Gb? First of all we need to hide this, see __init_buf(),
        # write(), read().
        self.__buf = None
        self.__init_buf()
        self.clear()

    def __init_buf(self):
        self.__buf = multiprocessing.Manager().dict()

    def clear(self):
        #self.__buf = dict()
        pass

    def dump(self):
        print self.__buf

    def write(self, addr, src, n=None):
        if isinstance(src, types.IntType):
            src = "%d" % src
        if not n:
            n = len(src)
        for i in range(n):
            self.__buf[addr + i] = src[i]

    def read(self, addr, n):
        data = [0] * n
        for i in range(n):
            data[i] = self.__buf.get(addr + i, 0)
        return data

    def get_size(self):
        return self.__size

class RAM(Memory):
    """Random access memory (RAM)."""

