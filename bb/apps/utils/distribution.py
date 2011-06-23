#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

class DistributionMetadata:
    """Class to hold the distribution meta-data such as name, version,
    author, etc."""

    def __init__(self, name=None, version=None):
        self.__name = name 
        self.__version = version

    def get_name(self):
        return self.__name or "UNKNOWN"

    def get_version(self):
        return self.__version or "0.0.0"

        
