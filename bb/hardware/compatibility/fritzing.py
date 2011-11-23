#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import os
import os.path
import xml.dom
import xml.dom.minidom
import zipfile

from bb.hardware import Part, Connector

#_______________________________________________________________________________

FRITZING_HOME = "/opt/fritzing"
FRITZING_PART_FILE_EXT = "fzp"
FRITZING_PART_ZFILE_EXT = "fzpz"
FRITZING_SKETCH_FILE_EXT = "fz"

PART_ATTRIBUTES = ("version", "author", "title", "label", "date", "description")
CONNECTOR_ATTRIBUTES = ("description",)

def get_text(nodes):
    rc = []
    for node in nodes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

#_______________________________________________________________________________

def merge_parts(fz_part, part):
    """Merge two parts: fritzing part and bb part. Returns updated bb part."""
    return part

def read_sketch(fz_fname):
    if not os.path.exists(fz_fname):
        raise IOError("No such file: '%s'" % fz_fname)
    fz_string = None
    if fz_fname.endswith(FRITZING_SKETCH_FILE_EXT):
        fh = open(fz_fname, "r")
        fz_string = fh.read()
    fz_dom = xml.dom.minidom.parseString(fz_string)
    # Read root element:
    #   <module fritzingVersion="..." moduleId="...">
    #   </module>
    root = fz_dom.documentElement
    if not root.tagName == "module":
        raise Exception()
    instances = root.getElementsByTagName("instance")
    assert instances.length > 0, "'" + fz_fname + "' has no instances"
    for instance in instances:
        # The path attribute has the following view: :path
        # Do we need to take only the last path?
        part_fname = instance.getAttribute('path').split(":").pop()
        # In some way this path is absolute, we need to make it as local for
        # FRITZING_HOME directory
        if part_fname.startswith(os.sep):
            part_fname = part_fname[1:]
        part_fname = os.path.abspath(os.path.join(FRITZING_HOME, part_fname))
        if not os.path.exists(part_fname):
            raise IOError("No such part: '%s'" % part_fname)
        
        exit(0)

def read_part(part, fz_fname, update_parameters=True, update_connectors=True):
    """Read fritzing part file. It can be zipped .fzpz file or just .fzp file.

    For example:
      part = Part()
      read_part(part, 'MCP3208.fzpz')"""
    if not os.path.exists(fz_fname):
        raise IOError("No such file: '%s'" % fz_fname)
    fz_string = None
    # Whether our file is zip-file
    if fz_fname.endswith(FRITZING_PART_ZFILE_EXT):
        fh = None
        try:
            fh = zipfile.ZipFile(fz_fname)
        except:
            assert False, "'" + fz_fname + "' is not a zip file"
        for i, name in enumerate(fh.namelist()):
            if name.endswith(FRITZING_PART_FILE_EXT):
                fz_string = fh.read(name)
                break
    elif fname.endswith(FRITZING_PART_FILE_EXT):
        fh = open(fname, "r")
        raise NotImplementedError()
    assert fz_string, "no '" + FRITZING_PART_FILE_EXT + "' file found in '" \
        + fz_fname + "'"
    fzdom = xml.dom.minidom.parseString(fz_string)
    # Read root element:
    #   <module fritzingVersion="..." moduleId="...">
    #   </module>
    root = fzdom.documentElement
    assert root.tagName == "module", "'" + fz_fname + "' has no 'module' root"
    # Put attributes such as author, description, date, label, etc. as
    # properties of the part
    for part_attribute in PART_ATTRIBUTES:
        elements = root.getElementsByTagName(part_attribute)
        if not elements:
            continue
        part.set_property(part_attribute, get_text(elements[0].childNodes))
    if update_parameters:
        __read_properties(root, part)
    if update_connectors(root, part):
        __read_connections(root, part)

def __read_connections(root, part):
    """Read connectors:

      <connectors>
        <connector id="..." name="..." type="...">
        </connector>
      </connectors>"""
    connectors = root.getElementsByTagName("connectors").item(0)
    for connector in connectors.getElementsByTagName("connector"):
        c = Connector(connector.getAttribute("name"), connector.getAttribute("type"))
        # Read properties for this connector if such were defined
        for connector_attribute in CONNECTOR_ATTRIBUTES:
            elements = connector.getElementsByTagName(connector_attribute)
            if not elements:
                continue
            c.set_property(connector_attribute, get_text(elements[0].childNodes))
            part.add_connector(c)

def __read_properties(root, part):
    """Read part properties:

      <properties>
        <property name="...">...</property>
      </properties>"""
    properties = root.getElementsByTagName("properties").item(0)
    for property_ in properties.getElementsByTagName("property"):
        part.set_property(property_.getAttribute("name"), \
                              get_text(property_.childNodes))

#_______________________________________________________________________________

if __name__ == '__main__':
    #part = Part()
    #read_part(part, '/home/d2rk/Desktop/bbos/branches/robot2011/parts/MCP3208.fzpz')
    #print part.get_properties()
    #print part.find_connector("CH5_pin6").get_property("description")

    read_sketch("/home/d2rk/Desktop/bbos/branches/robot2011/common_board_base_do_not_edit.fz")
