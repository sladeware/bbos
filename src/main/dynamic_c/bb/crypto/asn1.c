/*
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 */

#include "asn1.h"

const uint8_t _pem_header[] = "-----BEGIN ";
const uint8_t _pem_footer[] = "-----END ";
const uint8_t _pem_dashes[] = "-----";

void
pem_decode(uint8_t *in, size_t in_len, uint8_t *out, size_t *out_len, 
           uint8_t *type_str)
{
  uint8_t *begin, *end, *b64;
  size_t b64_len;
  b64_len = 0;
  *out_len = 0;
  begin = strstr(in, _pem_header);
  begin += strlen(_pem_header);
  if (!strncmp(begin, type_str, strlen(type_str))) {
    begin += strlen(type_str);
  } else {
    return;
  }
  if (!strncmp(begin, _pem_dashes, strlen(_pem_dashes))) {
    begin += strlen(_pem_dashes);
  } else {
    return;
  }
  while (isspace(*begin)) {
    begin++;
  }
  end = strstr(begin, _pem_footer);
  /*
   * WARNING: In the current realisation on the following step the
   * base64 encoded block will be saved in output stream.
   *
   * XXX: do we need to allocate memory for this?
   */
  b64 = out;
  while (begin != end) {
    if (isalnum(*begin) || *begin=='+' || *begin=='=' || *begin=='/') {
      *b64++ = *begin++;
    } else {
      begin++;
    }
  }
  /* length of the base64 encoded string */
  b64_len = b64 - out;
  *out_len = base64_decode(out, b64-b64_len);
}

void
asn1_init(asn1_ctx_t *asn1_ctx, uint16_t *buf, int16_t buf_len)
{
  asn1_ctx->buf = buf;
  asn1_ctx->buf_len = buf_len;
  asn1_ctx->end = asn1_ctx->buf;
  *asn1_ctx->buf = ASN1_TAG_UNKNOWN;
}

uint8_t *
asn1_read_struct(uint8_t *pos, int16_t *tag, int32_t *len)
{
  pos = asn1_read_tag(pos, tag);
  pos = asn1_read_length(pos, len);
  return pos;
}

int16_t
asn1_length(asn1_ctx_t *asn1_ctx)
{
  return (int16_t)(asn1_ctx->end - asn1_ctx->buf);
}

uint8_t *
asn1_create_seq(asn1_ctx_t *asn1_ctx, uint8_t *start, uint8_t *end)
{
  return asn1_create_seq_tag(asn1_ctx, start, end, ASN1_TAG_SEQUENCE);
}

uint8_t *
asn1_create_seq_tag(asn1_ctx_t *asn1_ctx, uint8_t *start, uint8_t *end,
                    uint8_t entry_tag)
{
  int16_t len;
  uint8_t *in, *out;
  float f;
  if (start == NULL) {
    start = asn1_ctx->buf;
  }
  if (end == NULL) {
    end = asn1_ctx->end;
  }
  len = 1; // type
  f = (float)(end - start + 1);
  f = log10(f) / log10(2.0);
  f = ceil(f) / 7.0;
  len += (int)ceil(f - 0.0001); // size
  in = asn1_ctx->end;
  out = in + len;
  if(out > asn1_ctx->buf+asn1_ctx->buf_len)	{
    //log( LOG_ERROR, "asn1_create_seq_type: Buffer overflow" );
    return NULL;
  }
  while(in >= start) {
    *out = *in;
    out--;
    in--;
  }
  in++;
  // write type
  *in = entry_tag;
  in++;
  // write length
  asn1_write_long(asn1_ctx, in, end-start);
  asn1_ctx->end += len;
  return end;
}

