"""Class encapsulates a static scheduler for a BBOS process.
"""
__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from common import *
import sys
import traceback

class StaticScheduler:
    def __init__(self, main_functions):
        self.main_functions = verify_list(main_functions)
        for name in self.main_functions:
            verify_string(name)

    def append_thread(self, name):
        self.main_functions.append(verify_string(name))

    def output(self, f, top, bottom):
        try:
            f.write(verify_string(top))
            for main_function in self.main_functions:
                f.write("    " + main_function + "(); \\\n")
            f.write(verify_string(bottom))
        except IOError:
            print "\nThere were problems writing static scheduler"
            traceback.print_exc(file = sys.stderr)
            raise
