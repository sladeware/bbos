#!/usr/bin/env python

"""Fritzing is an open source software initiative[2] to support designers and
artists ready to move from physical prototyping to actual product. It was
developed at the University of Applied Sciences of Potsdam."""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import re
import os
import os.path
import sys
import xml.dom
import xml.dom.minidom
import zipfile
import types

from bb.hardware import Sketch
from bb.hardware.components import Component, Pin
from bb.utils.type_check import verify_list, verify_string

#_______________________________________________________________________________

# User defined fritzing home directory that can be set with help of
# set_fritzing_home_dir() function.
_fritzing_home_dir = None

def get_fritzing_home_dir():
    """Return path to the directory with fritzing distribution."""
    global _fritzing_home_dir
    return _fritzing_home_dir

def set_fritzing_home_dir(path):
    global _fritzing_home_dir
    if not os.path.exists(path):
        raise IOError("Directory '%s' does not exist" % path)
    _fritzing_home_dir = path

# User defined fritzing user directory that can be set with help of
# set_fritzing_user_dir() function.
_fritzing_user_dir = None

def set_fritzing_user_dir(path):
    global _fritzing_user_dir
    if not os.path.exists(path):
        raise IOError("Directory '%s' does not exist" % path)
    _fritzing_user_dir = path

def get_default_fritzing_user_dir():
    """Return default path to the global fritzing user directory
    depending on operating system name."""
    default_dirs = {
        "posix": "%s/.config/Fritzing" % os.environ["HOME"],
        }
    return default_dirs.get(os.name, None)

def get_fritzing_user_dir():
    """Return path to the global user directory. The location of this
    directory differs depending on operating system, and might
    even be hidden by default (see get_default_fritzing_user_dir())."""
    global _fritzing_user_dir
    return _fritzing_user_dir or get_default_fritzing_user_dir()

_fritzing_search_pathes = list()

def get_fritzing_search_pathes():
    """Return list of strings that specifies the search path for
    fritzing files."""
    global _fritzing_search_pathes
    fritzing_search_pathes = [get_fritzing_home_dir(), get_fritzing_user_dir()]
    return fritzing_search_pathes

#_______________________________________________________________________________

def get_text(nodes):
    rc = []
    for node in nodes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

#_______________________________________________________________________________

class Handler(object):
    def __init__(self, obj=None):
        self._fname = None
        self._buf = None
        self._root = None
        self._object = obj

    def get_object(self):
        return self._object

#_______________________________________________________________________________

class SketchHandler(Handler):
    ROOT_TAG_NAME = "module"
    TITLE_TAG_NAME = "title"
    INSTANCE_TAG_NAME = "instance"
    SCHEMATIC_VIEW_TAG_NAME = "schematicView"

    FILE_EXT = "fz"

    def __init__(self, fname=None):
        Handler.__init__(self)
        self._object = Sketch()
        self._part_handlers_table = dict()
        if fname:
            self.open(fname)

    def open(self, fname):
        self._fname = fname
        self._buf = None
        if not os.path.exists(fname):
            raise IOError("No such file: '%s'" % fname)
        if fname.endswith(self.FILE_EXT):
            fh = open(fname, "r")
            self._buf = fh.read()
        self.read()

    def find_part_handler_by_id(self, id_):
        return self._part_handlers_table.get(id_, None)

    def add_part_handler(self, part_handler):
        """Add Part handled by PartHandler to Sketch handled by
        SketchHandler."""
        part = part_handler.get_object()
        self._part_handlers_table[part.id] = part_handler
        self.get_object().add_part(part)

    def read(self):
        self._root = None
        # Read root element:
        #
        #   <module fritzingVersion="..." moduleId="...">
        #     ...
        #   </module>
        self._root = xml.dom.minidom.parseString(self._buf).documentElement
        if self._root.tagName != self.ROOT_TAG_NAME:
            raise Exception()
        instances = self._root.getElementsByTagName("instance")
        if instances.length <= 0:
            raise Exception("Sketch file '%s' has no instances" % fname)
        # First of all we need to read all the instances but do not process
        # them. Otherwise we want be able to connect them.
        for instance in instances:
            self.__read_instance(instance)
        for inctance in instances:
            self.__process_instance(instance)

    def __process_instance(self, instance):
        handler = self.find_part_handler_by_id(instance.getAttribute("modelIndex"))
        part = handler.get_object()
        views_elements = instance.getElementsByTagName("views")
        if not views_elements:
            raise Exception("It has no view!")
        # We are looking for schematic view (see SCHEMATIC_VIEW_TAG_NAME)
        views_element = views_elements.item(0)
        schematic_view_elements = views_element.getElementsByTagName(self.SCHEMATIC_VIEW_TAG_NAME)
        if not schematic_view_elements:
            # Some parts does not have schematic view
            return
        schematic_view_element = schematic_view_elements.item(0)
        # Start looking for connectors
        connectors_elements = schematic_view_element.getElementsByTagName("connectors")
        if not connectors_elements:
            # No connectors
            return
        connectors_element = connectors_elements.item(0)
        for connector_element in connectors_element.getElementsByTagName("connector"):
            number = connector_element.getAttribute("connectorId")
            src_connector = part.find_connector(number)
            connects_elements = connector_element.getElementsByTagName("connects")
            if not connects_elements:
                continue
            connects_element = connects_elements.item(0)
            for connection_element in connects_element.getElementsByTagName("connect"):
                dst_part_id = connection_element.getAttribute("modelIndex")
                dst_handler = self.find_part_handler_by_id(dst_part_id)
                dst_part = dst_handler.get_object()
                dst_connector = dst_part.find_connector( \
                    connection_element.getAttribute("connectorId"))
                src_connector.connect_to(dst_connector)
                exit(0)
        exit(0)

    def __read_instance(self, instance):
        """Read instance entry:

          <instance>
            ...
          </instance>

        And return PartHandler instance."""
        # The path attribute has the following view: :path
        # Do we need to take only the last path?
        part_fname = instance.getAttribute('path').split(":").pop()
        if not os.path.exists(part_fname):
            # In some way this path is absolute, we need to make it as local for
            # FRITZING_HOME directory
            if part_fname.startswith(os.sep):
                part_fname = part_fname[1:]
            part_fname = os.path.abspath(os.path.join(get_fritzing_search_pathes()[0], part_fname))
        if not os.path.exists(part_fname):
            raise IOError("No such part: '%s'" % part_fname)
        part_handler = PartHandler(fname=part_fname)
        part = part_handler.get_object()
        if not instance.hasAttribute("modelIndex"):
            raise Exception()
        part.id = instance.getAttribute("modelIndex")
        # Part reference
        elements = instance.getElementsByTagName("title")
        if elements:
            part.reference = get_text(elements[0].childNodes)
        self.add_part_handler(part_handler)
        return part_handler

