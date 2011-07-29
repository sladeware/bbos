
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import types

from bb.builder.compilers.unixc import UnixCCompiler

class CatalinaCompiler(UnixCCompiler):
    """Catalina is based upon LCC (a robust, widely used and portable C compiler 
    front-end), with a custom back-end that generates Large Memory Model (LMM) 
    PASM code for the Propeller."""

    executables = {
        "compiler"     : ["catalina"],
        "linker_exe"   : ["catalina"]
        }
    
    def __init__(self, verbose=False, dry_run=False):
        UnixCCompiler.__init__(self, verbose, dry_run)

    def define_macro(self, name, value=None, c_symbol=False):
        """Define a preprocessor macro for all compilations driven by this
        compiler object. The macro has two optional parameters. 
        The optional parameter 'value' should be a
        string; if it is not supplied, then the macro will be defined
        without an explicit value and the exact outcome depends on the
        compiler used (XXX true? does ANSI say anything about this?). 
        The optional parameter 'c_symbol' indicates whether it's a C symbol
        or a SPIN symbol."""
        # Delete from the list of macro definitions/undefinitions if
        # already there (so that this one will take precedence).
        i = self._find_macro(name)
        if i is not None:
            del self.macros[i]
        defn = ((name, value), c_symbol)
        self.macros.append(defn)

    def _gen_preprocess_macro_options(self, macros):
        """Catalina uses -D to define SPIN symbols. To define the C symbol XXX 
        on the command line use -W-DXXX. Note there should be no space between 
        the D and the XXX. Also note that when you define SPIN symbol XXX, 
        Catalina automatically defines a C symbol __Catalina_XXX."""
        options = []
	for macro, c_symbol in macros:
	    if not (type(macro) is types.TupleType and 1<= len(macro) <= 2):
		raise TypeError("bad macro definition " + repr(macro) + ": " + 
                                "each element of 'macros' list must be a 1- or 2-tuple")
            before = ''
            if c_symbol:
                before = '-W' # add -W option to define C symbol
	    if len(macro) == 1:
		options.append("%s-U%s" % (before, macro[0]))
	    elif len(macro) == 2:
		if macro[1] is None: # define with no explicit value
		    options.append("%s-D%s" % (before, macro[0]))
		else:
		    # XXX *don't* need to be clever about quoting the
		    # macro value here, because we're going to avoid the
		    # shell at all costs when we spawn the command!
		    options.append("%s-D%s=%s" % ((before, ) + macro))
            elif len(macro) == 3:
		if macro[1] is None: # define with no explicit value
		    options.append("%s-D%s" % (before, macro[0]))
		else:
		    # XXX *don't* need to be clever about quoting the
		    # macro value here, because we're going to avoid the
		    # shell at all costs when we spawn the command!
		    options.append("%s-D%s=%s" % ((before,) + macro))
        return options

    def _gen_cc_options(self, pp_opts, debug, before):
        cc_opts = UnixCCompiler._gen_cc_options(self, pp_opts, debug, before)
        if self.verbose:
            cc_opts[:0] = ['-v']
        return cc_opts

    def _gen_ld_options(self, debug, before):
        ld_opts = UnixCCompiler._gen_ld_options(self, debug, before)
        if self.verbose:
            ld_opts[:0] = ['-v']
        # Add macro! 
        ld_opts.extend(self._gen_preprocess_options(self.macros, []))
        return ld_opts


