
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.kernel.thread import Thread

class Idle(Thread):
    def __init__(self):
        Thread.__init__(self, "BBOS_IDLE")


