
LCC_DIR=/usr/local/lib/catalina
CATALINA_SUPPORT_DIR = ../../../bb/builder/compilers/catalina

all:
	catalina -lci -lmulticog -DDEMO -DPC -I. multicog.c -o multicog
