<!--- -*- coding: utf-8; mode: markdown; -*- --->

Bionic Bunny Operating System

Copyright (c) 2011-2013 Sladeware LLC

http://www.bionicbunny.org/

[![Build status](https://api.travis-ci.org/sladeware/bbos.png?branch=master)](https://travis-ci.org/sladeware/bbos)

What is Bionic Bunny?
---------------------

Bionic Bunny (BB) is a platform for embedded systems development, providing
microkernel operating system-like functionality. It provides
language-independent, hardware-independent and network-transparent communication
for power efficient computing in heterogeneous microcontroller robotics
applications.

Installation
------------

1. Download the latest version of the BB platform (see
   <http://www.bionicbunny.org>) to the place where it will live
   (e.g. `/opt/bbos/`):

        $ git clone git@github.com:sladeware/bbos.git

2. To install bbos, make sure you have [Python](http://www.python.org/) 2.7 or
   greater installed. If you're in doubt, run:

        $ python -V

3. Run the tests:

        $ python setup.py test

   If some tests fail, this library may not work correctly on your system.
   Continue at your own risk.

4. Run this command from the command prompt to initiate setup process:

        $ python setup.py install

   All the modules will be installed automatically if required. The installation
   process will generate default config file `~/.bbconfig`. In case you would
   like to refresh it and does not want to reinstall the package, run:

        $ python -m bb.config

   Run the following command to uninstall the framework:

        $ python setup.py uninstall

Install using virtualenv
------------------------

Sometimes it's required to manually install bbos using
[virtualenv](http://www.virtualenv.org/). Create an environment
(e.g. `bbos-env`) and switch to bbos home directory:

    $ virtualenv bbos-env
    $ cd bbos/

The following example shows how to run tests:

    $ ../bbos-env/bin/python setup.py test

Continue installation process from step 3 from section INSTALL by using created
environment.