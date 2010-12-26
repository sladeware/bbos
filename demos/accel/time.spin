' Catalina Code

DAT ' code segment

' Catalina Export bbos_delay_usec

 long ' align long

C_bbos_delay_usec
				jmp #LODA
				long @C_usec_delay
				rdlong r12, RI ' usec delay ' r2 - t1, r3 - t2, r12 - 4us
				shl r12, #2 ' compute (usec * 4)
				shr r2, #2 wz
	if_z	mov r2, #1
				mov r3, r12
				add r3, cnt
				sub r3, #41
	C_wait
				waitcnt r3, r12
				sub r2, #1 ' decrement
				test r2, r2 wz
				jmp #BRNZ
				long @C_wait
				jmp #RETN

' Catalina Import usec_delay

' end

