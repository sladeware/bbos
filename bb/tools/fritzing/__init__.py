#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module provides compatibility with `Fritzing <http://fritzing.org>`_.
Fritzing is an
open source software initiative to support designers and artists ready
to move from physical prototyping to actual product. It was developed
at the University of Applied Sciences of Potsdam.

The Fritzing EDA is represented by :mod:`bb.tools.fritzing` package.

At the very first time, once you will try to interract with parts, Fritzing will
use :func:`bb.tools.fritzing.index_parts` to automatically index all parts
located on your machine at search pathes (see
:func:`bb.tools.fritzing.get_search_pathes()`). All the indexed parts will be
stored at index file. This file has
`JSON (JavaScript Object Notation) format <http://en.wikipedia.org/wiki/JSON>`_
and its name can be obtained by :func:`bb.tools.fritzing.get_index_filename`.
"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

#_______________________________________________________________________________

import copy
import re
import os
import os.path
import sys
import xml.dom
import xml.dom.minidom
import zipfile
import string
import types
import json

from bb.hardware.devices import Device, Pin, Wire
from bb.lib.crypto.md5 import md5sum
from bb.utils.type_check import verify_list, verify_string, is_string, \
    is_tuple, is_list

#_______________________________________________________________________________
# XML support primitives

def get_text(nodes):
    rc = []
    for node in nodes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

#_______________________________________________________________________________

_home_dir = None
_user_dir = None
_search_pathes = list()
_index_filename = "fritzing.index"

def get_home_dir():
    """Return path to the directory with Fritzing distribution."""
    global _home_dir
    return _home_dir

def set_home_dir(path):
    """Set fritzing home directory."""
    global _home_dir
    if not path or not os.path.exists(path):
        raise IOError("Directory '%s' does not exist" % path)
    _home_dir = path

def get_default_user_dir():
    """Return default path to the global Fritzing user directory depending on
    operating system (``os.name``).
    """
    default_dirs = {
        "posix": "%s/.config/Fritzing" % os.environ["HOME"],
    }
    return default_dirs.get(os.name, None)

def get_user_dir():
    """Return path to the global user directory. The location of this directory
    differs depending on operating system, and might even be hidden by default
    (see :func:`get_default_user_dir`)."""
    return _user_dir or get_default_user_dir()

def set_user_dir(path):
    """Set fritzing user directory."""
    if not path or not os.path.exists(path):
        raise IOError("Path '%s' does not exist" % path)
    _user_dir = path

def add_search_path(path):
    """Add a new path to Fritzing search pathes.
    """
    _search_pathes.append(path)

def add_search_pathes(pathes):
    """Add a list of pathes to Fritzing search pathes. See also
    :func:`add_search_path`.
    """
    for path in pathes:
        add_search_path(path)

def get_search_pathes():
    """Return a list of strings that specifies the search path for Fritzing
    files. By default includes user directory and home directory.
    """
    pathes = list()
    pathes.extend(_search_pathes)
    for path in (get_home_dir(), get_user_dir()):
        if path:
            pathes.append(path)
    return pathes

def find_part_files(pathes, recursive=False):
    """Search and return a list of Fritzing part files ``.fzp`` that can be
    found at given `pathes`. List subdirectories recursively if flag
    `recursive` is ``True``."""
    if not is_list(pathes):
        pathes = [pathes]
    files = list()
    for path in pathes:
        if os.path.isdir(path):
            for name in os.listdir(path):
                if name.startswith("."): # improve this
                    continue
                pathes.append(os.path.join(path, name))
        elif os.path.isfile(path) and (path.endswith(PartHandler.FILE_EXT) \
                                           or path.endswith(PartHandler.ZFILE_EXT)):
            files.append(os.path.abspath(path))
    return files

def set_index_filename(filename):
    """Set the name of the index file that will be used by Fritzing. If file
    does not exist it will be created."""
    _index_filename = filename

def get_index_filename():
    """Return the name of index file.
    """
    return _index_filename

