all:
	catalina -D DEMO -D NO_SCREEN -D NO_KEYBOARD -D NO_MOUSE -D NO_HMI -D NO_SD \
	-I./../ ../time.c ../sio.c -lc test_printf.c ../cog.c -o test_printf
