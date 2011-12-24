#!/usr/bin/env python

"""This module provides compatibility with Fritzing EDA."""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

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
from hashlib import md5

from bb.eda.compatibility import EDA
from bb.eda import Device, Part, Pin
from bb.utils.type_check import verify_list, verify_string, is_string, is_tuple, is_list

def md5sum(filename, buf_size=8192):
    m = md5()
    # the with statement makes sure the file will be closed 
    with open(filename) as f:
        # We read the file in small chunk until EOF
        data = f.read(buf_size)
        while data:
            # We had data to the md5 hash
            m.update(data)
            data = f.read(buf_size)
    # We return the md5 hash in hexadecimal format
    return m.hexdigest()

#_______________________________________________________________________________

class Fritzing(EDA):
    """This class represents Fritzing EDA. Fritzing is an open source software 
    initiative to support designers
    and artists ready to move from physical prototyping to actual
    product. It was developed at the University of Applied Sciences of
    Potsdam."""

    user_dir = None
    """User defined fritzing user directory that can be set with help of
    Fritzing.set_user_dir() function."""

    search_pathes = list()
    """A list of strings that specifies the search path for Fritzing files. By
    default includes user directory and home directory."""

    parts_index = dict()
    part_handlers_by_id = dict()
    part_filenames_by_id = dict()

    INDEX_FILENAME = "fritzing.index"

    def __init__(self):
        EDA.__init__(self)

    @classmethod
    def get_default_user_dir(cls):
        """Return default path to the global fritzing user directory
        depending on operating system."""
        default_dirs = {
            "posix": "%s/.config/Fritzing" % os.environ["HOME"],
        }
        return default_dirs.get(os.name, None)

    @classmethod
    def get_user_dir(cls):
        """Return path to the global user directory. The location of this
        directory differs depending on operating system, and might
        even be hidden by default (see Fritzing.get_default_user_dir())."""
        return cls.user_dir or cls.get_default_user_dir()

    @classmethod
    def get_search_pathes(cls):
        """Return list of strings that specifies the search path for
        fritzing files."""
        search_pathes = [cls.get_home_dir(), cls.get_user_dir()]
        return search_pathes

    @classmethod
    def find_part_files(cls, pathes, recursive=False):
        """Search and return a list of Fritzing part files `.fzp` that can be
        found at given pathes. List subdirectories recursively if flag
        `recursive` is True."""
        if not is_list(pathes):
            pathes = [pathes]
        files = list()
        for path in pathes:
            if os.path.isdir(path):
                for name in os.listdir(path):
                    if name.startswith("."): # improve this
                        continue
                    pathes.append(os.path.join(path, name))
            elif os.path.isfile(path) and path.endswith(PartHandler.FILE_EXT):
                files.append(os.path.abspath(path))
        return files

    @classmethod
    def index_parts(cls, search_pathes=None, force=False):
        """Index all Fritzing parts that can be found from `search_pathes`. By
        default if `search_pathes` were not defined then
        `Fritzing.get_search_pathes()` will be used.
        
        Once all the parts were indexed, they are stored at index file
        Fritzing.INDEX_FILENAME in order to increase performance in future.
        However, each new time the index table is loading, the system will
        remove obsolete parts
        and add new parts if such will be found. In order to reindex all parts
        set `force` as True."""
        if len(cls.parts_index):
            return
        if not search_pathes:
            search_pathes = cls.get_search_pathes()
        # Read index file
        if os.path.exists(cls.INDEX_FILENAME):
            index_fh = open(cls.INDEX_FILENAME)
            cls.parts_index = json.loads(''.join(index_fh.readlines()))
            index_fh.close()
        all_part_files = list()
        for search_path in cls.get_search_pathes():
            for parts_location in ("parts", "resources/parts"):
                for group in ("core", "user", "obsolete", "contrib"):
                    path = os.path.join(search_path, parts_location, group)
                    if not os.path.exists(path):
                        continue
                    all_part_files.extend(cls.find_part_files(path, recursive=True))
        # Look up for broken files and remove them
        broken_files = set(cls.parts_index.keys()) - set(all_part_files)
        for filename in broken_files:
            del cls.parts_index[filename]
        # Start working...
        has_updates = False
        counter = 0
        total = len(all_part_files)
        for pfile in all_part_files:
            frmt = "%"+ str(len(str(total))) +"d/%d\r"
            sys.stdout.write(frmt % (counter, total))
            counter += 1
            # Make check sum for this file            
            checksum = md5sum(pfile)
            if pfile in cls.parts_index:
                (old_checksum, old_module_id) = cls.parts_index[pfile]
                if old_checksum == checksum:
                    cls.part_handlers_by_id[old_module_id] = None
                    cls.part_filenames_by_id[old_module_id] = pfile
                    continue
            ph = PartHandler(pfile)
            cls.parts_index[pfile] = (checksum, ph.module_id)
            cls.part_handlers_by_id[ph.module_id] = ph
            cls.part_filenames_by_id[module_id] = pfile
            has_updates = True
        # Rewrite index file only if it has some updates
        if has_updates:
            cls.__write_index()
        # Update 

    @classmethod
    def load_part_handler_by_id(cls, id):
        part_handler = cls.part_handlers_by_id[id]
        if not part_handler:
            filename = cls.part_filenames_by_id[id]
            part_handler = cls.part_handlers_by_id[id] = PartHandler(filename)
        return part_handler

    @classmethod
    def __write_index(cls):
        fh = open(cls.INDEX_FILENAME, "w")
        fh.write(json.dumps(cls.parts_index))
        fh.close()

    @classmethod
    def reindex_parts(cls):
        cls.parts_index = dict()
        cls.index_parts()

    @classmethod
    def fix_filename(cls, filename):
        """Try to fix given filename if such does not exist by using search
        pathes."""
        if os.path.exists(filename):
            return filename
        for search_path in cls.get_search_pathes():
            fixed_filename = os.path.abspath(os.path.join(search_path, filename))
            if os.path.exists(fixed_filename):
                return fixed_filename
        raise IOError("Can not fix file: '%s'" % filename)

    @classmethod
    def parse(cls, fname_or_stream, handler=None):
        if is_string(fname_or_stream):
            fname = cls.fix_filename(fname_or_stream)
            if not os.path.exists(fname):
                raise IOError("No such file: '%s'" % fname)
            if not handler:
                if fname.endswith(SketchHandler.FILE_EXT):
                    # OK, we're going to work with sketch, we need to index
                    # all the parts first in order to ommit collisions
                    cls.reindex_parts()
                    handler = SketchHandler()
                    handler.open(fname)
                elif fname.endswith(PartHandler.FILE_EXT) or \
                        fname.ednswith(PartHandler.ZFILE_EXT):
                    handler = PartHandler()
                    handler.open(fname)
                else:
                    raise Exception("Do not know how to open %s" % fname)
        return handler.get_object()

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
    PCB_VIEW_TAG_NAME = "pcbView"
    ICON_VIEW_TAG_NAME = "iconView"

    FILE_EXT = "fz"

    def __init__(self, fname=None):
        Handler.__init__(self)
        self._object = Device()
        self._part_handlers_table = dict()
        if fname:
            self.open(fname)

    def open(self, fname):
        self._fname = fname
        self._buf = None
        if not os.path.exists(fname):
            raise IOError("No such file: '%s'" % fname)
        if fname.endswith(self.FILE_EXT):
            self._stream = open(fname, "r")
        self.read()

    def find_part_handler_by_index(self, id_):
        return self._part_handlers_table.get(id_, None)

    def register_part_handler(self, part_handler):
        """Add Part handled by PartHandler to Sketch handled by
        SketchHandler."""
        part = part_handler.get_object()
        self._part_handlers_table[part_handler.model_index] = part_handler
        self.get_object().add_part(part)

    def read(self, stream=None):
        if stream:
            self._stream = stream
        self._buf = self._stream.read()
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
        handler = self.find_part_handler_by_index(instance.getAttribute("modelIndex"))
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
            src_connector = part.find_pin(id_)
            connects_elements = connector_element.getElementsByTagName("connects")
            if not connects_elements:
                continue
            connects_element = connects_elements.item(0)
            for connection_element in connects_element.getElementsByTagName("connect"):
                dst_part_index = connection_element.getAttribute("modelIndex")
                dst_handler = self.find_part_handler_by_index(dst_part_index)
                dst_part = dst_handler.get_object()
                dst_connector = dst_part.find_pin( \
                    connection_element.getAttribute("connectorId"))
                src_connector.connect_to(dst_connector)

    def __read_instance(self, instance):
        """Read instance entry:

          <instance>
            ...
          </instance>

        And return PartHandler instance."""
        id = instance.getAttribute("moduleIdRef")
        part_handler = Fritzing.load_part_handler_by_id(id)
        if not part_handler:
            # The path attribute has the following view: :path
            # Do we need to take only the last path?
            part_fname = instance.getAttribute('path').split(":").pop()
            if not os.path.exists(part_fname):
                # In some way this path is absolute, we need to make it as local for
                # FRITZING_HOME directory
                if part_fname.startswith(os.sep):
                    part_fname = part_fname[1:]
                part_fname = os.path.abspath(os.path.join(Fritzing.get_search_pathes()[0], part_fname))
            if not os.path.exists(part_fname):
                raise IOError("No such part: '%s'" % part_fname)
            part_handler = PartHandler(fname=part_fname)
        part = part_handler.get_object()
        if not instance.hasAttribute("modelIndex"):
            raise Exception()
        part_handler.model_index = instance.getAttribute("modelIndex")
        # Part reference
        elements = instance.getElementsByTagName("title")
        if elements:
            part.reference = get_text(elements[0].childNodes)
        self.register_part_handler(part_handler)
        return part_handler

