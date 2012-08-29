Copyright (c) 2011-2012 Sladeware LLC

Bionic Bunny <http://bionicbunny.org>

## Contents

 * What is Bionic Bunny?
 * Installing on Linux

## What is Bionic Bunny?

Bionic Bunny (BB) is a platform for embedded systems development, providing
microkernel operating system-like functionality. It provides
language-independent, hardware-independent and network-transparent communication
for power efficient computing in heterogeneous microcontroller robotics
applications.

## Installing on Linux

First, of all, you need to install prerequisites. BB requires Python 2.5 or
higher and a few other basic tools:

    $ sudo apt-get install make git python python-networkx automake autoconf

Next, download the latest version of BB platform (see <http://bionicbunny.org>)
to the place where it will live (e.g. `/opt/bbos/`):

    $ git clone git@github.com:sladeware/bbos.git bbos

Go to this directory and initiate configuration process:

    $ cd /opt/bbos/
    $ ./configure

Once configuration was successfully done, run installation as root:

    $ sudo make install

## Development

To run testing, go to the root BB directory and run:

    $ python test.py
