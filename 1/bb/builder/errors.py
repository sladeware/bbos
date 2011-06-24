
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

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
    pass

class LinkError(Exception):
    pass

# Exception classes used by the CCompiler implementation classes
class CCompilerError(CompileError):
    """Some compile/link operation failed."""

