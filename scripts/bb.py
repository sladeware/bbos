#!/usr/bin/env python

import optparse
import imp
import logging
import sys
import traceback

sys.path.pop(0)

import bb
from bb.config import host_os
import bb.config.importing as bbimport

logging.basicConfig(level=logging.DEBUG)

config = None
actions = dict()

class Action(object):
    def __init__(self, function, usage, short_desc, long_desc='',
                 error_desc=None, options=lambda obj, parser: None,
                 uses_basepath=True, hidden=False):
        self.function = function
        self.usage = usage
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.error_desc = error_desc
        self.options = options
        self.uses_basepath = uses_basepath
        self.hidden = hidden

    def __call__(self):
        return self.function()

    def get_action_descriptions(klass):
        """Returns a formatted string containing the short_descs for all actions."""
        action_names = klass.action_register.keys()
        action_names.sort()
        desc = ''
        for action_name in action_names:
            if not klass.action_register[action_name].hidden:
                desc += '  %s: %s\n' % (action_name,
                                        klass.action_register[action_name].short_desc)
        return desc

def get_actions():
    global actions
    return actions.values()

def get_action_names():
    global actions
    return actions.keys()

def register_action(name, action):
    global actions
    actions[name] = action

def is_supported_action(name):
    return name in get_action_names()

def get_action(name):
    global actions
    return actions[name]

def action(usage, short_desc, uses_basepath=False,
           options=lambda obj, parser: None):
    def _(function):
        action = Action(function, usage, short_desc, uses_basepath,
                        options=options)
        register_action(function.__name__, action)
        return function
    return _

class Actions:
    @action(
        usage='%prog help <action>',
        short_desc='Print help for a specific action.',
        uses_basepath=False)
    def help(action_name=None):
        """Prints help for a specific action.

        Args:
        action: If provided, print help for the action provided.

        Expects self.args[0], or 'action', to contain the name of the action in
        question.  Exits the program after printing the help message.
        """
        global config
        if not action_name:
            if len(config.args) > 1:
                config.args = [' '.join(config.args)]
            if len(config.args) != 1 or  not is_supported_action(config.args[0]):
                config.optparser.error('Expected a single action argument. '
                                       ' Must be one of:\n' +
                                       get_action_descriptions())
            action_name = config.args[0]
        action = get_action(action_name)
        config.optparser, unused_options = config._make_specific_parser(action)
        print config.optparser
        config._print_help_and_exit(exit_code=0)

    def _perform_build_options(config, optparser):
        optparser.add_option('--list-toolchains', dest='list_toolchains',
                             action='store_true',
                             help='List supported toolchains.')
    @action(
        usage='%prog build',
        options=_perform_build_options,
        short_desc='Build.',
        uses_basepath=False)
    def build():
        build_script_filename = "build.py"
        build_script_path = host_os.path.join(bb.env["BB_APPLICATION_HOME"],
                                              build_script_filename)
        if not host_os.path.exists(build_script_path):
            print "Build script '%s' doesn't exist" % build_script_path
        print "Run build script: %s" % build_script_path
        try:
            bbimport.enable_import_build()
            imp.load_source('bb.buildtime.application.build', build_script_path)
        except:
            print '-' * 70
            print "Exception in build script"
            print '-' * 70
            traceback.print_exc(file=sys.stdout)
            print '-' * 70

class Config(object):
    """Class to wrap build-script functionality.

    Attributes:
    optparser: An instnace of :class:`optparse.OptionParser`
    argv: The original command line as a list.
    args: The positional command line args left over after parsing
    the options.
    raw_input_fn: Function used for getting raw user input.
    error_fh: Unexpected errors are printer to this file handle.
    """

    def __init__(self, argv=sys.argv, optparser_class=optparse.OptionParser,
                 raw_input_fn=raw_input,
                 out_fh=sys.stdout,
                 error_fh=sys.stderr):
        self.argv = argv
        self.optparser_class = optparser_class
        self.raw_input_fn = raw_input_fn
        self.out_fh = out_fh
        self.error_fh = error_fh
        self.args = dict()
        self.options = optparse.Values()
        self.optparser = self._get_optparser()
        self.action = None
        for action in get_actions():
            action.options(self, self.optparser)

    def parse_command_line(self, argv=sys.argv):
        self.options, self.args = self.optparser.parse_args(argv[1:])
        if len(self.args) < 1:
            self._print_help_and_exit()
        if self.options.help:
            self._print_help_and_exit()
        action_name = self.args.pop(0)
        if not is_supported_action(action_name):
            self.optparser.error("Unknown action: '%s'\n" %
                                 (action_name, ))
        self.action = get_action(action_name)
        self.optparser, self.options = self._make_specific_parser(self.action)
        if self.options.help:
            self._print_help_and_exit()

    def get_option(self, name, default=None):
        value = getattr(self.options, name, default)
        return value

    def _print_help_and_exit(self, exit_code=2):
        self.optparser.print_help()
        sys.exit(exit_code)

    def _make_specific_parser(self, action):
        """Creates a new parser with documentation specific to 'action'.

        Args:
        action: An Action instance to be used when initializing the new parser.

        Returns:
        A tuple containing:
        parser: An instance of OptionsParser customized to 'action'.
        options: The command line options after re-parsing.
        """
        parser = self._get_optparser()
        parser.set_usage(action.usage)
        parser.set_description('%s\n%s' % (action.short_desc, action.long_desc))
        action.options(self, parser)
        options, unused_args = parser.parse_args(self.argv[1:])
        return parser, options

    def _get_optparser(self):
        class Formatter(optparse.IndentedHelpFormatter):
            def format_description(self, description):
                return description, '\n'

        parser = self.optparser_class(usage='%prog [options] <action> [options]',
                                      formatter=Formatter(),
                                      conflict_handler='resolve')
        parser.add_option('-h', '--help', action='store_true', dest='help',
                          help='Show the help message and exit.')
        parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
                          help='Be verbose')
        #parser.add_option('--dry-run', action='store_true', dest='dry_run',
        #                  help='Show only messages that would be printed in a real run.')
        #parser.add_option("--multiterminal", action="store_true",
        #                  dest="multiterminal",
        #                  help="Open each new running OS in a new terminal. "\
        #                      "Supports Linux.")
        return parser

config = Config()
config.parse_command_line()
action = config.action
try:
    action()
except Exception, e:
    print e
    exit(1)
