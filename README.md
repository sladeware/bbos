Copyright (c) 2011-2012 Sladeware LLC

Bionic Bunny <http://bionicbunny.org>

## CONTENTS

 * WHAT IS BIONIC BUNNY?
 * INSTALLING ON LINUX AND OTHER PLATFORMS

## WHAT IS BIONIC BUNNY?

Bionic Bunny (BB) is a platform for embedded systems development, providing
microkernel operating system-like functionality. It provides
language-independent, hardware-independent and network-transparent communication
for power efficient computing in heterogeneous microcontroller robotics
applications.

## INSTALLING ON LINUX AND OTHER PLATFORMS

First, of all, you need to install prerequisites, BB requires Python 2.5
or higher:

       $ sudo apt-get install make git python python-networkx

Next, download the latest version of BB platform (see <http://bionicbunny.org>)
to the place where it will live (e.g. /opt/bionicbunny/):

       $ git clone git@github.com:sladeware/bbos.git bionicbunny

Go to this directory and initiate configuration process:

       $ cd /opt/bionicbunny/
       $ ./configure

Once configuration was successfully done, run installation as root:

       $ sudo make install
