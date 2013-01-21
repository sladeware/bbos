all:
	catalina -D DEMO -D NO_SCREEN -D NO_KEYBOARD -D NO_MOUSE -D NO_HMI -D NO_SD \
	-I./../ ../time.c ../sio.c -lc ../cog.c print_me_who_i_am.c \
	-o print_me_who_i_am
