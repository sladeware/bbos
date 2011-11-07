#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

class KernelException(Exception):
    """The root kernel exception."""

class KernelTypeException(KernelException):
    """Raised when object has incorrect type."""

class KernelModuleException(KernelException):
    """Raised when we unable to load an expected module."""
