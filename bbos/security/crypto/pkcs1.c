/* START LIBRARY DESCRIPTION ***************************************************
LIB/CRYPTO/BBOS_PKCS1.LIB

	Copyright (c) 2010 Sun Scoper Inc.

DESCRIPTION:

   An implementation of the PKCS#1 standard for RSA cryptologhy and public-key
	encryptio and signature constructions. Based on RFC 3447.

CONFIGURATION MACROS:

FUNCTION DICTIONARY:

END DESCRIPTION ***************************************************************/

/*** BeginHeader rsa_public_key_pem_decode, */
#ifndef __BBOS_CRYPTO_PKCS1_LIB
#define __BBOS_CRYPTO_PKCS1_LIB

#use "rsa.lib"
#use "bbos_asn1.lib"

const uint8_t rsa_public_key_str[] = "RSA PUBLIC KEY";

bbos_crypto_debug RSA_key* rsa_public_key_pem_decode(uint8_t* encoded_key, size_t encoded_key_len);

#endif __BBOS_CRYPTO_PKCS1_LIB
/*** EndHeader */

/*
int rsaes_pkcs1_v1_5_encrypt(struct RSA_key_t far *key, \
char far *in, size_t inlen, char far *out, size_t far *outlen) {
}


int rsaes_pkcs1_v1_5_decrypt(struct RSA_key_t far *key, \
char far *crypt, size_t cryptlen, char far *plain, size_t far *plainlen) {
}
*/


bbos_crypto_debug rsa_key * 
rsa_public_key_pem_decode(uint8_t *encoded_key, size_t encoded_key_len)
{
	uint8_t *der;
	size_t der_len;
	uint8_t struct_tag;
	int32_t struct_len, struct_buf;
	RSA_key *key;

	/*
	 * WARNING: in this realisation the DER data will be saved over the PEM data.
	 * XXX: do we need to allocate a special memory for this?
	 */
	der = encoded_key;

	/* decode PEM decoded key */
	pem_decode(encoded_key, encoded_key_len, der, &der_len, rsa_public_key_str);

	if (der_len == 0) {
		return NULL;       	// XXX: message?
	}

	key = (RSA_key*)xalloc(sizeof(*key));

	/* Sequence */
	der = asn1_read_struct(der, &struct_tag, &struct_len);
	if (struct_tag != ASN1_TAG_SEQUENCE)
		return NULL;

	/* Modulus */
	der = asn1_read_struct(der, &struct_tag, &struct_len);
	if (struct_tag != ASN1_TAG_INTEGER)
		return NULL;
	//der = asn1_read_int(der, struct_len, &struct_buf);
	key->public.n.length = (int16_t)struct_len - 1; // XXX: ???
	bin2mp(der, &key->public.n, (int16_t)struct_len);
	der += (int16_t)struct_len;

	/* Public exponent */
	der = asn1_read_struct(der, &struct_tag, &struct_len);
	if (struct_tag != ASN1_TAG_INTEGER)
		return NULL;
	//der = asn1_read_int(der, struct_len, &struct_buf);
	key->public.e.length = (int16_t)struct_len - 1; // XXX: ???
	bin2mp(der, &key->public.e, (int16_t)struct_len);
	der += (int16_t)struct_len;

	return key;
}


