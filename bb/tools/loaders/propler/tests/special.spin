CON
'
' Set these to suit the platform by modifying "Catalina_Common"
' Also, that is now where the PIN definitions for the platform
' are defined. Do not modify these in this file.
'
_clkmode  = xtal1 + pll16x
_xinfreq  = 5_000_000

PUB Start : ok | DATA, PAGE, BLOCK, XFER, MAX_LOAD
   dira[16..23]~~ 'Set pins to output
   repeat
     !outa[17]
     waitcnt(clkfreq / 6 + cnt)  ' Delay for some time

