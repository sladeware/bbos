
ROOT=../..

all:
	catalina -v -M2m -y -I. -I../.. -lci -DDEMO -DPC -o demo \
	demo.c ../../bbos/drivers/stamp.c ../../bbos/drivers/accel/h48c.c time.spin

load:
	bstl -p 3 demo.binary


