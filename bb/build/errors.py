#!/usr/bin/env python

"""Provides exceptions used by the builder modules. Note that builder
modules may raise standard exceptions; in particular, :class:`SystemExit` is
usually raised for errors that are obviously the end-user's fault
(eg. bad command-line arguments)."""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

class BuilderError(Exception):
    pass

class BuilderInternalError(BuilderError):
    pass

class BuilderExecutionError(BuilderError):
    pass

class BuilderPlatformError(BuilderError):
    pass

class LoaderError(Exception):
    pass

class UnknownLoader(Exception):
    """"""

class UnknownCompiler(Exception):
    """"""

class UnknownFileError(Exception):
    """Attempt to process an unknown file type."""

class CompileError(Exception):
    """Some compile/link operation failed."""

class LinkError(Exception):
    pass

# Exception classes used by the CCompiler implementation classes
class CCompilerError(CompileError):
    """Some C/C++ compile/link operation failed."""
