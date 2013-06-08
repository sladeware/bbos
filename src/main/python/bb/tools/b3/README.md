<!--- -*- coding: utf-8; mode: markdown; -*- -->

Bionic Bunny Build (B3)
=======================

Bionic Bunny Build or **B3** is a build tool initially created for BB
applications. At a high level, B3 reads build descriptions stored in build
scripts or `BUILD`, constructs a directed acyclic graph (DAG) called image of
targets, and executes a specified set of goals against those targets.

B3 is part of BB framework and so depends on `bb` package. However it doesn't
depend on BB application.

Compilers and Loaders
---------------------

B3 intends to use a big variaty of compilers and loaders in order to support
wide range of existed microcontrollers and boards.

All the supported compilers are located in `bb.tools.compilers` package and can
be managed by `bb.tools.compiler_manager` manager. Each compiler is derived from
`Compiler` class.

All the loaders are located in `bb.tools.loaders` package and can be managed by
`bb.tools.loader_manager`.