#_______________________________________________________________________________

class PinHandler(Handler):
    """Learn more about connectors:
      http://fritzing.org/developer/fritzing-part-format/"""
    METADATA_PROPERTIES = ("description",)

    def __init__(self):
        self._object = Pin()

    def read(self, connector_element):
        #<connector id="..." name="..." type="...">
        #  ...
        #</connector>
        id_ = connector_element.getAttribute("id")
        if id_:
            self._object.id = id_
        name = connector_element.getAttribute("name")
        if name:
            self._object.designator = name
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

#_______________________________________________________________________________

class PartHandler(Handler):
    """A Fritzing part is made up of a number of files, one required
    metadata file (file suffix is `.fzp`, so the metadata file is also
    referred to as an FZP), and up to four SVG files.

    The metadata file lists a part's title, description, and other
    properties, as well as a references to the part's SVG files. It
    also specifies a part's connectors and internal buses.

    Learn more about fritzing part format: http://fritzing.org/developer/fritzing-part-format/"""

    ROOT_TAG_NAME = "module"
    CONNECTORS_TAG_NAME = "connectors"
    CONNECTOR_TAG_NAME = "connector"

    # Metadata file extension referred as an FZP
    FILE_EXT = "fzp"
    # Extension for a zipped metadata file
    ZFILE_EXT = "fzpz"

    METADATA_PROPERTIES = (
        "version",
        "author",
        ("title", "name"),
        ("label", "reference_format"),
        "date",
        "description",
    )

    def __init__(self, fname=None, part=None):
        Handler.__init__(self)
        self._object = part or Part()
        self._model_index = None
        self._module_id = None
        if fname:
            self.open(fname)

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
        # Update part identifier
        self._object.id = self.module_id = self._root.getAttribute("moduleId")
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
        connectors_element = connectors_elements.item(0)
        for connector_element in connectors_element.getElementsByTagName(self.CONNECTOR_TAG_NAME):
            connector_handler = PinHandler()
            connector_handler.read(connector_element)
            self._object.add_pin(connector_handler.get_object())

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

