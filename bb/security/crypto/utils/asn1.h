/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file asn1.h
 * @brief ASN.1 Support
 */

#ifndef __CRYPTO_UTILS_ASN1_H
#define __CRYPTO_UTILS_ASN1_H

#use "MPARITH.LIB"
#use "BASE64.LIB"

#include <bbos/types.h>

enum {
  ASN1_TAG_UNKNOWN	    = 0x00,
  ASN1_TAG_BOOLEAN          = 0x01,
  ASN1_TAG_INTEGER	    = 0x02,
  ASN1_TAG_HUGEINTEGER      = 0x0102,
  ASN1_TAG_BITSTRING        = 0x03,
  ASN1_TAG_OCTETSTRING      = 0x04,
  ASN1_TAG_NULL		    = 0x05,
  ASN1_TAG_OID		    = 0x06,
  ASN1_TAG_ENUMERATED	    = 0x0A,
  ASN1_TAG_PRINTABLE_STRING = 0x13,
  ASN1_TAG_IA5              = 0x16,
  ASN1_TAG_DATETIME	    = 0x17,
  ASN1_TAG_SEQUENCE	    = 0x30,
  ASN1_TAG_SET              = 0x31,
  ASN1_TAG_IP_ADDR	    = 0x40,
  ASN1_TAG_COUNTER	    = 0x41,
  ASN1_TAG_TIME_TICKS       = 0x43
};

/**
 * Structure to contain ASN.1 buffer information.
 */
typedef struct {
  uint16_t *buf;
  int16_t buf_len;
  uint16_t *end;
} asn1_ctx_t;

/* Prototypes */

void asn1_init(asn1_ctx_t *asn1_ctx, uint16_t *buf, int16_t buf_len);

int16_t asn1_length(asn1_ctx_t *asn1_ctx);

uint8_t *asn1_create_seq(asn1_ctx_t *asn1_ctx, uint8_t *start, uint8_t *end);

uint8_t *asn1_create_seq_tag(asn1_ctx_t *asn1_ctx, uint8_t *start, uint8_t *end,
uint8_t entry_tag);

uint8_t *asn1_append_int_tag(asn1_ctx_t *asn1_ctx, uint32_t val, uint8_t len,
uint8_t tag);

uint8_t *asn1_append_int(asn1_ctx_t *asn1_ctx, uint32_t val, uint8_t len);

uint8_t *asn1_append_oid(asn1_ctx_t *asn1_ctx, uint8_t *oid);

uint8_t *asn1_append_timetick(asn1_ctx_t *asn1_ctx, int32_t val);

uint8_t *asn1_append_string(asn1_ctx_t *asn1_ctx, uint8_t *str);

uint8_t *asn1_read_struct(uint8_t *pos, int16_t *tag, int32_t *len);

uint8_t *asn1_read_string(uint8_t *pos, int32_t len, uint8_t *str);

uint8_t *asn1_read_length(uint8_t* pos, int32_t *len);

uint8_t *asn1_read_tag(uint8_t* pos, int16_t *tag);

uint8_t *asn1_read_int(uint8_t *pos, int32_t len, int32_t *val);

uint8_t *asn1_read_oid(uint8_t* pos, int32_t len, uint8_t *oid);

uint8_t *asn1_write_long(asn1_ctx_t *asn1_ctx, uint8_t *out, long val);

int16_t asn1_oidcmp(uint8_t *oid1, uint8_t *oid2);

int16_t asn1_calc_oid_length(uint8_t *oid);

void pem_decode(uint8_t *in, size_t in_len, uint8_t *out, size_t *out_len,
uint8_t *type_str);

#endif /* __CRYPTO_UTILS_ASN1_H */