_parts_index = dict()
_part_handlers_by_id = dict()
_part_filenames_by_id = dict()

def index_parts(search_pathes=None, force=False):
    """Index all Fritzing parts that can be found at `search_pathes`. By default
    if `search_pathes` were not defined then :func:`get_search_pathes` will be
    used.

    Once all the parts were indexed, they are stored at index file
    :func:`get_index_filename` in order to increase performance in
    future. However, each new time created index file is loading and the system
    is removing obsolete parts and add new parts if such will be found.

    In order to reindex parts set `force` as ``True``.
    """
    global _parts_index
    global _part_handlers_by_id
    global _part_filenames_by_id
    if len(_parts_index):
        return
    # Use environment search pathes if search_pathes list was not defined
    if not search_pathes:
        search_pathes = get_search_pathes()
        # Check default environment pathes such as user
        # specific directory and home directory. Print warning
        # message if they does not exist.
        # We also need to remove these directories from search
        # pathes. They has to be processed in a special way.
        magic_pathes = list()
        if not get_home_dir():
            raise Exception("WARNING: home directory can not be defined.", \
                "Please set it manually by using bb.tools.fritzing.set_home_dir().")
        else:
            search_pathes.remove(get_home_dir())
            magic_pathes.append(get_home_dir())
        if not get_user_dir():
            print "WARNING: user specific directory can not be defined.", \
                "Please set it manually by using bb.tools.fritzing.set_user_dir()"
        else:
            search_pathes.remove(get_user_dir())
            magic_pathes.append(get_home_dir())
        # Scan magic pathes and extend existed search pathes.
        for magic_path in magic_pathes:
            for parts_location in ("parts", "resources/parts"):
                for group in ("core", "user", "obsolete", "contrib"):
                    path = os.path.join(magic_path, parts_location, group)
                    if not os.path.exists(path):
                        continue
                    search_pathes.append(path)
    # Read old index file if such already exists
    if os.path.exists(get_index_filename()):
        index_fh = open(get_index_filename())
        _parts_index = json.loads(''.join(index_fh.readlines()))
        index_fh.close()
    all_part_files = list()
    # Scan all search pathes one by one and extract part files
    for search_path in search_pathes:
        sys.stdout.write("Scaning %s... " % search_path)
        new_part_files = find_part_files(search_path, recursive=True)
        print "%d" % len(new_part_files)
        all_part_files.extend(new_part_files)
    # Look up for broken files and remove them
    broken_files = set(_parts_index.keys()) - set(all_part_files)
    for filename in broken_files:
        del _parts_index[filename]
    # Start working...
    has_updates = False
    counter = 0
    total = len(all_part_files)
    for pfile in all_part_files:
        frmt = "%"+ str(len(str(total))) +"d/%d\r"
        sys.stdout.write("Indexing " + frmt % (counter, total))
        counter += 1
        # Make check sum for this file
        checksum = md5sum(pfile)
        if pfile in _parts_index:
            (old_checksum, old_module_id) = _parts_index[pfile]
            if old_checksum == checksum:
                _part_handlers_by_id[old_module_id] = None
                _part_filenames_by_id[old_module_id] = pfile
                continue
        ph = PartHandler(pfile)
        _parts_index[pfile] = (checksum, ph.module_id)
        _part_handlers_by_id[ph.module_id] = ph
        _part_filenames_by_id[ph.module_id] = pfile
        has_updates = True
    print # empty line
    # Rewrite index file only if it has some updates
    if has_updates:
        __write_index()
    # Update

def reindex_parts():
    """Perform complete reindexing. The :func:`get_index_filename` will be
    removed and the cache will be erased."""
    _parts_index = dict()
    index_parts(force=True)

def load_part_handler_by_id(id):
    """Try to load part by its id (see `moduleId` attribute) and
    return :class:`PartHandler` instance."""
    part_handler = _part_handlers_by_id.get(id, None)
    if not part_handler:
        filename = _part_filenames_by_id.get(id, None)
        if not filename:
            raise Exception("Can not found part with id '%s'" % id)
        part_handler = _part_handlers_by_id[id] = PartHandler(filename)
    return part_handler

