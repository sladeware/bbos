/*
 * lib/crypto/utils/asn1.c
 *
 * ASN.1 Support
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 *
 */

/*** BeginHeader	asn1_init, asn1_length, asn1_create_seq, asn1_create_seq_tag,
									asn1_append_int_tag, asn1_append_int, asn1_append_oid,
									asn1_append_timetick, asn1_append_string, asn1_read_string,
									asn1_read_length, asn1_read_tag, asn1_read_int, asn1_read_oid,
									asn1_oidcmp, asn1_calc_oid_length, asn1_write_long,
									pem_decode */

#include <bbos/lib/crypto/utils/asn1.h>

/*** EndHeader */

const uint8_t _pem_header[] = "-----BEGIN ";
const uint8_t _pem_footer[] = "-----END ";
const uint8_t _pem_dashes[] = "-----";

/**
 * Reads data structure: tag and length.
 */
uint8_t *
asn1_read_struct(uint8_t *pos, int16_t *tag, int32_t *len)
{
	pos = asn1_read_tag(pos, tag);
	pos = asn1_read_length(pos, len);

	return pos;
}


/**
 * Converts PEM encoding to the binary DER form.
 * @in:
 * @out:
 * @out_len:
 * @type_str:
 *
 * Return value:
 *
 * N/A
 *
 * TODO:
 * 
 * Add debug messages.
 */
void
pem_decode(uint8_t *in, size_t in_len, uint8_t *out, size_t *out_len, 
uint8_t *type_str)
{
	auto uint8_t *begin, *end, *b64;
	size_t b64_len;

	/* Initialization */
	b64_len = 0;
	*out_len = 0;

	begin = strstr(in, _pem_header);
	begin += strlen(_pem_header);
	if (!strncmp(begin, type_str, strlen(type_str)))
		begin += strlen(type_str);
	else
		return;

	if (!strncmp(begin, _pem_dashes, strlen(_pem_dashes)))
		begin += strlen(_pem_dashes);
	else
	return;

	while (isspace(*begin))
		begin++;

	end = strstr(begin, _pem_footer);

	/*
	 * WARNING: In the current realisation on the following step the
	 * base64 encoded block will be saved in output stream.
	 *
	 * XXX: do we need to allocate memory for this?
	 */
	b64 = out;
	while (begin != end) {
		if (isalnum(*begin) || *begin=='+' || *begin=='=' || *begin=='/')
			*b64++ = *begin++;
		else
			begin++;
	}

	/* length of the base64 encoded string */
	b64_len = b64-out;

	*out_len = base64_decode(out, b64-b64_len);
}

/**
 * Initializes an asn1_ctx_t.
 * @asn1_ctx: A pointer to asn1_ctx_t structure.
 * @buf: A pointer to the buffer used to store the ASN.1 sequence.
 * @buf_len: Length of the buffer pointer to by pBuffer.
 *
 * Return value:
 *
 * N/A
 */
void
asn1_init(asn1_ctx_t *asn1_ctx,	uint8_t *buf, int16_t buf_len)
{
	asn1_ctx->buf = buf;
	asn1_ctx->buf_len = buf_len;
	asn1_ctx->end = asn1_ctx->buf;
	*asn1_ctx->buf = ASN1_TAG_UNKNOWN;
}

/**
 * Gets the current length of the ASN.1 sequence.
 * @asn1_ctx: A pointer to asn1_ctx_t structure.
 *
 * Return value:
 *
 * Length of the ASN.1 sequence.
 */
int16_t
asn1_length(asn1_ctx_t *asn1_ctx)
{
	return (int16_t)(asn1_ctx->end - asn1_ctx->buf);
}

/**
 * Creates a ASN.1 sequence. asn1_create_seq_type is passed ASN1_TAG_SEQUENCE.
 * as the type.
 * @asn1_ctx:
 * @start:
 * @end:
 *
 * Return value:
 *
 * Pointer to the end of the sequence.
 *
 * See also:
 * asn1_create_seq_type
 */
uint8_t *
asn1_create_seq(asn1_ctx_t *asn1_ctx, uint8_t *start, uint8_t *end)
{
	return asn1_create_seq_tag(asn1_ctx, start, end, ASN1_TAG_SEQUENCE);
}

/**
 * Creates a ASN.1 sequence of tag entry_tag. Shifts the bytes
 * pointed to by start and end and prepend them with the type
 * and length.
 * @asn1_ctx: A pointer to asn1_ctx_t structure.
 * @start: Pointer to the start of the sequence. Specify NULL to start at 
 * the beginning of the buffer.
 * @end: Pointer to the end of the sequence. Specify NULL to end at the end of the buffer.
 * @entry_tag: Type to assign to the new sequence.
 *
 * Return value:
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

uint8_t *
asn1_create_seq_tag(asn1_ctx_t *asn1_ctx, uint8_t *start, uint8_t *end,
uint8_t entry_tag)
{
	auto int16_t len;
	auto uint8_t *in, *out;
	auto float f;

	if(start == NULL) start = asn1_ctx->buf;
	if(end == NULL) end = asn1_ctx->end;

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

/**
 * Appends an integer to the end of a ASN.1 sequence of type tag.
 * @asn1_ctx: A pointer to asn1_ctx_t structure.
 * @val: Integer value to append.
 * @len: Length in bytes of the integer to store. For example if you were to
 * put val=200 you may only want to store it as 1 byte.
 * @tag: One of the ASN.1 types to prepend to the integer.
 *
 * Return value:
 *
 * Pointer to the end of the integer.
 */
