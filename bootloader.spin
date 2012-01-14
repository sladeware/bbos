CON
'
' Set these to suit the platform by modifying "Catalina_Common"
' Also, that is now where the PIN definitions for the platform
' are defined. Do not modify these in this file.
'
_clkmode  = Common#CLOCKMODE
_xinfreq  = Common#XTALFREQ
_stack    = Common#STACKSIZE
'
' Set these to suit the Generic SD Loader, or whatever other
' program is executed on the master propeller.
'
MODE      = Common#SIO_LOAD_MODE
BAUD      = Common#SIO_BAUD
'
' Set this to indicate the CPU we are:
'
THIS_CPU  = 1
'
' Set up Proxy, HMI and CACHE symbols and constants:
'
#include "Constants.inc"

OBJ
  Common : "Catalina_Common"                          ' Common Definitions
  Loader : "Catalina_SIO_Loader_Spinner"                  ' Low Level Loader
  SIO    : "Catalina_SIO_Plugin"                      ' SIO Card Plugin


VAR
  long StackA[32]
  long pin_offset

PUB Start : ok | DATA, PAGE, BLOCK, XFER, MAX_LOAD

  ' Set up the Registry - required to use the SIO Plugin
  Common.InitializeRegistry

  DATA  := Common#LOADTIME_ALLOC


  PAGE  := DATA  - Loader#PAGE_SIZE
  BLOCK := PAGE  - SIO#BLOCK_SIZE
  XFER  := BLOCK - 8
  DATA  := XFER

  MAX_LOAD := XFER ' cannot load past here

  'cognew(spinner, @StackA)

  '
  ' Start the SIO plugin
  '
  SIO.Start(BLOCK, Common#SI_PIN, Common#SO_PIN, MODE, BAUD, TRUE)


  ' Load a program from serial I/O to Hub and XMM RAM.
  ' The first 31k (32k minus any buffer space) is loaded
  ' into Hub RAM, and any data beyond 32k is loaded into
  ' XMM. Then the Propeller is restarted.
  Loader.Start (BLOCK, PAGE, XFER, THIS_CPU, MAX_LOAD)

PUB spinner
  dira[16..23]~~ 'Set pins to output
  pin_offset := 0
  repeat
    !outa[16 + pin_offset]
    waitcnt(clkfreq / 400 * 15 + cnt)  ' Delay for some time
    pin_offset := (pin_offset + 1) // 8