def __write_index():
    fh = open(get_index_filename(), "w")
    fh.write(json.dumps(_parts_index))
    fh.close()

def fix_filename(filename):
    """Try to fix given filename if such file does not exist by using search
    pathes."""
    if os.path.exists(filename):
        return filename
    for search_path in get_search_pathes():
        fixed_filename = os.path.abspath(os.path.join(search_path, filename))
        if os.path.exists(fixed_filename):
            return fixed_filename
    raise IOError("Can not fix file: '%s'" % filename)

def parse(filename):
    """Create an xml parser and use it to parse a document. Return
    :class:`bb.hardware.devices.device.Device` object. The document name is
    passed in as `filename`.

    The document type (sketch or part) will be defined automatically
    by using file extension.
    """
    if not os.path.exists(filename):
        raise IOError("No such file: '%s'" % filename)
    index_parts()
    if filename.endswith(SketchHandler.FILE_EXT):
        # OK, we're going to work with sketch, we need to index
        # all the parts first in order to ommit collisions
        handler = SketchHandler()
        handler.open(filename)
    elif filename.endswith(PartHandler.FILE_EXT) or \
            filename.ednswith(PartHandler.ZFILE_EXT):
        handler = PartHandler()
        handler.open(filename)
    else:
        raise Exception("Do not know how to open %s" % fname)
    return handler.get_object()

#_______________________________________________________________________________

class Handler(object):
    def __init__(self, obj=None):
        self._fname = None
        self._buf = None
        self._root = None
        self._object = obj

    def get_object(self):
        return self._object

class SketchHandler(Handler):
    """This handler handles `Fritzing sketch file
    <http://fritzing.org/developer/fritzing-sketch-file-format/>`_."""

    ROOT_TAG_NAME = "module"
    TITLE_TAG_NAME = "title"
    INSTANCE_TAG_NAME = "instance"
    SCHEMATIC_VIEW_TAG_NAME = "schematicView"
    PCB_VIEW_TAG_NAME = "pcbView"
    ICON_VIEW_TAG_NAME = "iconView"

    FILE_EXT = "fz"

    def __init__(self, filename=None):
        Handler.__init__(self)
        self._object = Device()
        self._instance_handlers_table = dict()
        if filename:
            self.open(filename)

    def open(self, fname):
        self._fname = fname
        self._buf = None
        if not os.path.exists(fname):
            raise IOError("No such file: '%s'" % fname)
        if fname.endswith(self.FILE_EXT):
            self._stream = open(fname, "r")
        self.read()

    def find_instance_handler_by_index(self, id_):
        """Find and return :class:`InstanceHandler` by index (modelIndex)."""
        return self._instance_handlers_table.get(id_, None)

    def register_instance_handler(self, instance_handler):
        """Register :class:`bb.hardware.devices.device.Device` that
        belongs to :class:`InstanceHandler` by the handler of this
        sketch."""
        part = instance_handler.get_object()
        self._instance_handlers_table[instance_handler.model_index] = \
            instance_handler
        self.get_object().add_element(part)

    def read(self, stream=None):
        """Read sketch::

        <module fritzingVersion="..." moduleId="...">
        </module>"""
        if stream:
            self._stream = stream
        self._buf = self._stream.read()
        self._root = None
        # Read root element:
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
        for instance in instances:
            self.__process_instance(instance)

    def __process_instance(self, instance):
        handler = self.find_instance_handler_by_index( \
            instance.getAttribute("modelIndex"))
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
            id_ = connector_element.getAttribute("connectorId")
            src_connector = None
            if isinstance(part, Wire):
                src_connector = part.find_pin(id_)
            else:
                src_connector = part.find_elements(Pin).find_element(id_)
            if not src_connector:
                raise Exception("Can not find pin '%s' of '%s'" %
                                (id_, part.get_designator()))
            connects_elements = connector_element.getElementsByTagName("connects")
            if not connects_elements:
                continue
            connects_element = connects_elements.item(0)
            for connection_element in connects_element.getElementsByTagName("connect"):
                dst_part_index = connection_element.getAttribute("modelIndex")
                dst_handler = self.find_instance_handler_by_index(dst_part_index)
                dst_part = dst_handler.get_object()
                if isinstance(dst_part, Wire):
                    pin = dst_part.find_pin(connection_element.getAttribute("connectorId"))
                    if not pin:
                        raise Exception("Cannot find pin")
                    src_connector.connect_to(pin)
                else:
                    dst_connector = dst_part.find_elements(Pin).find_element(\
                        connection_element.getAttribute("connectorId"))
                    src_connector.connect_to(dst_connector)

    def __read_instance(self, instance):
        """Read instance entry and return InstanceHandler instance."""
        instance_handler = InstanceHandler()
        instance_handler.read(instance)
        self.register_instance_handler(instance_handler)
        return instance_handler

