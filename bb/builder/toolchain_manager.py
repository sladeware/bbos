#!/usr/bin/env python

_toolchains = list()

def toolchain(toolchain_class):
    global _toolchains
    _toolchains.append(toolchain_class)
    return toolchain_class

def get_toolchains():
    return _toolchains
