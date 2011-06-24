#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import os
from types import *

#_______________________________________________________________________________

def which(program):
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

class PlatformError(Exception):
    """"""

class ExecutionError(Exception):
    """"""

def spawn(cmd, search_path=True, verbose=False, dry_run=False):
    """Run another program, specified as a command list 'cmd', in a new
    process. 'cmd' is just the argument list for the new process, ie.
    cmd[0] is the program to run and cmd[1:] are the rest of its arguments.
    There is no way to run a program with a name different from that of its
    executable.

    If 'search_path' is true (the default), the system's executable
    search path will be used to find the program; otherwise, cmd[0]
    must be the exact path to the executable.  If 'dry_run' is true,
    the command will not actually be run.

    Raise ExecutionError if running the program fails in any way; just
    return on success."""
    if not type(cmd) is ListType:
        raise TypeError("'cmd' must be a list")
    if verbose:
        print ' '.join(cmd)
    if os.name == 'posix':
        _spawn_posix(cmd, search_path, verbose, dry_run)
    else:
        raise PlatformError(
            "Don't know how to spawn programs on platform '%s'" % os.name)

# TODO: replace _std*_fd with sys.std*.fileno()
_stdin_fd = sys.stdin.fileno()
_stdout_fd = sys.stdout.fileno()
_stderr_fd = sys.stderr.fileno()

def _spawn_posix(cmd, search_path=True, verbose=False, dry_run=False):
    if dry_run:
        return

    # XXX add debug to arguments
    debug = True

    exec_fn = search_path and os.execvp or os.execcv

    if not debug:
        child_stdin, parent_stdout = os.pipe()
        parent_stdin, child_stdout = os.pipe()
        (_, child_stderr) = os.pipe()

    pid = os.fork()

    if not pid: # in a new child
        # Redirect STDIN, STDOUT and STDERR
        if not debug:
            os.dup2(child_stdin, _stdin_fd)
            os.dup2(child_stdout, _stdout_fd)
            os.dup2(child_stderr, _stderr_fd)

        try:
            exec_fn(cmd[0], cmd)
        except OSError, e:
            sys.stderr.write("unable to execute %s: %s\n" % (cmd[0], e.strerror))
            os._exit(1)
    else: # inside the parent
        # Loop until the child either exits or is terminated by a signal
        # (ie. keep waiting if it's merely stopped)
        while 1:
            try:
                (pid, status) = os.waitpid(pid, 0)
            except OSError, exc:
                import errno
                if exc.errno == errno.EINTR:
                    continue
                raise ExecutionError("command '%s' failed: %s" 
                                            % (cmd[0], exc[-1]))

            if not debug:
                os.close(child_stdin)
                os.close(child_stdout)
                os.close(child_stderr)

            if os.WIFSIGNALED(status):
                raise ExecutionError(
                    "command '%s' terminated by signal %d" 
                    % (cmd[0], os.WTERMSIG(status)))
            elif os.WIFEXITED(status):
                exit_status = os.WEXITSTATUS(status)
                if exit_status == 0:
                    return # hey, it succeeded!
                else:
                    raise ExecutionError(
                        "command '%s' failed with exit status %d" 
                        % (cmd[0], exit_status))
            elif os.WIFSTOPPED(status):
                continue
            else:
                raise ExecutionError(
                    "unknown error executing '%s': termination status %d" 
                    % (cmd[0], status))
# _spawn_posix()