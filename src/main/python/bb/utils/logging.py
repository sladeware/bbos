# http://www.bionicbunny.org/

from __future__ import absolute_import

from logging import *

# Make sure a NullHandler is available
# This was added in Python 2.7/3.2
try:
  from logging import NullHandler
except ImportError:
  class NullHandler(logging.Handler):
    def emit(self, record):
      pass

get_logger = getLogger

# NOTE: full-size format: %(levelname) 7s
_LOG_FORMAT = "[%(levelname).1s] %(message)s"
basicConfig(level=DEBUG, format=_LOG_FORMAT)
captureWarnings(True)

# Ensure the creation of the bb logger with a null handler. This ensures we
# don't get any 'No handlers could be found for logger "bb"' messages
logger = get_logger("bb")
if not logger.handlers:
  logger.addHandler(NullHandler())
