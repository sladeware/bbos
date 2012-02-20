all:
	catalina -lc -y -v -I../../libprop -DDEMO -DNO_HMI blink_me_who_i_am.c -o blink_me_who_i_am
