{{
        Copyright (c) 2012 Sladeware LLC
}}
CON
_clkmode  = xtal1 + pll16x
_xinfreq  = 5_000_000

PUB Start : ok | DATA, PAGE, BLOCK, XFER, MAX_LOAD
   dira[16..23]~~ 'Set pin to output
   repeat
     !outa[16 + cogid]
     waitcnt(clkfreq / 2 + cnt) ' Delay for half a second
