all:
	catalina -D DEMO -D NO_HMI \
	-I./../ ../time.c ../full_duplex_serial.c ../bitwise_op.c -lci test_full_duplex_serial.c ../cogutil.c -o test_full_duplex_serial
