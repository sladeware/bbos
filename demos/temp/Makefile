
ROOT=../..
DRIVERS=$(ROOT)/bbos/drivers

all:
	catalina -v -M2m -y -I. -I../.. -lci -DDEMO -DPC -o demo \
	demo.c \
	$(DRIVERS)/onewire/slaves/ds18b20.c $(DRIVERS)/onewire/bus.c \
	time.spin

load:
	bstl -p 3 demo.binary


