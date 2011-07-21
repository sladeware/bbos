#!/usr/bin/env python

"""Design blinker's application"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bb import app

blinker = app.new_application()
process = blinker.add_process('blinker')

from bb.os.hardware.boards import PropellerDemoBoard
board = PropellerDemoBoard([process])

if app.get_mode() is app.SIMULATION_MODE:
	blinker.run()

