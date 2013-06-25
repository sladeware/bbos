# http://www.bionicbunny.org/
# Copyright (c) 2012-2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko

"""
  from bb.utils import executable

  class FooProgram(executable.ExecutableWrapper,
                   executable.ParamsReaderInterface):

    EXECUTABLE = "foo"
    OPTIONS = ["-g"]

    @executable.param_handler("sources")
    def add_sources(self, sources):
      print sources

  foo = FooProgram(dry_run=True)
  foo.read_params({"sources": (1, 2, 3)})

  >>> (1, 2, 3)

  foo.run()

  >>> foo -g
"""

import inspect
import types

from bb.utils.containers import DictWrapper
from bb.utils import typecheck
from bb.utils import spawn
from bb.utils import path_utils

param_handlers_cache = {}

def param_handler(param):
  """This function is used as decorator to bind handler to specific
  parameter.
  """
  def wrapper(handler):
    caller_frame = inspect.getouterframes(inspect.currentframe(), 2)
    class_name = caller_frame[1][3]
    param_handlers_cache.setdefault(class_name, {})
    param_handlers_cache[class_name][param] = handler.__name__
    return handler
  return wrapper

class ExecutableParams(DictWrapper):
  """This class represents parameters for an :class:`ExecutableWrapper`
  interface.
  """

  EXECUTABLE_CLASS = None

  def __init__(self, *args, **kwargs):
    DictWrapper.__init__(self, *args, **kwargs)
    self._context = dict()

  @property
  def context(self):
    return self._context

ExecutableParameters = ExecutableParams

class ParamsReaderInterface(object):

  param_handlers = {}

  def __init__(self):
    self.__param_handlers = self.param_handlers
    self.__processing_param = None

  def get_processing_params(self):
    return self.__processing_params

  def read_params(self, params):
    if not isinstance(params, self.Parameters):
      params = self.Parameters(params)
    if not "basedir" in params.context:
      caller_frame = inspect.getouterframes(inspect.currentframe(), 2)
      params.context["basedir"] = path_utils.dirname(inspect.getsourcefile(
          caller_frame[1][0])) or "."
    self.__processing_params = params
    if self.__param_handlers:
      for param, handler_name in self.__param_handlers.items():
        if not param in params:
          continue
        value = params[param]
        handler = getattr(self, handler_name)
        handler(value)
    self.__processing_params = None

ParametersReaderInterface = ParamsReaderInterface

class ExecutableWrapperMeta(type):

  def __new__(metacls, name, bases, d):
    cls = type.__new__(metacls, name, bases, d)
    # Initialize Parameters subclass
    Parameters = getattr(cls, "Parameters", None)
    if not Parameters or \
          (Parameters and Parameters in [getattr(base, "Parameters", None) \
                                           for base in bases]):
      base_params = []
      for base in bases:
        param_class = getattr(base, "Parameters", None)
        if param_class:
          base_params.append(param_class)
      cls.Parameters = type("%sParams" % cls.__name__, tuple(base_params),
                            {})
      cls.Parameters.EXECUTABLE_CLASS = cls
    # Initialize ParamsReaderInterface
    if ParamsReaderInterface in bases:
      if cls.__name__ in param_handlers_cache:
        cls.param_handlers.update(param_handlers_cache[cls.__name__])
    return cls

class ExecutableWrapper(object):
  """This class is wrapper for an executable.

  For each new executable class will be created special parameters class,
  e.g. :attr:`Compiler.Parameters` will be :class:`CompilerParams`.
  """

  Parameters = ExecutableParameters

  executable = None
  OPTIONS = []

  __metaclass__ = ExecutableWrapperMeta

  def __init__(self, executable=None, verbose=0, dry_run=False, options=[],
               params=[]):
    self._dry_run = False
    if dry_run:
      self.set_dry_run_mode(dry_run)
    if issubclass(self.__class__, ParamsReaderInterface):
      ParamsReaderInterface.__init__(self)
    self._executable = None
    if executable:
      self.set_executable(executable)
    elif getattr(self.__class__, "executable", None):
      self.set_executable(self.executable)
    self._verbose = 0
    if verbose:
      self.set_verbosity_level(verbose)
    self._options = []
    if options:
      self.set_options(options)
    elif hasattr(self, "OPTIONS"):
      self.set_options(self.OPTIONS)

  def set_verbosity_level(self, level):
    """Set verbosity level."""
    if not typecheck.is_int(level):
      raise TypeError()
    self._verbose = level

  def get_verbosity_level(self):
    """Returns verbosity level."""
    return self._verbose

  def check_options(self, options):
    if not typecheck.is_list(options):
      raise TypeError()
    for option in options:
      if not typecheck.is_string(option):
        raise TypeError()

  def set_options(self, options):
    self.check_options(options)
    self._options = options

  def add_options(self, options):
    for option in options:
      self.add_option(option)

  def add_option(self, option):
    self._options.append(option)

  def get_options(self):
    return self._options

  def enable_dry_run_mode(self):
    """Enables dry run mode."""
    self._dry_run = True

  def disable_dry_run_mode(self):
    """Disables dry run mode."""
    self._dry_run = False

  def set_dry_run_mode(self, true_or_false):
    if not typecheck.is_bool(true_or_false):
      raise TypeError("'true_or_false' has to be boolean")
    self._dry_run = true_or_false

  def is_dry_run_mode_enabled(self):
    """Returns ``True`` if dry run mode is enabled, ``False`` otherwise."""
    return self._dry_run

  def set_executable(self, executable):
    if not typecheck.is_string(executable):
      raise TypeError("Has to be string: %s" % executable)
    self._executable = executable

  def get_executable(self):
    """Returns handled executable."""
    return self._executable

  def check_executable(self):
    """Checks executable. All of them has to exist. Print warning if some
    executable was specified but not defined.
    """
    if not self._executable or not spawn.which(self._executable):
      return False
    return True

  def run(self, dry_run=False):
    dry_run = self.is_dry_run_mode_enabled() or dry_run
    exe = self.get_executable()
    try:
      spawn.spawn([exe] + self.get_options(),
                  debug=self.get_verbosity_level(), dry_run=dry_run)
    except spawn.ExecutionError, msg:
      raise Exception(msg)
