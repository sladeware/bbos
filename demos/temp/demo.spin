CON

  _CLKMODE = XTAL1 + PLL16X
  _XINFREQ = 5_000_000

        DQ = 0

VAR
  long temp

OBJ
  pst  :  "Parallax Serial Terminal"
  ssr  :  "One_wire_P_002"

PUB DEMO_TEST
  pst.Start(115_200)

  pst.Str(String("D18B20 Temp sensor"))

  ssr.Start()
  ssr.Start_Conversion(DQ)
  ssr.Get_Temperature(temp)

DAT
{{
}}
