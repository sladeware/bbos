#!/usr/bin/env python

from bb.tools.cg.generators.c import Statement, Token, Node

class Include(Statement):
    def __init__(self, path):
        Statement.__init__(self)
        if not isinstance(path, Token):
            path = Token(path)
        self.add_element(path)

    def get_path(self):
        return self.get_element_by_index(0)

    def __repr__(self):
        return "#include <%s>\n" % self.get_path()

class ParameterList(Node):
    def __init__(self, parameters):
        Node.__init__(self)
        for parameter in parameters:
            if not isinstance(parameter, Token):
                parameter = Token(parameter)
            self.add_element(parameter)

    def __repr__(self):
        strings = []
        for element in self.get_elements():
            strings.append(element.__repr__())
        return "(%s)" % ", ".join(strings)

class Define(Statement):
    def __init__(self, name, parameter_list, tokens):
        Statement.__init__(self)
        if not isinstance(name, Token):
            name = Token(name)
        if parameter_list:
            if not isinstance(parameter_list, ParameterList):
                parameter_list = ParameterList(parameter_list)
        self.add_elements([name, parameter_list, tokens])

    def get_name(self):
        return self.get_element_by_index(0)

    def get_parameter_list(self):
        return self.get_element_by_index(1)

    def get_tokens(self):
        return self.get_element_by_index(2)

    def __repr__(self):
        if self.get_parameter_list():
            return "#define %s%s %s\n" % (self.get_name(),
                                          self.get_parameter_list(),
                                          self.get_tokens())
        else:
            return "#define %s %s\n" % (self.get_name(), self.get_tokens())