uint8_t *
asn1_append_int_tag(asn1_ctx_t *asn1_ctx, uint32_t val, uint8_t len, uint8_t tag)
{
  // write type
  *(asn1_ctx->end) = tag;
  asn1_ctx->end++;
  // write length
  asn1_ctx->end = asn1_write_long(asn1_ctx, asn1_ctx->end, len);
  // write data
  switch (len) {
  case 1:
    *asn1_ctx->end = (uint8_t)((val >> 0) & 0xFF);
    asn1_ctx->end++;
    break;
  case 2:
    *asn1_ctx->end = (uint8_t)((val >> 8) & 0xFF);
    asn1_ctx->end++;
    *asn1_ctx->end = (uint8_t)((val >> 0) & 0xFF);
    asn1_ctx->end++;
    break;
  case 3:
    *asn1_ctx->end = (uint8_t)((val >> 16) & 0xFF);  *asn1_ctx->end++;
    *asn1_ctx->end = (uint8_t)((val >> 8) & 0xFF);   *asn1_ctx->end++;
    *asn1_ctx->end = (uint8_t)((val >> 0) & 0xFF);   *asn1_ctx->end++;
    break;
  case 4:
    *asn1_ctx->end = (uint8_t)((val >> 24) & 0xFF);  *asn1_ctx->end++;
    *asn1_ctx->end = (uint8_t)((val >> 16) & 0xFF);  *asn1_ctx->end++;
    *asn1_ctx->end = (uint8_t)((val >> 8) & 0xFF);   *asn1_ctx->end++;
    *asn1_ctx->end = (uint8_t)((val >> 0) & 0xFF);   *asn1_ctx->end++;
    break;
  default:
    /* TODO: handle integers with length greater than 4 */
    break;
  }
  return asn1_ctx->end;
}

uint8_t *
asn1_append_int(asn1_ctx_t *asn1_ctx, uint32_t val, uint8_t len)
{
  return asn1_append_int_tag(asn1_ctx, val, len, ASN1_TAG_INTEGER);
}

uint8_t *
asn1_append_timetick(asn1_ctx_t *asn1_ctx, int32_t val)
{
  return asn1_append_int_tag(asn1_ctx, val, 4, ASN1_TAG_TIME_TICKS);
}

uint8_t *
asn1_append_string(asn1_ctx_t *asn1_ctx, uint8_t *str)
{
  int16_t str_len;
  str_len = strlen(str);
  /* write type */
  *(asn1_ctx->end) = ASN1_TAG_OCTETSTRING;
  asn1_ctx->end++;
  /* write length */
  asn1_ctx->end = asn1_write_long(asn1_ctx, asn1_ctx->end, str_len);
  /* write data */
  strncpy(asn1_ctx->end, str, str_len);
  asn1_ctx->end += str_len;
  return asn1_ctx->end;
}

uint8_t *
asn1_append_oid(asn1_ctx_t *asn1_ctx, uint8_t *oid)
{
  int16_t len;
  int16_t c;
  int8_t tmp[10];
  int8_t *tmp_out;
  int32_t num;
  int8_t *p;
  // write type
  *(asn1_ctx->end) = ASN1_TAG_OID;
  asn1_ctx->end++;
  // write length
  len = asn1_calc_oid_length(oid);
  if (len == -1) {
    //log( LOG_ERROR, "Invalid OID: %s", szOID );
    return NULL;
  }
  asn1_ctx->end = asn1_write_long(asn1_ctx, asn1_ctx->end, len);
  // write oid
  tmp_out = tmp;
  c = 0;
  p = oid;
  for (;;) {
    if ((*p == '.') || (*p == '\0')) {
      *tmp_out = '\0';
      num = atol(tmp);
      if (c == 0) {
        *(asn1_ctx->end) = (uint8_t)(num * 40);
      }
      else if (c == 1) {
        *(asn1_ctx->end) += (uint8_t)(num);
        asn1_ctx->end++;
      }
      else {
        asn1_ctx->end = asn1_write_long(asn1_ctx, asn1_ctx->end, num);
      }
      c++;
      tmp_out = tmp;
      if (*p == '\0')
        break;
    } else {
      *tmp_out++ = *p;
    }
    p++;
  }
  return asn1_ctx->end;
}

uint8_t *
asn1_read_tag(uint8_t *pos, int16_t *tag)
{
  *tag = *pos;
  return pos + 1;
}

uint8_t *
asn1_read_length(uint8_t *pos, int32_t *len)
{
  int16_t len_len;
  if (*pos == 0x80) { // Indefinite form
    /** @todo support the ASN.1 indefinite form */
#ifdef ASN1_DEBUG
    printf( "ASN.1 Indefinite form not supported\n" );
#endif
  } else if (*pos & 0x80) { // definite long form
    len_len = (*pos) & 0x7F;
    pos++;
    *len = 0;
    while (len_len > 0) {
      *len = (*len) << 8;
      *len |= (int32_t)(*pos);
      pos++;
      len_len--;
    }
  } else {
    *len = (int32_t)(*pos);
    pos++;
  }
  return pos;
}

