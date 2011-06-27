
from bbos.kernel.module import *
from bbos.hardware.drivers.serial.core import SerialCore

def p8x32_serial(kernel):
    message = kernel.receive_message(bbos_module_name())
    if not message:
        return
    if message.label == "BBOS_DRIVER_OPEN":
        print "Open serial connection with baudrate %d" % message.data[0]

bbos_module_name("P8X32_SERIAL")
bbos_module_thread(p8x32_serial)
#bbos_module_commands([])
bbos_module_copyright("Copyright (c) 2011 Slade Maurer, Alexander Sviridenko")
bbos_module_author("Slade Maurer, Alexander Sviridenko")
