#!/usr/bin/env python

"""Provide an interface to the mechanisms used to implement the import
statement.

See also:
http://docs.python.org/library/functions.html#__import__
http://docs.python.org/library/imp.html
http://www.python.org/dev/peps/pep-0302/
"""

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import os.path
import sys
import imp

class Importer:
    @classmethod
    def load(class_, name, globals_=None, locals_=None, fromlist=None,
             level=-1):
        """Allows to import modules as in the standard fashion
        Importer.load('os.path'), and also as Importer.load('os/path') or even
        Importer.load('os/path.py')."""
        # The module path is a directory or file. Provide dot-separator.
        #import os.path # XXX: very important to keep it here
        if os.path.isfile(name) or os.path.isdir(name):
            head = name
            name = ''
            while head:
                head, tail = os.path.split(head)
                if not len(name):
                    name = tail
                else:
                    name = '.'.join([tail, name])
        parent = class_._determine_parent(globals_, level)
        q, tail = class_._find_head_package(parent, name)
        module = class_._load_tail(q, tail)
        if not fromlist:
            return q
        if hasattr(module, "__path__"):
            class_._ensure_fromlist(module, fromlist)
        return module

    @classmethod
    def _determine_parent(class_, globals_, level=-1):
        if not globals_ or  not globals_.has_key("__name__"):
            return None
        pname = globals_['__name__']
        #if globals_.has_key("__path__"):
        if '__path__' in globals_:
            parent = sys.modules[pname]
            assert globals_ is parent.__dict__
            return parent
        if '.' in pname:
            i = pname.rfind('.')
            pname = pname[:i]
            parent = sys.modules[pname]
            assert parent.__name__ == pname
            return parent
        return None

    @classmethod
    def _find_head_package(class_, parent, name):
        # Import the first
        if '.' in name:
            # 'some.interesting.package':
            #   head = 'some'
            #   tail = 'interesting.package'
            i = name.find('.')
            head = name[:i]
            tail = name[i+1:]
        else:
            head = name
            tail = ""
        if parent:
            # If this is subpackage then qname = parent's name + head
            qname = "%s.%s" % (parent.__name__, head)
        else:
            qname = head
        q = class_._import_module(head, qname, parent)
        if q:
            return q, tail
        if parent:
            qname = head
            parent = None
            q = class_._import_module(head, qname, parent)
            if q: return q, tail
        raise ImportError("No module named " + qname)

    @classmethod
    def _load_tail(class_, q, tail):
        m = q
        while tail:
            i = tail.find('.')
            if i < 0: i = len(tail)
            head, tail = tail[:i], tail[i+1:]
            mname = "%s.%s" % (m.__name__, head)
            m = class_._import_module(head, mname, m)
            if not m:
                raise ImportError("No module named " + mname)
        return m

    @classmethod
    def _ensure_fromlist(class_, m, fromlist, recursive=0):
        for sub in fromlist:
            if sub == "*":
                if not recursive:
                    try:
                        all = m.__all__
                    except AttributeError:
                        pass
                    else:
                        class_._ensure_fromlist(m, all, 1)
                continue
            if sub != "*" and not hasattr(m, sub):
                #subname = "%s.%s" % (m.__name__, sub)
                subname = m.__name__
                submod = class_._import_module(sub, subname, m)
                if not submod:
                    raise ImportError("Can not import_module(%s, %s, %s)" %
                                      (sub, subname, m))

    @classmethod
    def _import_module(class_, partname, fqname, parent):
        try:
            return sys.modules[fqname]
        except KeyError:
            pass
        try:
            fp, pathname, stuff = imp.find_module(partname,
                                                  parent and parent.__path__)
        except ImportError:
            return None
        try:
            m = imp.load_module(fqname, fp, pathname, stuff)
        finally:
            if fp:
                fp.close()
        if parent:
            setattr(parent, partname, m)
        return m
