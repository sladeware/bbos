
#include <cogutil.h>
void
delay_ms(int ms)
{
  _waitcnt(_cnt() + ms * (_clockfreq() / 1000));
}
int main()
{
  char counter;
  int bitset;

  bitset = detect_free_cogs();
  counter = count_free_cogs();
  while (1)
  {
    printf("Number of free cogs: %d (bitset=%d)\n", counter, bitset);
    delay_ms(1000);
  }
  return 0;
}
