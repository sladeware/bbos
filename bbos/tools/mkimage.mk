
all:
	gcc -I.. -I../lib/generic ../lib/generic/crc32.c ../bbos/image.c ../lib/generic/zlib.c mkimage.c -o mkimage
