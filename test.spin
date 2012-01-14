CON
'
' Set these to suit the platform by modifying "Catalina_Common"
' Also, that is now where the PIN definitions for the platform
' are defined. Do not modify these in this file.
'
_clkmode  = xtal1 + pll16x
_xinfreq  = 5_000_000

VAR
  long StackA[32]
  long pin_offset

PUB Start : ok | DATA, PAGE, BLOCK, XFER, MAX_LOAD

  cognew(spinner, @StackA)

PUB spinner
  dira[16..23]~~ 'Set pins to output
  pin_offset := 0
  repeat
    !outa[16 + pin_offset]
    waitcnt(clkfreq / 400 * 15 + cnt)  ' Delay for some time
    pin_offset := (pin_offset + 1) // 8


