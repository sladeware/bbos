
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

# Exception classes used by the CCompiler implementation classes
class CCompilerError (Exception):
    """Some compile/link operation failed."""

class UnknownCompiler(Exception):
    """"""

class UnknownFileError (CCompilerError):
    """Attempt to process an unknown file type."""

class CompileError(CCompilerError):
    pass