class PinHandler(Handler):
    """Parse connectors:
    <connector id="..." name="..." type="...">
      ...
    </connector>"""
    METADATA = ("description",)

    def __init__(self):
        self._object = Pin()

    def read(self, connector_element):
        id_ = connector_element.getAttribute("id")
        if id_:
            self._object.metadata.number = id_
        name = connector_element.getAttribute("name")
        if name:
            self._object.metadata.name = name
        type_ = connector_element.getAttribute("type")
        if type_:
            self._object.metadata.type = type_
        # Read metadata properties for this connector if such were defined
        for property_ in get_properties(self._object.metadata):
            elements = connector_element.getElementsByTagName(property_)
            if not elements:
                continue
            text = get_text(elements[0].childNodes)
            setattr(self._object.metadata, property_, text)

class ComponentHandler(Handler):
    """A Fritzing part is made up of a number of files, one required
    metadata file (file suffix is .fzp, so the metadata file is also
    referred to as an FZP), and up to four SVG files.

    The metadata file lists a part's title, description, and other
    properties, as well as a references to the part's SVG files. It
    also specifies a part's connectors and internal buses. Each
    connector's graphic is an element found in the relevant view SVG
    file. Since any SVG element can have an id attribute, the metadata
    file refers to a connector's graphic element using that element's
    id.

    Learn more about fritzing part format:
      http://fritzing.org/developer/fritzing-part-format/"""

    ROOT_TAG_NAME = "module"
    CONNECTORS_TAG_NAME = "connectors"
    CONNECTOR_TAG_NAME = "connector"

    # Metadata file extension referred as an FZP
    FILE_EXT = "fzp"
    # Extension for a zipped metadata file
    ZFILE_EXT = "fzpz"

    METADATA_COMPATIBILITY = {
        "title": "name",
        "reference_format": None,
        "label": "reference_format"
        }

    def __init__(self, fname=None, part=None):
        Handler.__init__(self)
        self._object = part or Part()
        self._metadata_map = dict()
        # Copy all metadata properties from Part class
        for property_ in get_properties(self._object.metadata):
            self._metadata_map[property_] = property_
        # Provide metadata compatibility
        for property_, value in self.METADATA_COMPATIBILITY.items():
            if not value:
                del self._metadata_map[property_]
            elif value:
                self._metadata_map[property_] = value
        if fname:
            self.open(fname)

    def open(self, fname):
        """Open fritzing part file, which can be zipped .fzpz file or
        just .fzp file."""
        self._fname = fname
        self._doc = None
        self._buf = None
        self._root = None
        if not os.path.exists(fname):
            raise IOError("No such file: '%s'" % fname)
        # Whether our file is zip-file
        if fname.endswith(self.ZFILE_EXT):
            fh = None
            try:
                fh = zipfile.ZipFile(fname)
            except:
                raise IOError("'" + fname + "' is not a zip file")
            for i, name in enumerate(fh.namelist()):
                if name.endswith(self.FILE_EXT):
                    self._buf = fh.read(name)
                    break
            if not self._buf:
                raise Exception("No '%s' file found in '%s'" %
                                (self.FILE_EXT, fname))
        elif fname.endswith(self.FILE_EXT):
            fh = open(fname, "r")
            self._buf = fh.read()
        self.read()

    def read(self):
        if not self._buf:
            raise Exception("The buffer is empty. Nothing to read.")
        self._doc = xml.dom.minidom.parseString(self._buf)
        # Read root element:
        #
        #   <module fritzingVersion="..." moduleId="...">
        #     ...
        #   </module>
        self._root = self._doc.documentElement
        if self._root.tagName != self.ROOT_TAG_NAME:
            raise Exception("'%s' has no '%s' root element" % \
                                (fname, self.ROOT_TAG_NAME))
        if not self._root.hasChildNodes():
            raise Exception("Root tag has no child nodes.")
        # Put attributes such as author, description, date, label, etc. as
        # properties of the metadata instance for this part
        for (src_name, dst_name) in self._metadata_map.items():
            elements = self._root.getElementsByTagName(src_name)
            if not elements:
                continue
            if hasattr(self._object.metadata, dst_name):
                text = get_text(elements[0].childNodes)
                setattr(self._object.metadata, dst_name, text)
        self.__read_properties()
        self.__read_tags()
        self.__read_connectors()

    def __read_tags(self):
        """Read tags: <tags><tag> ... </tag> ... </tags>. The
        tags are translated as keywords."""
        tags_elements = self._root.getElementsByTagName("tags")
        if not tags_elements:
            return
        tags_element = tags_elements.item(0)
        for tag_element in tags_element.getElementsByTagName("tag"):
            self._object.metadata.keywords.append(get_text(tag_element.childNodes))

    def __read_connectors(self):
        """Read connectors: <connectors>...</connectors>."""
        connectors_elements = self._root.getElementsByTagName(self.CONNECTORS_TAG_NAME)
        if not connectors_elements:
            # Some parts does not have connectors (e.g. note)
            return
        connectors_element = connectors_elements.item(0)
        for connector_element in connectors_element.getElementsByTagName(self.CONNECTOR_TAG_NAME):
            connector_handler = PinHandler()
            connector_handler.read(connector_element)
            self._object.add_connector(connector_handler.get_object())

    def __read_properties(self):
        """Read part's properties:

        <properties>
          <property name="...">...</property>
        </properties>"""
        properties = self._root.getElementsByTagName("properties").item(0)
        for property_ in properties.getElementsByTagName("property"):
            name = property_.getAttribute("name")
            text = get_text(property_.childNodes)
            self._object.properties.__dict__[name] = get_text(property_.childNodes)

