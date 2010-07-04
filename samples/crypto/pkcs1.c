
#use "PKCS1.LIB"

main() {
	RSA_key *key;
	char *encoded_key;
   size_t encoded_key_len;

   encoded_key_len = 97;
   encoded_key = (char *)xalloc(encoded_key_len);
   strcpy(encoded_key, \
   	"-----BEGIN RSA PUBLIC KEY-----\n"       \
      "MBgCEQCPPpOh0mf5j23OYkttvYbXAgMBAAE=\n" \
      "-----END RSA PUBLIC KEY-----\n"         \
   );

	if ((key=rsa_public_key_pem_decode(encoded_key, encoded_key_len)) != NULL) {
   	printf("Public key was successfully readed.");
   } else {
   	printf("Public was not loaded.");
   }
}

