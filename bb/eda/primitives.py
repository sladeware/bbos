#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

#_______________________________________________________________________________

class Primitive(object):
    """This class is basic for any electrical primitive."""

    def __init__(self):
        self.__owner = None

    @property
    def owner(self):
        return self.__owner
        
    @owner.setter
    def owner(self, primitive):
        self.__owner = primitive

#_______________________________________________________________________________

class Distributable(object):
    class Metadata(object):
        """This class keeps metadata information."""
        def __init__(self):
            self.__author = None
            self.__name = None
            self.__version = "0.0.0"
            self.__description = None
            self.__reference_format = "Part"
            self.__keywords = list()

        @property
        def keywords(self):
            """A list of additional keywords to be used to assist
            searching for the package in a larger catalog. This makes
            the part findable."""
            return self.__keywords

        @property
        def name(self):
            return self.__name

        @name.setter
        def name(self, name):
            self.__name = name

        @property
        def reference_format(self):
            """See Part.reference"""
            return self.__reference_format

        @reference_format.setter
        def reference_format(self, frmt):
            self.__reference_format = frmt

        @property
        def description(self):
            """A longer description of the part that can run to
            several paragraphs."""
            return self.__description

        @description.setter
        def description(self, text):
            self.__description = text

        @property
        def version(self):
            return self.__version

        @version.setter
        def version(self, version):
            self.__version = version

        @property
        def author(self):
            """A string containing the author's name at a minimum; additional
            contact information may be provided."""
            return self.__author

        @author.setter
        def author(self, name):
            self.__author = name

    def __init__(self):
        # Store the meta-data (name, version, author, and so
        # forth) in a separate object -- we're getting to have enough
        # information here that it's worth it.
        self.__metadata = self.Metadata()

    @property
    def metadata(self):
        return self.__metadata

class Configurable(object):
    """Interface."""

    class Config:
        def __str__(self):
            return str(self.__dict__)

    def __init__(self):
        self.__config = Configurable.Config()

    def add_parameter(self, name, value=None):
        setattr(self.__config, name, value)

    def get_parameter(self, name):
        return getattr(self.__config, name)

    @property
    def config(self):
        return self.__config

class Symbol(Primitive, Configurable):
    """An electronic symbol is a pictogram used to represent various
    electrical and electronic devices (such as wires, batteries,
    resistors, and transistors) in a schematic diagram of an
    electrical or electronic circuit. """

    def __init__(self):
        """By default designator is None."""
        Primitive.__init__(self)
        Configurable.__init__(self)
        self.__designator_format = "P%d"
        self.__designator = None

    @property
    def designator_format(self):
        """Defines the format string to be used with the part
        designator. A reference designator unambiguously identifies a
        component in an electrical schematic (circuit diagram) or on a
        printed circuit board (PCB). The reference designator usually
        consists of one or two letters followed by a number, e.g. R13,
        C1002."""
        return self.__designator_format

    @designator_format.setter
    def designator_format(self, frmt):
        self.__designator_format = frmt

    @property
    def designator(self):
        """Designator is the name of a part on a printed circuit by
        convention beginning with one or two letters followed by a
        numeric value. The letter designates the class of component;
        eg. "Q" is commonly used as a prefix for transistors."""
        return self.__designator

    @designator.setter
    def designator(self, text):
        """By default if name is not selected it equals to
        designator."""
        self.__designator = text
        if not self.metadata.name:
            self.metadata.name = text




