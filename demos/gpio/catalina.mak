
ROOT=../..

all:
	catalina -v -M2m -y -I. -I../.. -lci -DDEMO -o demo \
			$(ROOT)/bbos/kernel/port.c \
			$(ROOT)/bbos/kernel/idle.c \
			$(ROOT)/bbos/kernel/system.c \
			test.c \
			$(ROOT)/bbos/drivers/gpio/libgpio.c \
			$(ROOT)/bbos/drivers/gpio/p8x32a.c 

load:
	bstl -p 1 demo.binary


