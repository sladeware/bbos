
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import traceback

from bbos.kernel.thread import Thread
from bbos.kernel.scheduler import Scheduler

class StateMachine(Scheduler):
	"""
	The state machine approach to real-time scheduler.

        The state machine are simple constructs used to perform several 
        activities in a specified order. For example, the operation of a
        washing machine or a dishwasher is easily described with a state 
        machine construct.
	"""
	def __init__(self, order=[]):
		Scheduler.__init__(self, "State Machine", is_dynamic=False)
                self.set_order(order)
        # __init__()

        def set_order(self, order):
            for thread in order:
                assert isinstance(thread, Thread), \
                    "Incorrect order of threads. %s is not a thread" % thread
            self.order = order
        # select_order()

        def get_order(self):
            return self.order
        # get_order()

        def config(self, proj):
            """
            Configure state maching scheduling policy.
            """
            try:
                f = open("bbos.h", "a")
            except IOError:
                print "There were problems writing to the end of %s" % "bbos.h"
                traceback.print_exc(file=sys.stderr)
                raise
            # Generating scheduling order
            print "Scheduling order: "
            f.write("#define bbos_switch_thread()\\\n")
            f.write("\twhile(1) {\\\n")
            for i in range(len(self.get_order())):
                thread = self.order[i]
                print "\t%d. %s" % (i, thread.get_name())
                f.write("\t\t%s();\\\n" % thread.get_entry())
            f.write("\t}\n")
            f.close()
            # Configure base class
            Scheduler.config(self, proj)
        # config()