uint8_t *
asn1_append_int_tag(asn1_ctx_t *asn1_ctx, uint32_t val, uint8_t len,\
uint8_t tag)
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
		// todo: handle integers with length greater than 4
		break;
	}

	return asn1_ctx->end;
}

/**
 * Appends an integer to the end of an ASN.1 sequence of type ASN1_TAG_INTEGER.
 *
 * Return value:
 *
 * Pointer to the end of the integer.
 *
 * Also see:
 * asn1_append_int_tag
 */
uint8_t *
asn1_append_int(asn1_ctx_t *asn1_ctx, uint32_t val, uint8_t len)
{
	return asn1_append_int_tag(asn1_ctx, val, len, ASN1_TAG_INTEGER);
}

/**
 * Appends timeticks to the end of an ASN.1 sequence.
 * @asn1_ctx: A pointer to asn1_ctx_t structure.
 * @val: Time tick value to append.
 *
 * Return value:
 *
 * Pointer to the end of the integer.
 *
 * See also:
 * asn1_append_int_tag
 */
uint8_t *
asn1_append_timetick(asn1_ctx_t *asn1_ctx, int32_t val)
{
	return asn1_append_int_tag(asn1_ctx, val, 4, ASN1_TAG_TIME_TICKS);
}

/**
 * Appends a string to the end of an ASN.1 sequence. Return a
 * pointer to the end of the ASN.1 sequence.
 * @asn1_ctx: A pointer to asn1_ctx_t structure.
 * @str: string to append to the ASN.1 sequence.
 */
uint8_t *
asn1_append_string(asn1_ctx_t *asn1_ctx, uint8_t *str)
{
	auto int16_t str_len;

	str_len = strlen(str);

	// write type
	*(asn1_ctx->end) = ASN1_TAG_OCTETSTRING;
	asn1_ctx->end++;

	// write length
	asn1_ctx->end = asn1_write_long(asn1_ctx, asn1_ctx->end, str_len);

	// write data
	strncpy(asn1_ctx->end, str, str_len);
	asn1_ctx->end += str_len;

	return asn1_ctx->end;
}

/**
 * Appends an OID to the end of an ASN.1 sequence. Return a pointer
 * to the end of the ASN.1 sequence.
 * @asn1_ctx: A pointer to asn1_ctx_t structure.
 * @oid: A string representation of an OID. (ex 1.2.3.4.5)
 */
