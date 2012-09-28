#!/usr/bin/env python

from bb.os.drivers.onewire.slaves import DS18B20Driver

with DS18B20Driver as bundle:
  bundle.build_cases.update({
    'propeller': {
      'sources': ('ds18b20.c', '../onewire_bus.c')
    }
  })
