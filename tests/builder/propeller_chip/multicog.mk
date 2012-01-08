
LCC_DIR=/usr/local/lib/catalina
CATALINA_SUPPORT_DIR = ../../../bb/builder/compilers/catalina

all:
	homespun -b $(LCC_DIR)/target/Catalina_LMM_dynamic.spin -o catalina_lmm
	spinc catalina_lmm.binary > catalina_lmm_array.h
	dos2unix LMM_array.h
	catalina -lci -DDEMO -DPC -I. -I$(CATALINA_SUPPORT_DIR)/include $(CATALINA_SUPPORT_DIR)/lib/catalina_lmm.c $(CATALINA_SUPPORT_DIR)/lib/catalina_time.c multicog.c -o multicog
