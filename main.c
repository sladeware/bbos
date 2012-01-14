#include <stdio.h>

void main() {

  _dira(1 << 16, 1 << 16);
  _outa(1 << 16, 1 << 16);
  _dira(1 << 17, 1 << 17);
  _outa(1 << 17, 1 << 17);
  _dira(1 << 18, 1 << 18);
  _outa(1 << 18, 1 << 18);
  _dira(1 << 19, 1 << 19);
  _outa(1 << 19, 1 << 10);
  _dira(1 << 20, 1 << 20);
  _outa(1 << 20, 1 << 20);

  //delay_ms(1000);
  //printf("Hello!\n");
  //delay_ms(1000);

  while(1) {
  }; // loop forever
}

