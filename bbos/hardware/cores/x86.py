"""No frills single X86 core.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos.hardware.core import *
from bbos.builder.common import *


class X86(BBOSCore):
    def __init__(self, process):
        BBOSCore.__init__(self, process)

        # Modify includes
        includes = ""
        self.process.append_include_files(includes)

        # Modify compiler include directories
        dirs = []
        self.modify_compiler_include_directories(dirs)

        # Modify compiler include argument
        self.modify_compiler_include_argument("-I")

        # Modify compiler name
        self.modify_compiler_name("gcc")

        # Modify compiler options
        options = ""
        self.modify_compiler_options(str(options))

