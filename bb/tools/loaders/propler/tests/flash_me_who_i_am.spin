CON
_clkmode  = xtal1 + pll16x
_xinfreq  = 5_000_000

PUB Start : ok
   dira[16..23]~~ 'Set pin to output
   outa[16 + cogid]~~
   repeat