class PinHandler(Handler):
    """Learn more about connectors from `Fritzing part format
    <http://fritzing.org/developer/fritzing-part-format/>`_."""
    METADATA_PROPERTIES = ("description",)

    def __init__(self):
        self._object = Pin()

    def read(self, connector_element):
        """Read connector::

        <connector id="..." name="..." type="...">
        </connector>"""
        id_ = connector_element.getAttribute("id")
        if id_:
            self._object.set_designator(id_)
        name = connector_element.getAttribute("name")
        if name:
            self._object.set_property("name", name)
        #type_ = connector_element.getAttribute("type")
        #if type_:
        #    self._object.metadata.type = type_
        # Read metadata properties for this connector if such were defined
        for property_ in self.METADATA_PROPERTIES:
            elements = connector_element.getElementsByTagName(property_)
            if not elements:
                continue
            text = get_text(elements[0].childNodes)
            self._object.set_property(property_, text)

class InstanceHandler(Handler):
    """This class handles part instance from sketch."""

    def __init__(self):
        Handler.__init__(self)
        self.__model_index = None

    def read(self, element):
        """Read instance::

        <instance moduleIdRef="..." modelIndex="..." path="...">
        </instance>

        It may include ``<title>...</title>`` which will be translated as
        reference designator."""
        if not element.getAttribute("moduleIdRef"):
            raise Exception("Instance does not have 'moduleIdRef' attribute")
        part_handler = load_part_handler_by_id( \
            element.getAttribute("moduleIdRef"))
        if not part_handler:
            # The path attribute has the following view: :path
            # Do we need to take only the last path?
            part_fname = instance.getAttribute('path').split(":").pop()
            if not os.path.exists(part_fname):
                # In some way this path is absolute, we need to make it as
                # local for fritzing home directory
                if part_fname.startswith(os.sep):
                    part_fname = part_fname[1:]
                part_fname = os.path.abspath( \
                    os.path.join(get_search_pathes()[0], part_fname))
            if not os.path.exists(part_fname):
                raise IOError("No such part: '%s'" % part_fname)
            part_handler = PartHandler(fname=part_fname)
        self._object = part_handler.get_object().clone()
        if not element.hasAttribute("modelIndex"):
            raise Exception("Instance does not have modelIndex attribute.")
        self.model_index = element.getAttribute("modelIndex")
        # Part reference designator
        elements = element.getElementsByTagName("title")
        if elements:
            self._object.set_designator(get_text(elements[0].childNodes))

    @property
    def model_index(self):
        """This property allows you to set/get instance model
        index. This index represents model index on particular
        sketch."""
        return self.__model_index

    @model_index.setter
    def model_index(self, new_index):
        self.__model_index = new_index

