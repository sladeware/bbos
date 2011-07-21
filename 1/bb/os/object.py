
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import types

import bb.app

class Object:
    """This class handle OS object activity to provide management of simulation
    and building modes.

    Just for internal use for each object the global mode MODE value will be 
    copied and saved as the special attribute. Thus the object will be able to 
    recognise environment's mode it which it was initially started."""

    def __init__(self):
        self.mode = bb.app.MODE
