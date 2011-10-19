#!/usr/bin/env python

import os.path
import xml.sax.handler

from driver.generator import DriverGenerator, DriverContentHandler

class Argument(object):
  def __init__(self, name=None, type=None):
    self.__name = name
    self.__type = type

  def get_name(self):
    return self.__name

  def get_type(self):
    return self.__type

class Method(object):
  def __init__(self, name=None, return_type="void"):
    self.name = name
    self.return_type = return_type
    self.arguments = []

  def get_name(self):
    return self.name

  def get_return_type(self):
    return self.return_type

  def has_argument(self, argument):
    for existed_argument in self.arguments:
      if existed_argument.get_name() == argument.get_name():
        return True
    return False

  def add_argument(self, argument):
    if self.has_argument(argument):
      pass
    self.arguments.append(argument)

  def get_arguments(self):
    return self.arguments

  def get_num_arguments(self): # get_arity?
    return len(self.get_arguments())

class CDriverContentHandler(DriverContentHandler):
  tags=("argument", )

  def __init__(self, *args, **kargs):
    DriverContentHandler.__init__(self, tags=CDriverContentHandler.tags)

  def _open_method(self, attrs):
    print "Method '%s'" % attrs.get("name", None)
    method = Method(name=attrs.get("name", None),
                    return_type=attrs.get("return_type", "void"))
    self.driver.get_interface().add_method(method)
    self.last_method = method

  def _open_argument(self, attrs):
      argument = Argument(name=attrs.get("name", None),
                          type=attrs.get("type", None))
      self.last_method.add_argument(argument)

class CDriverGenerator(DriverGenerator):
  def __init__(self, driver):
    DriverGenerator.__init__(self)
    self.driver = driver
    self.__lang = "c"

  def gen_interface(self):
    """Generate driver interface files: source file and header file."""
    self._gen_interface_hdr_file()
    self._gen_interface_src_file()
    self._gen_hal_hdr_file()
    self._gen_hal_src_file()

  def _gen_hal_hdr_file(self):
    fname = "%s_hal.h" % self.driver.get_name()
    print "Generate", fname
    fh = open(fname, 'w')
    # Generate runner prototype
    fh.write("void %s_%s();\n" % (self.driver.get_name(), "messenger"))
    fh.close()
    
  def _gen_hal_src_file(self):
    pass

  def _gen_interface_src_file(self):
    """Do not generate source file if such already exists. User may already
    write driver specific code to the source file and we do not want to lose it.
    """
    fname = "%s_interface.c" % self.driver.get_name()
    self._interface_src_fname = fname
    # TODO Add special flag to be able to rewrite source file by force.
    if os.path.exists(fname):
      return
    print "Generate", fname
    fh = open(fname, 'w')
    fh.write('#include "%s"\n' % self._interface_hdr_fname)
    # Generate command functions
    for command in self.driver.get_interface().get_methods():
      fh.write("\n%s\n" % command.get_return_type())
      fh.write("%s_%s(" % (self.driver.get_name(), command.get_name()))
      if command.get_num_arguments():
        for i in range(command.get_num_arguments()):
          argument = command.get_arguments()[i]
          fh.write("%s %s" % (argument.get_type(), argument.get_name()))
          if (i + 1) != command.get_num_arguments():
            fh.write(", ")
      fh.write(")\n")
      fh.write("{\n\n}\n")
    fh.close()

  def _gen_interface_hdr_file(self):
    """Generate interface header file."""
    fname = "%s_interface.h" % self.driver.get_name()
    self._interface_hdr_fname = fname
    print "Generate", fname
    fh = open(fname, 'w')
    # Header comment
    fh.write("/*\n")
    fh.write(" * Please do not edit this by hand, as your changes will be lost.\n")
    fh.write(" */\n")
    h = "__%s_H" % self.driver.get_name().upper()
    fh.write("#ifndef %s\n" % h)
    fh.write("#define %s\n" % h)
    """# Thread identifier
    if self.driver.get_thread_id():
      fh.write("/* Check thread identifier */\n")
      fh.write("#ifndef %s\n" % self.driver.get_thread_id())
      fh.write("#error %s was not defined!\n" % self.driver.get_thread_id())
      fh.write("#endif /* %s */\n" % self.driver.get_thread_id())
    # Port identifier
    if self.driver.get_port_id():
      fh.write("/* Check port identifier */\n")
      fh.write("#ifndef %s\n" % self.driver.get_port_id())
      fh.write("#error %s was not defined!\n" % self.driver.get_port_id())
      fh.write("#endif /* %s */\n" % self.driver.get_port_id())"""
    # Generate command prototypes
    fh.write("/* Command prototypes */\n")
    for command in self.driver.get_interface().get_methods():
      fh.write("PROTOTYPE(")
      fh.write("%s %s_%s, (" % (command.get_return_type(), self.driver.get_name(), 
                                command.get_name()))
      if command.get_num_arguments():
        for i in range(command.get_num_arguments()):
          argument = command.get_arguments()[i]
          fh.write("%s %s" % (argument.get_type(), argument.get_name()))
          if (i + 1) != command.get_num_arguments():
            fh.write(", ")
      fh.write("));\n")
    # Finalize
    fh.writelines("#endif /* %s */\n" % h)
    fh.close()

