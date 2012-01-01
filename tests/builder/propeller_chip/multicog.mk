
LCC_DIR=/usr/local/lib/catalina
CATALINA_SUPPORT_DIR = ../../../bb/builder/compilers/catalina

all:
	homespun -b $(LCC_DIR)/target/Catalina_LMM_Dynamic.spin -o LMM
	spinc LMM.binary > LMM_array.h
	dos2unix LMM_array.h
	catalina -lci -DDEMO -DPC -I. -I$(CATALINA_SUPPORT_DIR)/include $(CATALINA_SUPPORT_DIR)/lib/catalina_lmmk.c $(CATALINA_SUPPORT_DIR)/lib/catalina_time.c multicog.c -o multicog
