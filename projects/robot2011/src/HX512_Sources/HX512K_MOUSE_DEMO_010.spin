{
HYDRA XTREME 512K SRAM CARD Mouse Demo 1.0
Author: Andre' LaMothe, (C) Nurve Networks LLC

Update Log:

Description: This program is an example of using the CPLD on the HX512 to do
something other than be a memory controller. This little program uses the mouse
to control the LEDs on the HX512, right/left scrolls a little dot on the
program LEDs while the buttons turn on the read/write/latch lines.

NOTE: You must compile and download the appropriate ABEL program into the CPLD. The
filename of the new behavior is:

CD_ROOT:\SOURCES\mousetracker_01.abl - Source code.

If you do compile it yourself, make sure to set the final constraint file, so that
all IOs are "LVCMOS33" (instead of LVCMOS18), also change the output slewrates to "SLOW".

The pre-compiled JEDEC file for your convenience is:

CD_ROOT:\SOURCES\mousetracker_01.jed - Source code.
 

}
'///////////////////////////////////////////////////////////////////////
' CONSTANTS SECTION ////////////////////////////////////////////////////
'///////////////////////////////////////////////////////////////////////

CON

  _clkmode = xtal2 + pll4x            ' enable external clock and pll times 4
  _xinfreq = 10_000_000 + 0000        ' set frequency to 10 MHZ plus some error

  ' SRAM bus interface pin constants
  SRAM_CTRL_0 = 1 ' NET_RX_CLK       (expansion pin 10)
  SRAM_CTRL_1 = 2 ' NET_TX_DATA      (expansion pin 9)

  SRAM_STROBE = 30 ' USB_RXD (Prop TX ----> USB_RXD Host) (expansion pin 19)

  SRAM_IO_7 = 23 ' IO_7 (pin 28)
  SRAM_IO_6 = 22
  SRAM_IO_5 = 21
  SRAM_IO_4 = 20
  SRAM_IO_3 = 19
  SRAM_IO_2 = 18
  SRAM_IO_1 = 17
  SRAM_IO_0 = 16  ' IO_0 (pin 21)

  ' mouse buttons
  MOUSE_MIDDLE   = 2
  MOUSE_RIGHT    = 1
  MOUSE_LEFT     = 0
  
'//////////////////////////////////////////////////////////////////////////////
' VARIABLES SECTION ///////////////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////

VAR

'//////////////////////////////////////////////////////////////////////////////
' OBJECT DECLARATION SECTION //////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////

OBJ
  mouse : "mouse_iso_010.spin"       ' instantiate a mouse object
  
'//////////////////////////////////////////////////////////////////////////////
' PUBLIC FUNCTIONS ////////////////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////

PUB Start

  'start mouse on pingroup 2 (Hydra mouse port)
  mouse.start(2)

  ' set the data bus and clock to outputs, so we can talk to CPLD
  InitalizeIO

  ' main loop, track mouse and buttons and send to CPLD interface as agreed up in interface spec
  repeat

    ' test for right/left movement
    if (mouse.delta_x > 0)
      OUTA[ SRAM_IO_0 ] := 1
      OUTA[ SRAM_IO_1 ] := 0      
    elseif (mouse.delta_x < 0)
      OUTA[ SRAM_IO_1 ] := 1
      OUTA[ SRAM_IO_0 ] := 0      
    else 
      OUTA[ SRAM_IO_0 ] := 0
      OUTA[ SRAM_IO_1 ] := 0      

    ' test for buttons
    OUTA[ SRAM_IO_4 ] := mouse.button(MOUSE_LEFT)
    OUTA[ SRAM_IO_5 ] := mouse.button(MOUSE_MIDDLE)               
    OUTA[ SRAM_IO_6 ] := mouse.button(MOUSE_RIGHT)

    ' the CPLD needs a heartbeat for all the registered logic  
    Pulse_Clock

' ////////////////////////////////////////////////////////////////////

PUB Pulse_Clock
' Pulses the clock line on the CPLD which is ultimately attached to pin 38 of the CPLD

  OUTA[ SRAM_STROBE ] := $01
  OUTA[ SRAM_STROBE ] := $00  
  
' ////////////////////////////////////////////////////////////////////

PUB InitalizeIO
' Initializes the IO for HYDRA<->CPLD interface,
' in this case we just need to set the data bus to output as well as the clock strobe line

  ' set bus I/O directions for data bus
  OUTA[ SRAM_IO_7..SRAM_IO_0 ] := $00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ] := $FF            ' $FF ouput, $00 input

  ' set strobe
  OUTA[ SRAM_STROBE ]          := %0000000_0     ' clear strobe
  DIRA[ SRAM_STROBE ]          := $01            ' set to output                 

' ////////////////////////////////////////////////////////////////////

                        