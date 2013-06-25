***********
Application
***********

An application is defined by a :class:`~bb.app.app.Application` and is comprised
of a set of processes running on a particular system topology to perform work
meeting the application's requirements.

It combines all of the build systems of all of the defined processes, where each
process correnspond to the appropriate :class:`~bb.app.mapping.Mapping` instance
from `mappings`. Therefore the application includes the models of processes,
their communication, hardware description, simulation and build
specifications. At the same time the processes inside of an application can be
segmented into clusters, or a group of CPUs.

An :class:`~bb.app.app.Application` instance is connected to specific directory
called `home directory` that keeps actual application data. Such directory can
be created either with help of **b3** or manually with help of
:func:`~bb.app.app.Application.init_home_dir`.

.. toctree::
   :maxdepth: 1

   app
   mapping
   os/index
   hardware/index