class PartHandler(Handler):
    """A Fritzing part is made up of a number of files, one required metadata
    file (file suffix is ``.fzp``, so the metadata file is also referred to as
    an FZP), and up to four SVG files.

    The `Fritzing metadata file
    <http://fritzing.org/developer/fritzing-part-format/>`_ lists a part's
    title, description, and other properties, as well as a references to the
    part's SVG files. It also specifies a part's connectors and internal buses.
    """

    ROOT_TAG_NAME = "module"
    CONNECTORS_TAG_NAME = "connectors"
    CONNECTOR_TAG_NAME = "connector"

    FILE_EXT = "fzp"
    """Metadata file extension referred as an FZP."""
    ZFILE_EXT = "fzpz"
    """Extension for a zipped metadata file."""

    METADATA_PROPERTIES = (
        "version",
        "author",
        ("title", "name"),
        ("label", "reference_format"),
        "date",
        "description",
    )

    def __init__(self, filename=None, device=None):
        Handler.__init__(self)
        self._object = device or Device()
        self._model_index = None
        self._module_id = None
        if filename:
            self.open(filename)

    @property
    def model_index(self):
        return self._model_index

    @model_index.setter
    def model_index(self, new_model_index):
        self._model_index = new_model_index

    @property
    def module_id(self):
        return self._module_id

    @module_id.setter
    def module_id(self, new_module_id):
        self._module_id = new_module_id

    def open(self, fname):
        """Open and read fritzing part file, which can be zipped file
        :const:`PartHandler.ZFILE_EXT` or just
        :const:`PartHandler.FILE_EXT` file."""
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
        """Read part::

            <module fritzingVersion="..." moduleId="...">
            </module>
        """
        if not self._buf:
            raise Exception("The buffer is empty. Nothing to read.")
        self._doc = xml.dom.minidom.parseString(self._buf)
        # Read root element
        self._root = self._doc.documentElement
        if self._root.tagName != self.ROOT_TAG_NAME:
            raise Exception("'%s' has no '%s' root element" % \
                                (fname, self.ROOT_TAG_NAME))
        if not self._root.hasChildNodes():
            raise Exception("Root tag has no child nodes.")
        # Update part identifier
        self._object.id = self.module_id = self._root.getAttribute("moduleId")

        if self.module_id == "WireModuleID":
            self._object = Wire()

        # Put attributes such as author, description, date, label, etc. as
        # properties of the metadata instance for this part
        for src in self.METADATA_PROPERTIES:
            dst = None
            if is_tuple(src):
                src, dst = src
            else:
                dst = src
            elements = self._root.getElementsByTagName(src)
            if not elements:
                continue
            text = get_text(elements[0].childNodes)
            self._object.set_property(dst, text)
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
        property_ = self._object.set_property("keywords", list())
        for tag_element in tags_element.getElementsByTagName("tag"):
            property_.value.append(get_text(tag_element.childNodes))

    def __read_connectors(self):
        """Read connectors: <connectors>...</connectors>."""
        connectors_elements = self._root.getElementsByTagName(self.CONNECTORS_TAG_NAME)
        if not connectors_elements:
            # Some parts does not have connectors (e.g. note)
            return
        # Extract list of pins from connectors
        pins = list()
        connectors_element = connectors_elements.item(0)
        for connector_element in connectors_element.getElementsByTagName(self.CONNECTOR_TAG_NAME):
            connector_handler = PinHandler()
            connector_handler.read(connector_element)
            pins.append(connector_handler.get_object())
        # Handle special cases
        if isinstance(self._object, Wire):
            self._object.connect(pins[0], pins[1])
            return
        # Simply add all the pins to the element
        for pin in pins:
            self._object.add_element(pin)

    def __read_properties(self):
        """Read part's properties:

        <properties>
          <property name="...">...</property>
        </properties>"""
        properties = self._root.getElementsByTagName("properties").item(0)
        for property_ in properties.getElementsByTagName("property"):
            name = property_.getAttribute("name")
            text = get_text(property_.childNodes)
            self._object.set_property(name, get_text(property_.childNodes))

