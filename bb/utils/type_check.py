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

__copyright__ = "Copyright (c) 2011-2012 Sladeware LLC"

"""Validation tools for generic object structures.
"""

from types import *

def validate(**_params_):
    def check_types(_func_, _params_ = _params_):
        def modified(*args, **kw):
            arg_names = _func_.func_code.co_varnames
            kw.update(zip(arg_names, args))
            for name, type in _params_.iteritems():
                param = kw[name]
                if isinstance(type, TypeType):
                    assert param is None or isinstance(param, type),\
                        "Parameter '%s' should be type '%s'" % (name, type.__name__)
                elif isinstance(type, FunctionType):
                   assert type(param), "Parameter '%s' didn't pass %s" % (name, type.__name__)
                else:
                    assert "!"
            return _func_(**kw)
        return modified
    return check_types

def is_int(var):
    """Return ``True`` if the specified object is an integer."""
    return type(var) is IntType

def is_long(var):
    """Return true if the specified object is a long integer."""
    return type(var) is LongType

def is_boolean(var):
    """Return true if the specified object is a boolean."""
    return type(var) is BooleanType

is_bool = is_boolean

def is_string(var):
    """Return true if the specified object is a string."""
    return type(var) is StringType

def is_list(var):
    """Return true if the specified variable is a list."""
    return type(var) is ListType

def is_tuple(var):
    return type(var) is TupleType

def is_dict(var):
    """Return true if the specified variable is a dictionary."""
    return type(var) is DictType

def is_number(x):
    "Is x a number? We say it is if it has a __int__ method."
    return hasattr(x, '__int__')

def is_sequence(x):
    "Is x a sequence? We say it is if it has a __getitem__ method."
    return hasattr(x, '__getitem__')

def verify_boolean(var):
    if var and not is_boolean(var):
        raise TypeError("'%s' is not a boolean type: %s" %
                        (var.__class__.__name__, var))
    return var

verify_bool = verify_boolean

def validate_int(var):
    if var and not is_int(var):
        raise TypeError("'%s' is not a int type: %s" %
                        (var.__class__.__name__, var))
    return var

verify_int = validate_int # Remove

def verify_list(var):
    if var and not is_list(var):
        raise TypeError("'%s' is not a list type: %s" %
                        (var.__class__.__name__, var))
    return var

def verify_string(var):
    if not var or not is_string(var):
        raise TypeError("'%s' is not a string type: %s" %
                        (var.__class__.__name__, var))
    return var
