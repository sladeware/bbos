#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "<oleks.sviridenko@gmail.com> Oleksandr Sviridenko"

#______________________________________________________________________________
# Compatibility with Python 2.2, 2.3, and 2.4

# The AIMA code was originally designed to run in Python 2.2 and up.
# The first part of this file implements for Python 2.2 through 2.4
# the parts of 2.5 that the original code relied on. Now we're
# starting to go beyond what can be filled in this way, but here's
# the compatibility code still since it doesn't hurt:

try:
    bool, True, False ## Introduced in 2.3
except NameError:
    class bool(int):
        """Simple implementation of Booleans, as in PEP 285."""
        def __init__(self, val): self.val = val
        def __int__(self): return self.val
        def __repr__(self): return ('False', 'True')[self.val]

    True, False = bool(1), bool(0)

try:
    sum ## Introduced in 2.3
except NameError:
    def sum(seq, start=0):
        """Sum the elements of seq.
        >>> sum([1, 2, 3])
        6
        """
        return reduce(operator.add, seq, start)

try:
    enumerate ## Introduced in 2.3
except NameError:
    def enumerate(collection):
        """Return an iterator that enumerates pairs of (i, c[i]). PEP 279.
        >>> list(enumerate('abc'))
        [(0, 'a'), (1, 'b'), (2, 'c')]
        """
        ## Copied from PEP 279
        i = 0
        it = iter(collection)
        while 1:
            yield (i, it.next())
            i += 1


try:
    reversed ## Introduced in 2.4
except NameError:
    def reversed(seq):
        """Iterate over x in reverse order.
        >>> list(reversed([1,2,3]))
        [3, 2, 1]
        """
        if hasattr(seq, 'keys'):
            raise TypeError("mappings do not support reverse iteration")
        i = len(seq)
        while i > 0:
            i -= 1
            yield seq[i]

try:
    sorted ## Introduced in 2.4
except NameError:
    def sorted(seq, cmp=None, key=None, reverse=False):
        """Copy seq and sort and return it.
        >>> sorted([3, 1, 2])
        [1, 2, 3]
        """
        seq2 = copy.copy(seq)
        if key:
            if cmp == None:
                cmp = __builtins__.cmp
            seq2.sort(lambda x,y: cmp(key(x), key(y)))
        else:
            if cmp == None:
                seq2.sort()
            else:
                seq2.sort(cmp)
        if reverse:
            seq2.reverse()
        return seq2

try:
    set, frozenset ## set builtin introduced in 2.4
except NameError:
    try:
        import sets ## sets module introduced in 2.3
        set, frozenset = sets.Set, sets.ImmutableSet
    except (NameError, ImportError):
        class BaseSet:
            "set type (see http://docs.python.org/lib/types-set.html)"

            def __init__(self, elements=[]):
                self.dict = {}
                for e in elements:
                    self.dict[e] = 1

            def __len__(self):
                return len(self.dict)

            def __iter__(self):
                for e in self.dict:
                    yield e

            def __contains__(self, element):
                return element in self.dict

            def issubset(self, other):
                for e in self.dict.keys():
                    if e not in other:
                        return False
                return True

            def issuperset(self, other):
                for e in other:
                    if e not in self:
                        return False
                return True

            def union(self, other):
                return type(self)(list(self) + list(other))

            def intersection(self, other):
                return type(self)([e for e in self.dict if e in other])

            def difference(self, other):
                return type(self)([e for e in self.dict if e not in other])

            def symmetric_difference(self, other):
                return type(self)([e for e in self.dict if e not in other] +
                                  [e for e in other if e not in self.dict])

            def copy(self):
                return type(self)(self.dict)

            def __repr__(self):
                elements = ", ".join(map(str, self.dict))
                return "%s([%s])" % (type(self).__name__, elements)

            __le__ = issubset
            __ge__ = issuperset
            __or__ = union
            __and__ = intersection
            __sub__ = difference
            __xor__ = symmetric_difference

        class frozenset(BaseSet):
            "A frozenset is a BaseSet that has a hash value and is immutable."

            def __init__(self, elements=[]):
                BaseSet.__init__(elements)
                self.hash = 0
                for e in self:
                    self.hash |= hash(e)

            def __hash__(self):
                return self.hash

        class set(BaseSet):
            "A set is a BaseSet that does not have a hash, but is mutable."

            def update(self, other):
                for e in other:
                    self.add(e)
                return self

            def intersection_update(self, other):
                for e in self.dict.keys():
                    if e not in other:
                        self.remove(e)
                return self

            def difference_update(self, other):
                for e in self.dict.keys():
                    if e in other:
                        self.remove(e)
                return self

            def symmetric_difference_update(self, other):
                to_remove1 = [e for e in self.dict if e in other]
                to_remove2 = [e for e in other if e in self.dict]
                self.difference_update(to_remove1)
                self.difference_update(to_remove2)
                return self

            def add(self, element):
                self.dict[element] = 1

            def remove(self, element):
                del self.dict[element]

            def discard(self, element):
                if element in self.dict:
                    del self.dict[element]

            def pop(self):
                key, val = self.dict.popitem()
                return key

            def clear(self):
                self.dict.clear()

            __ior__ = update
            __iand__ = intersection_update
            __isub__ = difference_update
            __ixor__ = symmetric_difference_update

#_______________________________________________________________________________
# Miscellaneous Functions

def caller(n=1):
    """Return the name of the calling function n levels up in the frame stack.
    >>> caller(0)
    'caller'
    >>> def f():
    ...     return caller()
    >>> f()
    'f'
    """
    import inspect
    return inspect.getouterframes(inspect.currentframe())[n][3]

_PROPERTIES_BY_CLASS = dict()

def property(f):
    """Redefine built-in property function that return a property
    attribute for new-style classes (classes that derive from
    object). Properties defined with help of this decorator can be
    extracted by using get_properties().
    """
    import __builtin__
    cls_name = caller(2)
    if cls_name not in _PROPERTIES_BY_CLASS:
        _PROPERTIES_BY_CLASS[cls_name] = dict()
    _PROPERTIES_BY_CLASS[cls_name][f.__name__] = f
    return __builtin__.property(f)

def get_properties(obj):
    """Return a list of names of property attributes defined with help of
    property() decorator. For example::

    class Metadata(object):
        def __init__(self):
            self._name = "UNKNOWN"
            self._author = "UNKNOWN"

        @property
        def name(self):
            return self._name

        @property
        def author(self):
            return self._author

    If then metadata is an instance of Metadata, then
    get_properties(metadata) will return ['name', 'author'].
    """
    import types
    cls_name = None
    if isinstance(obj, object):
        cls_name = obj.__class__.__name__
    if type(obj) == types.TypeType:
        cls_name = obj.__name__
    if cls_name not in _PROPERTIES_BY_CLASS:
        return None
    return _PROPERTIES_BY_CLASS[cls_name].keys()