uint8_t *
asn1_read_string(uint8_t *pos, int32_t len, uint8_t *str)
{
  while(len > 0) {
    *str = *pos;
    str++;
    pos++;
    len--;
  }
  *str = '\0';
  return pos;
}

uint8_t *
asn1_read_int(uint8_t* pos, int32_t len, int32_t *val)
{
  int32_t tmp;

  switch ((int32_t)len) {
  case 1:
    *val = *pos++;
    break;
  case 2:
    *val = (int32_t)*pos++<< 8L | (int32_t)*pos++;
    break;
  case 3:
    *val = (int32_t)*pos++<<16L | (int32_t)*pos++<< 8L | (int32_t)*pos++;
    break;
  case 4:
    *val = (int32_t)*pos++<<24L | (int32_t)*pos++<<16L | (int32_t)*pos << 8L | (int32_t)*pos++;
    break;
  default:
    *val = 0;
    pos += (int16_t)len;
#ifdef ASN1_DEBUG
    printf( "ASN.1 integers greater than 32-bit not supported\n" );
#endif
    break;
  }
  return pos;
}

uint8_t *
asn1_read_oid(uint8_t* pos, int32_t len, uint8_t *oid)
{
  uint8_t *end;
  uint32_t tmp;
  end = pos + (int16_t)len;
  oid += sprintf(oid, "%d.%d", (*pos) / 40, (*pos) % 40);
  pos++;
  while (pos < end) {
    *oid++ = '.';
    tmp = 0;
    while (*pos & 0x80) {
      tmp |= *pos++ & 0x7F;
      tmp = tmp << 7;
    }
    tmp |= *pos++;
    oid += sprintf(oid, "%d", tmp);
  }
  return pos;
}

/**
 * Compares two OIDs.
 *
 * @param oid1 OID to compare.
 * @param oid2 OID to compare.
 *
 * @return
 *
 * <0 - oid1 is less than oid2
 *  0 - oid1 equals oid2
 * >0 - oid1 is greater that oid2
 */
int16_t
asn1_oidcmp(int8_t *oid1, int8_t *oid2)
{
  uint8_t *p1, *p1_last;
  uint8_t *p2, *p2_last;
  uint8_t tmp1[10];
  uint8_t tmp2[10];
  p1 = p1_last = oid1;
  p2 = p2_last = oid2;
  while ((*p1!='\0') && (*p2!='\0')) {
    if (*p1 != *p2)
      break;
    if (*p1 == '.') {
      p1_last = p1 + 1;
      p2_last = p2 + 1;
    }
    p1++;
    p2++;
  }
  if ((*p1 == '\0') && (*p2 == '\0'))
    return 0;
  if (*p1 == '\0')
    return -1;
  if (*p2 == '\0')
    return 1;
  p1 = strchr(p1, '.');
  if(p1 == NULL) {
    p1 = p1_last + strlen(p1_last);
  }
  strncpy(tmp1, p1_last, p1-p1_last);
  tmp1[p1-p1_last] = '\0';
  p2 = strchr(p2, '.');
  if(p2 == NULL) {
    p2 = p2_last + strlen(p2_last);
  }
  strncpy(tmp2, p2_last, p2-p2_last);
  tmp2[p2-p2_last] = '\0';
  if(atoi(tmp1) < atoi(tmp2)) {
    return -1;
  }
  return 1;
}

int16_t
asn1_calc_oid_length(uint8_t *oid)
{
  uint8_t *p;
  int16_t len;
  uint8_t tmp[10];
  uint8_t *tmp_out;
  int32_t num;
  len = 1;
  p = strchr(oid, '.');
  if (p == NULL)
    return -1;
  p = strchr(p+1, '.');
  if (p == NULL)
    return -1;
  p++;
  tmp_out = tmp;
  for (;;) {
    if ((*p == '.') || (*p == '\0')) {
      *tmp_out = '\0';
      num = atol(tmp);
      if(num > 0x7F)
        len += 2;
      else
        len += 1;
      tmp_out = tmp;
      if(*p == '\0')
        break;
    } else {
      *tmp_out = *p;
      tmp_out++;
    }
    p++;
  }
  return len;
}

uint8_t *
asn1_write_long(asn1_ctx_t *asn1_ctx, uint8_t *out, int32_t val)
{
  if (val > 0x7F) {
    *out++ = 0x80 | ((uint8_t)((val >> 7) & 0x7F));
    val = val & 0x7F;
  }
  *out++ = (uint8_t)val;
  return (uint8_t *)out;
}
