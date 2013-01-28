/*
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 */

/**
 * @file asn1.h
 * @brief ASN.1 Support
 */

#ifndef __BB_CRYPTO_ASN1_H
#define __BB_CRYPTO_ASN1_H

#use "MPARITH.LIB"
#use "BASE64.LIB"

#include <bb/os/types.h>

enum {
  ASN1_TAG_UNKNOWN = 0x00,
  ASN1_TAG_BOOLEAN = 0x01,
  ASN1_TAG_INTEGER = 0x02,
  ASN1_TAG_HUGEINTEGER = 0x0102,
  ASN1_TAG_BITSTRING = 0x03,
  ASN1_TAG_OCTETSTRING = 0x04,
  ASN1_TAG_NULL = 0x05,
  ASN1_TAG_OID = 0x06,
  ASN1_TAG_ENUMERATED = 0x0A,
  ASN1_TAG_PRINTABLE_STRING = 0x13,
  ASN1_TAG_IA5 = 0x16,
  ASN1_TAG_DATETIME = 0x17,
  ASN1_TAG_SEQUENCE = 0x30,
  ASN1_TAG_SET = 0x31,
  ASN1_TAG_IP_ADDR = 0x40,
  ASN1_TAG_COUNTER = 0x41,
  ASN1_TAG_TIME_TICKS = 0x43
};

/**
 * Structure to contain ASN.1 buffer information.
 */
typedef struct {
  uint16_t *buf;
  int16_t buf_len;
  uint16_t *end;
} asn1_ctx_t;

/**
 * Initializes an asn1_ctx_t.
 *
 * @param asn1_ctx A pointer to asn1_ctx_t structure.
 * @param buf A pointer to the buffer used to store the ASN.1 sequence.
 * @param buf_len Length of the buffer pointer to by pBuffer.
 */
void asn1_init(asn1_ctx_t *asn1_ctx, uint16_t *buf, int16_t buf_len);

/**
 * Gets the current length of the ASN.1 sequence.
 * @param asn1_ctx A pointer to asn1_ctx_t structure.
 *
 * Return value:
 *
 * Length of the ASN.1 sequence.
 */
int16_t asn1_length(asn1_ctx_t *asn1_ctx);

/**
 * Creates a ASN.1 sequence.
 *
 * @param asn1_ctx
 * @param start
 * @param end
 *
 * Return value:
 *
 * Pointer to the end of the sequence.
 *
 * Description:
 *
 * asn1_create_seq_type is passed ASN1_TAG_SEQUENCE.
 *
 * See also
 *
 * asn1_create_seq_type
 */
uint8_t *asn1_create_seq(asn1_ctx_t *asn1_ctx, uint8_t *start, uint8_t *end);

/**
 * Creates a ASN.1 sequence of tag entry_tag. Shifts the bytes pointed to by 
 * start and end and prepend them with the type and length.
 *
 * @param asn1_ctx A pointer to asn1_ctx_t structure.
 * @param start Pointer to the start of the sequence. Specify NULL to start at 
 * the beginning of the buffer.
 * @param end Pointer to the end of the sequence. Specify NULL to end at the end
 * of the buffer.
 * @param entry_tag Type to assign to the new sequence.
 *
 * @return
 *
 * Pointer to the end of the sequence.
 *
 * Example:
 *
 * This example will shift bytes 0-10 over by 2 bytes and write
 * the type at byte 0 and the length at byte 1.  The function
 * will then return start_buf+12.
 *
 * asn1_create_seq_tag(&asn1, start_buf, start_buf+10, ASN1_TAG_SEQUENCE);
 */
uint8_t *asn1_create_seq_tag(asn1_ctx_t *asn1_ctx, uint8_t *start, uint8_t *end,
                             uint8_t entry_tag);

/**
 * Appends an integer to the end of a ASN.1 sequence of type tag.
 *
 * @param asn1_ctx A pointer to asn1_ctx_t structure.
 * @param val Integer value to append.
 * @param len Length in bytes of the integer to store (for example if you were to
 * put val=200 you may only want to store it as 1 byte).
 * @param tag One of the ASN.1 types to prepend to the integer.
 *
 * @return
 *
 * Pointer to the end of the integer.
 */
uint8_t *asn1_append_int_tag(asn1_ctx_t *asn1_ctx, uint32_t val, uint8_t len,
                             uint8_t tag);

/**
 * Appends an integer to the end of an ASN.1 sequence of type ASN1_TAG_INTEGER.
 *
 * @return
 *
 * Pointer to the end of the integer.
 */