uint8_t *
asn1_append_oid(asn1_ctx_t *asn1_ctx, uint8_t *oid)
{
	auto int16_t len;
	auto int16_t c;
	auto int8_t tmp[10];
	auto int8_t *tmp_out;
	auto int32_t num;
	auto int8_t *p;

	// write type
	*(asn1_ctx->end) = ASN1_TAG_OID;
	asn1_ctx->end++;

	// write length
	len = asn1_calc_oid_length(oid);
	if(len == -1) {
		//log( LOG_ERROR, "Invalid OID: %s", szOID );
		return NULL;
	}
	asn1_ctx->end = asn1_write_long(asn1_ctx, asn1_ctx->end, len);

	// write oid
	tmp_out = tmp;
	c = 0;
	p = oid;
	for(;;) {
		if((*p == '.') || (*p == '\0')) {
			*tmp_out = '\0';
			num = atol(tmp);
			if(c == 0) {
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
		}
		else {
			*tmp_out++ = *p;
		}
		p++;
	}

	return asn1_ctx->end;
}

/**
 * Reads the ASN.1 tag from an ASN.1 sequence.
 * @pos: Pointer to the position in the ASN.1 sequence.
 * @tag: Pointer to an integer to recieve the type.
 *
 * Return value:
 *
 * Position in the ASN.1 sequence after the type.
 */
uint8_t *
asn1_read_tag(uint8_t *pos, int16_t *tag)
{
	*tag = *pos;
	return pos + 1;
}

/**
 * Reads the ASN.1 length from an ASN.1 sequence.
 * @pos: Pointer to the position in the ASN.1 sequence.
 * @len: Pointer to an integer to recieve the length.
 *
 * Return value:
 *
 * Position in the ASN.1 sequence after the length.
 */
uint8_t *
asn1_read_length(uint8_t *pos, int32_t *len)
{
	auto int16_t len_len;

	if(*pos == 0x80) { // Indefinite form
		/** @todo support the ASN.1 indefinite form */
		#ifdef ASN1_DEBUG
			printf( "ASN.1 Indefinite form not supported\n" );
		#endif
	}
	else if(*pos & 0x80) { // definite long form
		len_len = (*pos) & 0x7F;
		pos++;
		*len = 0;
		while(len_len > 0) {
			*len = (*len) << 8;
			*len |= (int32_t)(*pos);
			pos++;
			len_len--;
		}
	}
	else {
		*len = (int32_t)(*pos);
		pos++;
	}

	return pos;
}

/**
 * Reads the ASN.1 string from an ASN.1 sequence.
 * @pos: Pointer to the position in the ASN.1 sequence.
 * @len: Length of the string.
 * @str: Pointer to a buffer to hold the string.
 *
 * Return value:
 *
 * Position in the ASN.1 sequence after the string.
 */
uint8_t *
asn1_read_string(uint8_t *pos, int32_t len, uint8_t *str)
{
	while(len > 0)	{
		*str = *pos;
		str++;
		pos++;
		len--;
	}
	*str = '\0';

	return pos;
}

/**
 * Reads the ASN.1 int from an ASN.1 sequence.
 * @pos: Pointer to the position in the ASN.1 sequence.
 * @len: Length of the integer.
 * @val: Pointer to a long to hold the integer.
 *
 * Return value:
 *
 * Position in the ASN.1 sequence after the integer.
 */
uint8_t *
asn1_read_int(uint8_t* pos, int32_t len, int32_t *val)
{
	auto int32_t tmp;

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

/**
 * Reads the ASN.1 oid from an ASN.1 sequence. 
 * @pos: Pointer to the position in the ASN.1 sequence.
 * @len: Length of the oid.
 * @oid: Pointer to a buffer to hold the oid.
 *
 * Return value:
 *
 * Position in the ASN.1 sequence after the oid.
 */
uint8_t *
asn1_read_oid(uint8_t* pos, int32_t len, uint8_t *oid)
{
	auto uint8_t *end;
	auto uint32_t tmp;

	end = pos + (int16_t)len;
	oid += sprintf(oid, "%d.%d", (*pos)/40, (*pos)%40);
	pos++;
	while(pos < end) {
		*oid++ = '.';
		tmp = 0;
		while(*pos & 0x80) {
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
 * @oid1: OID to compare.
 * @oid2: OID to compare.
 *
 * Return value:
 *
 * <0: oid1 is less than oid2
 *  0: oid1 equals oid2
 * >0: oid1 is greater that oid2
 */
int16_t
asn1_oidcmp(int8_t *oid1, int8_t *oid2)
{
	auto uint8_t *p1, *p1_last;
	auto uint8_t *p2, *p2_last;
	auto uint8_t tmp1[10];
	auto uint8_t tmp2[10];

	p1 = p1_last = oid1;
	p2 = p2_last = oid2;
	while((*p1!='\0') && (*p2!='\0')) {
		if(*p1 != *p2) break;
		if(*p1 == '.') {
			p1_last = p1 + 1;
			p2_last = p2 + 1;
		}
		p1++;
		p2++;
	}
	if((*p1 == '\0') && (*p2 == '\0'))
   	return 0;
	if(*p1 == '\0')
   	return -1;
	if(*p2 == '\0')
   	return 1;

	p1 = strchr(p1, '.');
	if(p1 == NULL)
   	p1 = p1_last + strlen(p1_last);
	strncpy(tmp1, p1_last, p1-p1_last);
	tmp1[p1-p1_last] = '\0';

	p2 = strchr(p2, '.');
	if( p2 == NULL )
   	p2 = p2_last + strlen(p2_last);
	strncpy(tmp2, p2_last, p2-p2_last);
	tmp2[p2-p2_last] = '\0';

	if(atoi(tmp1) < atoi(tmp2))
   	return -1;

	return 1;
}

/**
 * Calculates the length of an oid string in bytes.
 */
int16_t
asn1_calc_oid_length(uint8_t *oid)
{
	auto uint8_t *p;
	auto int16_t len;
	auto uint8_t tmp[10];
	auto uint8_t *tmp_out;
	auto int32_t num;

	len = 1;
	p = strchr(oid, '.');
	if(p == NULL)
   	return -1;
	p = strchr(p+1, '.');
	if(p == NULL)
   	return -1;
	p++;

	tmp_out = tmp;
	for (;;) {
		if((*p == '.') || (*p == '\0')) {
			*tmp_out = '\0';
			num = atol(tmp);
			if(num > 0x7F)
				len += 2;
			else
				len += 1;
			tmp_out = tmp;
			if(*p == '\0')
         	break;
		}
		else {
			*tmp_out = *p;
			tmp_out++;
		}
		p++;
	}

	return len;
}

/**
 * Writes a long value to the ASN.1 sequence.
 *
 * TODO:
 *
 * Make this function more robust currently only supports numbers upto 0x3F00.
 */
uint8_t *
asn1_write_long(asn1_ctx_t *asn1_ctx, uint8_t *out, int32_t val)
{
	if(val > 0x7F)	{
		*out++ = 0x80 | ((uint8_t)((val >> 7) & 0x7F));
		val = val & 0x7F;
	}

	*out++ = (uint8_t)val;

	return (uint8_t *)out;
}


