
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import os
from types import *

from bb.builder.compilers.c import CCompiler
from bb.builder.errors import *
from bb.builder.spawn import spawn
from bb.apps.utils.dir import mkpath

#_______________________________________________________________________________

class UnixCCompiler(CCompiler):
    source_extensions = [".c", ".C", ".cc", ".cxx", ".cpp", ".m"]
    object_extension = ".o"
    executables = {'preprocessor' : None,
                   'compiler'     : ["cc"],
                   'compiler_so'  : ["cc"],
                   'compiler_cxx' : ["cc"],
                   'linker_so'    : ["cc", "-shared"],
                   'linker_exe'   : ["cc"],
                   'archiver'     : ["ar", "-cr"],
                   'ranlib'       : None,
                  }

    def __init__(self, verbose=False, dry_run=False):
        CCompiler.__init__(self, verbose, dry_run)

    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        compiler = self.executables['compiler']
        try:
            spawn(compiler + cc_args + [src, '-o', obj] + extra_postargs, 
                  verbose=self.verbose,
                  dry_run=self.dry_run)
        except BuilderExecutionError, msg:
            raise CompileError, msg

    def _link(self, objects, output_filename, output_dir=None, 
             libraries=None, library_dirs=None,
             debug=False, 
	     extra_preargs=None, extra_postargs=None, target_lang=None):
        """Linking."""
        objects, output_dir, libraries, library_dirs = \
            self._setup_link(objects, output_dir, libraries, library_dirs)
        lib_options = self._gen_lib_options(library_dirs, libraries)
        if output_dir is not None:
            output_filename = os.path.join(output_dir, output_filename)
        ld_options = self._gen_ld_options(debug, extra_preargs)
        if extra_postargs:
            ld_options.extend(extra_postargs)
        ld_options += (objects + lib_options + ['-o', output_filename])
        mkpath(os.path.dirname(output_filename))
        try:
            linker = self.executables['linker_exe']
            if target_lang == "c++" and self.executables["compiler_cxx"]:
                # skip over environment variable settings if /usr/bin/env
                # is used to set up the linker's environment.
                # This is needed on OSX. Note: this assumes that the
                # normal and C++ compiler have the same environment
                # settings.
                i = 0
                if os.path.basename(linker[0]) == "env":
                    i = 1
                    while '=' in linker[i]:
                        i = i + 1
                linker[i] = self.compiler_cxx[i]
            spawn(linker + ld_options, verbose=self.verbose, dry_run=self.dry_run)
        except BuilderExecutionError, msg:
            raise LinkError, msg

    def get_library_option(self, lib):
        return "-l" + lib


