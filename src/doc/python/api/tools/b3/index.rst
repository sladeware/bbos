******************
Bionic Bunny Build
******************

This package represents Bionic Bunny Build system. Bionic Bunny Build or **B3**
is a build tool initially created for BB applications. At a high level, B3 reads
build descriptions stored in build scripts or `BUILD`, constructs a directed
acyclic graph (DAG) called image of targets, and executes a specified set of
goals against those targets.

B3 is part of BB framework and so depends on `bb` package. However it doesn't
depend on BB application.

.. toctree::

   b3
   commands/index
   rules/index
