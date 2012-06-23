
*********************
Writing simple module
*********************

BBOS can be dynamically altered at run time through the use of BBOS kernel
modules (BBOSKMs). Dynamically alterable means that you can load new
functionality into the kernel, unload functionality from the kernel.

For our first module, we'll start with a module that uses the kernel message
facility, ``print``, to print ``"Hello, world!"``.

Here's the simplest module possible located in `helloworld.py`::

    from bb.os.kernel import Module

    class helloworld(Module):
        AUTHOR="BB Team <info@bionicbunny.org>"
        DESCRIPTION="Simplest helloworld module"

        def on_load(self):
            print "Hello, world!"

        def on_unload(self):
            print "Goodbye, world!"

Kernel module has to be described by the class derived from the
:class:`bb.os.kernel.Module` class and that has the same name as the file does.
Thus since our module file is called ``helloworld`` we have a class
:class:`helloworld` that will describe it. This technique should be very fimiliar
to Java programmers.

Within a kernel module class you have to overwrite at least two methods: a
"start" method called :func:`bb.os.kernel.Module.on_load` which is called when
the module is loaded into the kernel, and an "end" method called
:func:`bb.os.kernel.Module.on_unload` which is called just before it is
unloaded.


