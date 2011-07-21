#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bb.builder.project import Wrapper
from bb.os.kernel.schedulers.staticscheduler import StaticScheduler

@Wrapper.bind("on_build", StaticScheduler)
def _build(sched, proj):
    try:
        f = open(proj.env['BBOS_H'], "a")
    except IOError:
        print "There were problems opening %s" % proj.env['BBOS_H']
        traceback.print_exc(file=sys.stderr)
        raise
    f.write("#define bbos_switch_thread()\\\n"
            "\twhile (1) {\\\n")
    for thread in sched.get_order():
        #f.write("\t\tbbos_thread_run(%s);\\\n" % thread.get_name())
        f.write("\t\t%s();\\\n" % thread.get_runner_name())
    f.write("\t}\n\n")
    f.close()
