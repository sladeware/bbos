#!/usr/bin/env python

import sys
from xml.sax.handler import ContentHandler
import driver.generator

class DriverGenerator(driver.generator.DriverGenerator):
    def __init__(self, drv):
        driver.generator.DriverGenerator.__init__(self)
        self.driver = drv
        self.__lang = "python"

    def gen(self):
        print "Generating..."
        self._gen_driver()
        self._gen_driver_activity()

    def _gen_driver(self):
        fh = open("./serial/test.py", "w")
        fh.write("class %s(Driver):\n" % self.driver.get_name())
        for method in self.driver.get_methods():
            fh.write("\tdef %s(self" % method.get_name())
            for argument in method.get_arguments():
                fh.write(", %s" % argument.get_name())
            fh.write("):\n")
            fh.write("\t\tpass\n\n")
        fh.close()
        
    def _gen_driver_activity(self):
        fh = open("./serial/test.py", "a")
        fh.write("class %s(DriverActivity):\n" % self.driver.get_activity().get_name())
        fh.write("\tcommands=dict(\n")
        for command in self.driver.get_activity().get_commands():
            fh.write('\t\t"%s": "%s",\n' % (command.get_name(), command.get_action()))
        fh.write("\t)\n")
        for command in self.driver.get_activity().get_commands():
            fh.write("\tdef %s():\n" % command.get_action())
            fh.write("\t\tpass\n\n")
        fh.close()

class Argument(object):
  def __init__(self, name=None):
    self.__name = name

  def get_name(self):
    return self.__name

class Method(object):
  def __init__(self, name=None):
    self.name = name
    self.arguments = []

  def get_name(self):
    return self.name

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

  def get_num_arguments(self):
    return len(self.get_arguments())

class Driver(object):
  def __init__(self, name=None):
      self.__name = name
      self.__methods = []

  def get_name(self):
      return self.__name

  def set_activity(self, activity):
    self.__activity = activity

  def get_activity(self):
    return self.__activity

  def add_method(self, method):
    self.__methods.append(method)

  def get_methods(self):
    return self.__methods

class DriverActivity(object):
    def __init__(self, name=None, thread_id=None, port_id=None):
        self.__name = name
        self.__thread_id = thread_id
        self.__port_id = port_id
        self.commands = []

    def get_name(self):
        return self.__name

    def has_command(self, command):
        for existed_command in self.commands:
            if existed_command.get_name() == command.get_name():
                return True
        return False

    def add_command(self, command):
        """Add a command. If the command is already exist it will be replaced by
        a new one and correspond warning will be printed."""
        if self.has_command(command):
            print "WARNING: Command '%s' was already added. Now it will be replaced" \
                % command.get_name()
            self.remove_command(self, command)
        self.commands.append(command)

    def remove_command(self, command):
        pass

    def get_commands(self):
        return self.commands

class Command(object):
    def __init__(self, name, action=None):
        self.__name = name
        self.__action = action
        
    def get_name(self):
        return self.__name

    def get_action(self):
        return self.__action

class DriverContentHandler(ContentHandler):
    tags=("driver", "activity", "method", "methods", "commands", "command", "argument")

    def __init__(self, tags=(), *args, **kargs):
        ContentHandler.__init__(self)
        self.__tags = DriverContentHandler.tags + tags
        self.driver = None

    def validateTag(self, tag):
        if not tag in self.__tags:
            raise Exception("Unknown tag '%s'\n" % tag)

    def startElement(self, tag, attrs):
        self.validateTag(tag)
        method_name = "_open_%s" % tag
        try:
            method = getattr(self, method_name)
        except AttributeError, e:
            print "WARNING: method '%s' that handles '%s' tag was not provided" \
                % (method_name, tag)
            return
        method(attrs)

    def _open_driver(self, attrs):
        name = attrs.get("name", None)
        print "Reading driver '%s'" % name
        self.driver = Driver(name=attrs.get("name", None))

    def _open_command(self, attrs):
        name = attrs.get("name", None)
        action = attrs.get("action", None)
        print "Add command '%s' => '%s'" % (name, action)
        cmd = Command(name, action)
        self.driver.get_activity().add_command(cmd)

    def _open_method(self, attrs):
        print "Add method '%s'" % attrs.get("name", None)
        method = Method(name=attrs.get("name", None))
        self.driver.add_method(method)
        self.last_method = method

    def _open_argument(self, attrs):
        argument = Argument(name=attrs.get("name", None))
        self.last_method.add_argument(argument)

    def _open_activity(self, attrs):
        sys.stdout.write("Processing activity ")
        name = attrs.get("name", None)
        sys.stdout.write("'%s'\n" % name)
        sys.stdout.write("Thread ID... ")
        tid = attrs.get("thread_id", None)
        if not tid:
            raise Exception("Attribute '%s' for '%s' activity was not provided" \
                              % ("thread_id", name))
        sys.stdout.write("'%s'\n" % tid)
        sys.stdout.write("Port ID... ")
        pid = attrs.get("port_id", None)
        if not tid:
            raise Exception("Attribute '%s' for '%s' activity was not provided" \
                              % ("port_id", name))
        sys.stdout.write("'%s'\n" % tid)
        activity = DriverActivity(name=name, thread_id=tid, port_id=pid)
        self.driver.set_activity(activity)