#_______________________________________________________________________________
# To __init__.py

def find_pkg_files(pkg, root=None, skip_names=[], recursive=True):
    verify_list(skip_names)
    verify_string(pkg)
    if not root:
        pkgs = pkg.split(".")
        pkg_half_path = os.path.sep.join(pkgs)
        root = None
        for path in sys.path:
            path = os.path.join(path, pkg_half_path)
            if os.path.exists(path):
                root = path
                break
    files = list()
    for name in os.listdir(root):
        if name in skip_names:
            continue
        path = os.path.join(root, name)
        if os.path.isdir(path) and recursive:
            if name.startswith("."): # improve this
                continue
            files.extend(find_pkg_files(".".join([pkg, name]), path, skip_names))
        if os.path.isfile(path) and path.endswith(".py"):
            files.append(".".join([pkg, name])) #(os.path.abspath(path))
    return files

def index_parts():
    skip_names = ["__init__.py"]
    for module_name in find_pkg_files("bb.hardware.parts", None, skip_names):
        module = __import__(module_name, globals())
        names = getattr(module, "__parts__", None)
        if not names:
            continue
        #for name in names:
        #    part_class = getattr(module, name, None)

#index_parts()

#_______________________________________________________________________________


if __name__ == '__main__':
    set_fritzing_home_dir("/opt/fritzing")

    ch = ComponentHandler("/opt/fritzing/parts/core/controller_propeller_D40.fzp")
    print ch.get_object().metadata.keywords
    #print ph.get_object().get_num_connectors()
    #print part.find_connector("CH5_pin6").get_property("description")

    #h = SketchHandler("/home/d2rk/Desktop/bbos/branches/robot2011/common_board_base_do_not_edit.fz")
    #print h.get_object().get_parts()