uint8_t *asn1_append_int(asn1_ctx_t *asn1_ctx, uint32_t val, uint8_t len);

/**
 * Appends an OID to the end of an ASN.1 sequence.
 *
 * @param asn1_ctx A pointer to asn1_ctx_t structure.
 * @param oid A string representation of an OID. (ex 1.2.3.4.5)
 *
 * @return
 *
 * Return a pointer to the end of the ASN.1 sequence.
 */
uint8_t *asn1_append_oid(asn1_ctx_t *asn1_ctx, uint8_t *oid);

/**
 * Appends timeticks to the end of an ASN.1 sequence.
 *
 * @param asn1_ctx A pointer to asn1_ctx_t structure.
 * @param val Time tick value to append.
 *
 * @return
 *
 * Pointer to the end of the integer.
 */
uint8_t *asn1_append_timetick(asn1_ctx_t *asn1_ctx, int32_t val);

/**
 * Appends a string to the end of an ASN.1 sequence.
 *
 * @param asn1_ctx A pointer to asn1_ctx_t structure.
 * @param str String to append to the ASN.1 sequence.
 *
 * @return
 *
 * Return a pointer to the end of the ASN.1 sequence.
 */
uint8_t *asn1_append_string(asn1_ctx_t *asn1_ctx, uint8_t *str);

/**
 * Reads data structure such as tag and length.
 * @param pos
 * @param tag
 * @param len
 */
uint8_t *asn1_read_struct(uint8_t *pos, int16_t *tag, int32_t *len);

/**
 * Reads the ASN.1 string from an ASN.1 sequence.
 *
 * @param pos Pointer to the position in the ASN.1 sequence.
 * @param len Length of the string.
 * @param str Pointer to a buffer to hold the string.
 *
 * @return:
 *
 * Position in the ASN.1 sequence after the string.
 */
uint8_t *asn1_read_string(uint8_t *pos, int32_t len, uint8_t *str);

/**
 * Reads the ASN.1 length from an ASN.1 sequence.
 *
 * @param pos Pointer to the position in the ASN.1 sequence.
 * @param len Pointer to an integer to recieve the length.
 *
 * @return
 *
 * Position in the ASN.1 sequence after the length.
 */
uint8_t *asn1_read_length(uint8_t* pos, int32_t *len);

/**
 * Reads the ASN.1 tag from an ASN.1 sequence.
 *
 * @param pos Pointer to the position in the ASN.1 sequence.
 * @param tag Pointer to an integer to recieve the type.
 *
 * @return
 *
 * Position in the ASN.1 sequence after the type.
 */
uint8_t *asn1_read_tag(uint8_t* pos, int16_t *tag);

/**
 * Reads the ASN.1 int from an ASN.1 sequence.
 * @param pos Pointer to the position in the ASN.1 sequence.
 * @param len Length of the integer.
 * @param val Pointer to a long to hold the integer.
 *
 * @return
 *
 * Position in the ASN.1 sequence after the integer.
 */
uint8_t *asn1_read_int(uint8_t *pos, int32_t len, int32_t *val);

/**
 * Reads the ASN.1 oid from an ASN.1 sequence. 
 *
 * @param pos Pointer to the position in the ASN.1 sequence.
 * @param len Length of the oid.
 * @param oid Pointer to a buffer to hold the oid.
 *
 * @return
 *
 * Position in the ASN.1 sequence after the oid.
 */
uint8_t *asn1_read_oid(uint8_t* pos, int32_t len, uint8_t *oid);

/**
 * Writes a long value to the ASN.1 sequence.
 * @param asn1_ctx
 * @param out
 * @param val
 *
 * @todo Make this function more robust currently only supports numbers upto 
 * 0x3F00.
 */
uint8_t *asn1_write_long(asn1_ctx_t *asn1_ctx, uint8_t *out, long val);

int16_t asn1_oidcmp(uint8_t *oid1, uint8_t *oid2);

/**
 * Calculates the length of an oid string in bytes.
 * @param oid
 *
 * @return
 *
 * Length of an oid string (in bytes).
 */
int16_t asn1_calc_oid_length(uint8_t *oid);

/**
 * Converts PEM encoding to the binary DER form.
 * @param in
 * @param out
 * @param out_len
 * @param type_str
 *
 * @todo Add debug messages.
 */
void pem_decode(uint8_t *in, size_t in_len, uint8_t *out, size_t *out_len,
                uint8_t *type_str);

#endif /* __BB_CRYPTO_ASN1_H */
