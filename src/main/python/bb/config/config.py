# -*- coding: utf-8; -*-
#
# Copyright (c) 2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko

import django.conf

import bb.config.compilers.python.builtins
import bb.config.compilers.python.importer # override standard __import__

# We would like to use Django templates without the rest of Django.
django.conf.settings.configure()
