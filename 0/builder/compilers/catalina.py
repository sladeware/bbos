
from builder.compilers.unixc import UnixCCompiler

#_______________________________________________________________________________

class CatalinaCompiler(UnixCCompiler):
    executables = {"compiler"     : ["catalina"],
                   "linker_exe"   : ["catalina"]
                   }
    
    def __init__(self, verbose=False, dry_run=False):
        UnixCCompiler.__init__(self, verbose, dry_run)
    # __init__()

    def _gen_cc_options(self, pp_opts, debug, before):
        cc_opts = UnixCCompiler._gen_cc_options(self, pp_opts, debug, before)
        if self.verbose:
            cc_opts[:0] = ['-v']
        return cc_opts
    # _gen_cc_options()

    def _gen_ld_options(self, debug, before):
        ld_opts = UnixCCompiler._gen_ld_options(self, debug, before)
        if self.verbose:
            ld_opts[:0] = ['-v']
        return ld_opts
    # _gen_ld_options()

# class CatalinaCompiler
