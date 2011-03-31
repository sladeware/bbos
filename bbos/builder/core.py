
import sys, os
from types import *

from builder.debug import DEBUG
from builder.errors import *
from builder.util import grok_environment_error

# Mainly import these so setup scripts can "from builder.core import" them.
from builder.dist import Distribution
from builder.command import Command
from builder.extension import Extension

# This is a barebones help message generated displayed when the user
# runs the setup script with no arguments at all.  More useful help
# is generated with various --help options: global help, list commands,
# and per-command help.
USAGE_TEMPLATE = """\
usage: %(script)s [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
   or: %(script)s --help [cmd1 cmd2 ...]
   or: %(script)s --help-commands
   or: %(script)s cmd --help
"""

def gen_usage (script_name):
    script = os.path.basename(script_name)
    return USAGE_TEMPLATE % vars()

# Legal keyword arguments for the setup() function
setup_keywords = (
	'distclass', 'script_name', 'script_args', 'options', 'name', 'version',
	'author', 'author_email', 'maintainer', 'maintainer_email', 'url',
	'license', 'description', 'long_description', 'keywords', 'platforms',
	'classifiers', 'download_url', 'requires', 'provides', 'obsoletes',
)

# Legal keyword arguments for the Extension constructor
extension_keywords = (
    'name', 'sources', 'include_dirs',
    'define_macros', 'undef_macros',
    'library_dirs', 'libraries', 'runtime_library_dirs',
    'extra_objects', 'extra_compile_args', 'extra_link_args',
    'swig_opts', 'export_symbols', 'depends', 'language'
)

def setup(**attrs):
    # Determine the distribution class -- either caller-supplied or
    # our Distribution (see below).
    klass = attrs.get('distclass')
    if klass:
        del attrs['distclass']
    else:
        klass = Distribution

    if 'script_name' not in attrs:
        attrs['script_name'] = os.path.basename(sys.argv[0])
    if 'script_args' not in attrs:
        attrs['script_args'] = sys.argv[1:]

    # Create the Distribution instance, using the remaining arguments
    # (ie. everything except distclass) to initialize it
    try:
        dist = klass(attrs)
    except DistutilsSetupError, msg:
        if 'name' in attrs:
            raise SystemExit, "error in %s setup command: %s" % \
                  (attrs['name'], msg)
        else:
            raise SystemExit, "error in setup command: %s" % msg

    # Find and parse the config file(s): they will override options from
    # the setup script, but be overridden by the command line.
    dist.parse_config_files()

    if DEBUG:
        print "options (after parsing config files):"
        dist.dump_option_dicts()

    # Parse the command line; any command-line errors are the end user's
    # fault, so turn them into SystemExit to suppress tracebacks.
    try:
        ok = dist.parse_command_line()
    except DistutilsArgError, msg:
        raise SystemExit, gen_usage(dist.script_name) + "\nerror: %s" % msg

    if DEBUG:
        print "options (after parsing command line):"
        dist.dump_option_dicts()

    # And finally, run all the commands found on the command line.

    if ok:
        try:
            dist.run_commands()
        except KeyboardInterrupt:
            raise SystemExit, "interrupted"
        except (IOError, os.error), exc:
            error = grok_environment_error(exc)

            if DEBUG:
                sys.stderr.write(error + "\n")
                raise
            else:
                raise SystemExit, error

        except (DistutilsError,
                CCompilerError), msg:
            if DEBUG:
                raise
            else:
                raise SystemExit, "error: " + str(msg)

    return dist


