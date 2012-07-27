#ifndef __BITWISE_OP
#define __BITWISE_OP

#define is_odd(x) parity(x)

char parity(int x);

int ror(int x, int bits);
int rcr(int x, int bits, char c);
int muxc(int dest, int mask, char c);
#define muxnc(dest, mask, c) muxc(dest, mask, !c)

#endif /* __BITWISE_OP */
