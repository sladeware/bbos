#!/usr/bin/env python
#
# http://bionicbunny.org/
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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

# TODO: see <http://peak.telecommunity.com/doc/src/peak/config/modules.html>

from imp import PY_COMPILED, PY_SOURCE, get_magic, get_suffixes
import sys
import types

PATCHES = {}

def finalize(level=1):
  """Builds module with appropriate patches, resolves module inheritance. This
  routine must be called only at the very end of a module's code. This is
  because any code which follows 'finalize_module()' will be executed twice.
  (Actually, the code before 'setupModule()' gets executed twice, also, but the
  module dictionary is reset in between, so its execution is cleaner.)
  """
  f = sys._getframe(level)
  d = frame.f_globals
  c = frame.f_code
  n = d["__name__"]
  m = sys.modules[name]
  build_module(m, c)

def build(module, code=None):
  codelist = get_code_list(module, code)
  d = module.__dict__
  if len(codelist)>1:
    saved = {}
    for name in '__file__', '__path__', '__name__', '__codelist__':
      try:
        saved[name] = d[name]
      except KeyError:
        pass
    d.clear()
    d.update(saved)
    map(sim.execute, codelist)
    sim.finish()
  if "__init__" in d:
    d["__init__"]()

def to_bases(bases, name=''):
  if isinstance(bases, (str, types.ModuleType)):
    bases = bases,
  for base in bases:
    if isinstance(base, str):
      base = lazyModule(name,b)
    yield b

def get_bases(module, name=''):
  return tuple(to_bases(getattr(module, "__bases__", ()), name))

def get_legacy_code(module):
  # TODO: this won't work with zipfiles yet
  file = module.__file__
  for (ext, mode, typ) in get_suffixes():
    if not file.endswith(ext):
      continue
    if typ == PY_COMPILED:
      f = open(file, mode)
      if f.read(4) == get_magic():
        f.read(4)   # skip timestamp
        import marshal
        code = marshal.load(f)
        f.close()
        return code
      # Not magic!
      f.close()
      raise AssertionError("Bad magic for %s" % file)
    elif typ == PY_SOURCE:
      f = open(file, mode)
      code = f.read()
      f.close()
      if code and not code.endswith('\n'):
        code += '\n'
      return compile(code, file, 'exec')
  raise AssertionError("Can't retrieve code for %s" % module)

def get_code_list(module, code=None):
  if hasattr(module,'__codelist__'):
    return module.__codeList__
  if code is None:
    code = get_legacy_code(module)
  name = module.__name__
  code = prepForSimulation(code)
  code_list = module.__codelist__ = PATCHES.get(name, []) + [code]
  bases = get_bases(module, name)
  path = getattr(module,'__path__', [])
  for base_module in bases:
    if not isinstance(base_module, types.ModuleType):
      raise TypeError("%s is not a module in %s __bases__" % (base_module,name))
    for p in getattr(base_module, '__path__', ()):
      if p in path:
        path.remove(p)
      path.append(p)
    for c in get_code_list(base_module):
      if c in codeList:
        code_list.remove(c)
      code_list.append(c)
  if path:
    module.__path__ = path
  return code_list
