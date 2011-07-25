
all:
	gcc -I../.. ../lib/generic/crc32.c ../boot/image.c ../lib/generic/zlib.c mkimage.c -o mkimage
