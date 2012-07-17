#!/usr/bin/env python

from bb.build import builder

import model

builder.set_application(model.print_hello_world)
builder.build()
