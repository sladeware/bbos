#!/usr/bin/env python

import types

_PARENTS={}

TAB=(' ' * 2)

class Element(object):
    pass

class Node(Element):
    def __init__(self):
        self.__elements = []

    def add_element(self, element):
        self.__elements.append(element)
        _PARENTS[id(element)] = self

    def add_elements(self, elements):
        for element in elements:
            self.add_element(element)

    def get_elements(self):
        return self.__elements

    def get_element_by_index(self, index):
        return self.__elements[index]

class Token(Element):
    """Token is an Element that directly represents bytes of source code."""
    def __init__(self, content=''):
        self.__content = content

    def get_content(self):
        return self.__content

    def __repr__(self, intent=''):
        return self.get_content()

class Statement(Node):
    def __init__(self, *args):
        Node.__init__(self)
        if len(args):
            for arg in args:
                if not isinstance(arg, Element):
                    arg = Token(arg)
                self.add_element(arg)

    def __repr__(self, intent=''):
        text = ''
        for element in self.get_elements():
            text += element.__repr__(intent)
        return "%s%s" % (intent, text)

class SelectionStatement(Statement):
    def __init__(self):
        Statement.__init__(self)

class Switch(SelectionStatement):
    def __init__(self, expr, statement):
        SelectionStatement.__init__(self)
        self.add_element(Token("switch"))
        self.add_element(expr)
        self.add_element(statement)

    def __repr__(self, intent=''):
        new_indent = intent + TAB
        return "%s%s () %s" % (intent,
                               self.get_element_by_index(0).__repr__(),
                               self.get_element_by_index(2).__repr__(intent=new_indent))

class Break(Statement):
    def __init__(self):
        Statement.__init__(self)
        self.add_element("break")
        self.add_element(";")

    def __repr__(self, intent=''):
        return "%s%s%s\n" % (intent,
                             self.get_element_by_index(0),
                             self.get_element_by_index(1))

class LabeledStatement(Statement):
    def __init__(self):
        Statement.__init__(self)

    def get_label(self):
        return self.get_element_by_index(0)

    def __repr__(self, intent=''):
        return "%s : \n" % self.get_label()

class Case(LabeledStatement):
    def __init__(self, expr, statement):
        LabeledStatement.__init__(self)
        self.add_element(Token("case"))
        if not isinstance(expr, Element):
            expr = Token(expr)
        self.add_element(expr)
        self.add_element(statement)

    def __repr__(self, intent=''):
        new_intent = intent + TAB
        return "%s%s %s:\n%s" % (intent,
                                 self.get_element_by_index(0).__repr__(),
                                 self.get_element_by_index(1).__repr__(),
                                 self.get_element_by_index(2).__repr__(intent=new_intent))

class CompoundStatement(Node):
    def __init__(self):
        Node.__init__(self)

    def __repr__(self, intent=''):
        new_intent = intent + TAB
        text = []
        for element in self.get_elements():
            text.append(element.__repr__(intent=new_intent))
        return "\n%s{\n%s%s}\n" % (intent, ''.join(text), intent)

class File(Node):
    def __init__(self, name):
        Node.__init__(self)
        self.__name = name

    def __repr__(self, intent=''):
        text = ''
        for element in self.get_elements():
            text += element.__repr__()
        return "%s%s" % (intent, text)

File.add_function = File.add_element

class DeclarationSpecifier(Node):
    """Possible storage_class_specifier's are: static, const, etc."""
    def __init__(self, storage_class_specifier, type_specifier):
        Node.__init__(self)
        self.add_elements([storage_class_specifier, type_specifier])

    def get_storage_class_specifier(self):
        return self.get_element_by_index(0)

    def get_type_specifier(self):
        return self.get_element_by_index(1)

    def __repr__(self):
        if not self.get_storage_class_specifier():
            return "%s" % self.get_type_specifier()
        else:
            return "%s %s" % (self.get_storage_class_specifier(),
                              self.get_type_specifier())

class Parameter(Node):
    def __init__(self, type, name):
        Node.__init__(self)
        if not isinstance(type, DeclarationSpecifier):
            type = DeclarationSpecifier(None, type)
        if not isinstance(name, Token):
            name = Token(name)
        self.add_elements([type, name])

    def get_type(self):
        return self.get_element_by_index(0)

    def get_name(self):
        return self.get_element_by_index(1)

    def __repr__(self):
        return "%s %s" % (self.get_type(), self.get_name())

class ParameterList(Node):
    def __init__(self, parameters):
        Node.__init__(self)
        if not type(parameters) is types.ListType:
            raise Exception("'parameters' must be a list type")
        for parameter in parameters:
            if type(parameter) is types.TupleType:
                parameter = Parameter(parameter[0], parameter[1])
            if not isinstance(parameter, Parameter):
                raise Exception("'parameter' must be a Parameter instance")
            self.add_element(parameter)

    def __repr__(self):
        strings = []
        for element in self.get_elements():
             strings.append(element.__repr__())
        return "(%s)" % ', '.join(strings)

class Function(Statement):
    def __init__(self, return_type, name, parameter_list=[],
                 block=CompoundStatement()):
        Statement.__init__(self)
        # If return_type was not defined with help of DeclarationSpecifier class
        if not isinstance(return_type, DeclarationSpecifier):
            if type(return_type) is types.TupleType:
                return_type = DeclarationSpecifier(return_type[0],
                                                   return_type[1])
            else:
                return_type = DeclarationSpecifier(None, return_type)
        if not isinstance(name, Token):
            name = Token(name)
        # Define parameter list
        if not isinstance(parameter_list, ParameterList):
            parameter_list = ParameterList(parameter_list)
        if not isinstance(block, CompoundStatement):
            raise Exception("'block' must be CompoundStatement instance")
        self.add_elements([return_type, name, parameter_list, block])

    def get_return_type(self):
        return self.get_element_by_index(0)

    def get_name(self):
        return self.get_element_by_index(1)

    def get_parameter_list(self):
        return self.get_element_by_index(2)

    def get_block(self):
        return self.get_element_by_index(3)

    def __repr__(self, indent=''):
        text = "%s %s%s%s" % \
            (self.get_return_type(), self.get_name(), self.get_parameter_list(),
             self.get_block())
        return text
