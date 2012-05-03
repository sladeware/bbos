#!/usr/bin/env python

"""Application manager aims to allow user to manage more than one application at
once. This feature provides apportunity to use one application from another."""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.app.application import Application

_application_table = list()
_active_application = None

def new_application(*args, **kargs):
    """Create and return the new :class:`bb.app.application.Application`
    instance. The new application will be the automatically marked as active."""
    application = Application(*args, **kargs)
    # NOTE: Do not register application here, it did this automatically
    # once an instance was created. The reason, the application can be
    # created simply by using Application class.
    set_active_application(application)
    return application

def start_application(application):
    application.start()

def stop_application(application):
    application.stop()

def register_application(application):
    _application_table.append(application)

def is_registered_application(application):
    return application in _application_table

def unregister_application(application):
    pass

def set_active_application(application):
    if not is_registered_application(application):
        return False
    _active_application = application
    return True

def get_active_application():
    return _active_application

def get_running_application():
    """Return currently running :class:`bb.app.application.Application`
    insance."""
    return Application.get_running_instance()
