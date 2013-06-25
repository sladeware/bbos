# -*- coding: utf-8; -*-
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko <info@bionicbunny.org>

import __builtin__

import collections
import os
import re
import copy
import marshal
import inspect
import types
import new
import functools
from glob import glob1
from contextlib import contextmanager
import networkx

import bb.config
import bb.object
from bb.utils import path_utils
from bb.utils import logging
from bb.utils import proxy
from bb.utils.containers import DictWrapper
from bb.utils import typecheck
from bb.tools.interpreters import python
from bb.tools.b3 import primitives

logger = logging.get_logger("bb")

_addresses_by_buildfile = collections.defaultdict(set)
_rules_by_address = dict()
_parsed_contexts = set()
_dynamic_rules = collections.defaultdict(set)

class DependencyGraph(networkx.DiGraph):
  """Read more about dependency graph:
  <http://en.wikipedia.org/wiki/Dependency_graph>
  """

  def resolve_forks(self):
    forks = filter(lambda node: isinstance(node, Fork), self.nodes())
    for fork in forks:
      for parent in self.predecessors(fork):
        parent_lang = parent.get_property_value("programming_language")
        remove_edge = False
        for child in self.successors(fork):
          child_lang = child.get_property_value("programming_language")
          if not child_lang or parent_lang == child_lang:
            self.add_edge(parent, child)
            remove_edge = True
        if remove_edge:
          self.remove_edge(parent, fork)

  def save(self, filepath='dependency_graph.png'):
    import matplotlib.pyplot as plt
    pos = networkx.graphviz_layout(self)
    networkx.draw(self, pos, with_labels=True, arrows=True)
    plt.savefig(filepath)

dependency_graph = DependencyGraph()

def get_primitive(name):
  return getattr(primitives, name, None)

def register_primitive(primitive, name=None):
  """Registers and returns primitive."""
  if not name:
    name = primitive.__name__
  if hasattr(primitives, name):
    logger.warning("Primitive %s will be replaced" % name)
  setattr(primitives, name, primitive)
  return primitive

def unregister_primitive(name):
  raise NotImplementedError()

def primitive(name=None, primitive=None):
  if primitive:
    register_primitive(primitive, name)
  else:
    raise Exception()

setattr(primitives, "primitive", primitive)

_rule_classes = dict()

class RuleClassFactory(object):
  """This factory generates rule classes bases on a given rule class, e.g.
  RuleClassFactory(CCBinary).gen() will generate another CCBinary rule
  class. The key moment here is arguments that you can pass to gen() method.
  """

  template = """class %(name)s(%(unrolled_bases)s):
  abstract = rule_cls.abstract
  default_args = args
  default_kwargs = kwargs

  def __init__(self, *fargs, **fkwargs):
    new_kwargs = None
    if parent_class:
      new_kwargs = DictWrapper(getattr(parent_class, "default_kwargs").copy())
      new_kwargs.update(kwargs)
    else:
      new_kwargs = DictWrapper(kwargs.copy())
    new_kwargs.update(fkwargs)
    # MRO will fix all subclass collisions
    rule_cls.__init__(self, *(args + fargs), **new_kwargs)

  def locate(self):
    return Address(ctx.buildfile, self.get_name())"""

  def __init__(self, rule_cls):
    self._rule_cls = rule_cls

  def gen_name(self, target, cls):
    fullname = bb.object.get_class_fullname(target)
    parts = fullname.split(".")
    return "_".join(parts[:-1] + [parts[-1] + cls.__name__])

  def gen(self, *args, **kwargs):
    bases = [self._rule_cls]
    target = len(args) and args[0] or kwargs.get("target", None)
    if not target:
      raise Exception()
    name = self.gen_name(target, self._rule_cls)
    parent_class = None
    for subklass in self._rule_cls.__bases__:
      parent_class = _rule_classes.get(self.gen_name(target, subklass), None)
      if parent_class:
        bases.append(parent_class)
        break
    try:
      result = self.template % {
        'name': name,
        'unrolled_bases': ','.join(["bases[%d]" % i for i in range(len(bases))])
      }
    except Exception, e:
      raise Exception(e.message + ":\n" + self.template)
    namespace = dict(rule_cls=self._rule_cls,
                     bases=bases,
                     parent_class = parent_class,
                     DictWrapper = DictWrapper,
                     Address = Address,
                     ctx=Context.locate(),
                     args=args,
                     kwargs=kwargs)
    try:
      exec result in namespace
    except SyntaxError, e:
      raise SyntaxError(e.message + ':\n' + self.template.format(namespace))
    klass = namespace[name]
    _rule_classes[name] = klass
    if not klass.abstract:
      _dynamic_rules[target].add(klass)
    return klass

  __call__ = gen

def register_rule(rule, address=None):
  if not address:
    address = rule.get_address()
  existing = _rules_by_address.get(address)
  if existing and existing.get_address().buildfile != address.buildfile:
    raise KeyError("%s already defined in a sibling BUILD file: %s" % (
      address,
      existing.address,
    ))
  _rules_by_address[address] = rule
  _addresses_by_buildfile[address.buildfile].add(address)
  dependency_graph.add_node(rule)
  return rule

def get_rule(address):
  """Returns the specified module rule if already parsed; otherwise, parses the
  buildfile in the context of its parent directory and returns the parsed rule.
  """
  if not address or not isinstance(address, Address):
    return TypeError()
  def lookup():
    return _rules_by_address[address] if address in _rules_by_address \
        else None
  rule = lookup()
  if rule:
    return rule
  else:
    Context(address.buildfile).parse()
    return lookup()

def parse_address(spec):
  context = Context.locate()
  address = None
  if typecheck.is_string(spec):
    if spec.startswith(':'):
      # the :[rule] could be in a sibling BUILD - so parse using the canonical
      # address
      pathish = "%s:%s" % (context.buildfile.canonical_relpath, spec[1:])
      address = get_address(context.buildfile.root_dir, pathish, False)
    else:
      address = get_address(context.buildfile.root_dir, spec, False)
  else:
    for child_target_class in bb.object.get_all_subclasses(spec):
      for parent_target_class, rule_classes in _dynamic_rules.items():
        if issubclass(child_target_class, parent_target_class):
          rule = parse_address(":i%s" % id(rule_classes))
          if not rule:
            deps = map(lambda rc: rc(target=spec), rule_classes)
            rule = Fork(name="i%s" % id(rule_classes), deps=deps)
          return rule
  return None if not address else get_rule(address)

def get_address(root_dir, path, is_relative=True):
  """Parses pathish into an Address. A pathish can be one of:

  1. the (relative) path of a BUILD file
  2. the (relative) path of a directory containing a BUILD file child
  3. either of 1 or 2 with a ':[module name]' suffix
  4. a bare ':[module name]' indicating the BUILD file to use is the one in
     the current directory

  If the pathish does not have a module suffix the ruleed module name is taken
  to be the same name as the BUILD file's containing directory.  In this way the
  containing directory name becomes the 'default' module rule for pants.

  If there is no BUILD file at the path pointed to, or if there is but the
  specified module rule is not defined in the BUILD file, an IOError is
  raised.
  """
  parts = path.split(':') if not path.startswith(':') else ['.', path[1:]]
  path = parts[0]
  if is_relative:
    path = os.path.relpath(os.path.abspath(path), root_dir)
  buildfile = None
  try:
    buildfile = BuildFile(root_dir, path)
  except IOError, e:
    return None
  if len(parts) == 1:
    parent_name = os.path.basename(os.path.dirname(buildfile.relpath))
    return Address(buildfile, parent_name)
  else:
    rule_name = ':'.join(parts[1:])
    return Address(buildfile, rule_name)

# TODO: this routine has to be moved somewhere in graph package.
def bfs(g, start):
    queue, enqueued = collections.deque([(None, start)]), set([start])
    while queue:
        parent, n = queue.popleft()
        yield parent, n
        new = set(g[n]) - enqueued
        enqueued |= new
        queue.extend([(n, child) for child in new])

class Primitive(object):
  """This class has to be used by all rules that need to be primitives and can
  be used in all BUILD files.
  """

class RuleWithSources(object):
  """This class provides interface for all rules that have a deal with
  sources and thus have 'srcs' argument.
  """

  def __init__(self, srcs=[]):
    self._work_dir = self._find_work_dir()
    self._sources = []
    if srcs:
      self.add_sources(srcs)

  def __iadd__(self, other):
    if not other or not isinstance(other, RuleWithSources):
      raise TypeError(other)
    self.add_sources(other.get_sources())
    return self

  def _find_work_dir(self):
    """Find and return work directory."""
    cwd = os.path.abspath(os.getcwd())
    path = os.path.relpath(self.get_address().buildfile.parent_path, cwd)
    return os.path.abspath(path)

  def get_work_dir(self):
    return self._work_dir

  def set_work_dir(self, path):
    if not typecheck.is_string(path):
      raise TypeError()
    self._work_dir = path

  def clear_sources(self):
    self._sources = []

  def _add_callable_source(self, func):
    if not callable(func):
      raise TypeError()
    required_args = []
    if hasattr(func, "func_code"):
      if func.func_code.co_argcount >= 2:
        required_args = [self, self.get_target()]
    else:
      required_args = [self, self.get_target()]
    extra_sources = func(*required_args)
    if extra_sources:
      extra_sources = typecheck.is_list(extra_sources) and extra_sources or \
          [extra_sources]
      self.add_sources(extra_sources)

  def add_source(self, source):
    """The source may have any type, it can be another rule, string, function or
    an outside object. However, it cannot be None. Returns source, once it has
    been added.
    """
    if not source:
      raise TypeError()
    # The source is an object or another rule.
    if (isinstance(source, object) and not typecheck.is_function(source) and \
          not typecheck.is_string(source)) or \
          (typecheck.is_string(source) and source.startswith(":")):
      # First of all check for attribute "__build__" and call it to resolve
      # dependencies.
      if hasattr(source, "__build__"):
        self._add_callable_source(source.__build__)
      elif callable(source):
        self._add_callable_source(source.__call__)
      rule = parse_address(source)
      if rule:
        if source not in self.get_dependencies():
          self.add_dependency(rule)
        source = rule
      #else:
      #  logger.warning("Cannot find appropriate rule for the source: %s" %
      #                 source)
    # Source is a function or something that we should call. The result is
    # assumed to be an extra sources that will be added by add_sources().
    elif callable(source):
      self._add_callable_source(source)
      return
    elif typecheck.is_string(source):
      if not os.path.isabs(source):
        source = os.path.abspath(os.path.join(self._work_dir, source))
    # FIXME: can be add not string based sources?
    if typecheck.is_string(source) or isinstance(source, Rule):
      self._sources.append(source)
    return source

  def add_sources(self, sources):
    """Adds a list of sources with help of add_source() method. Returns
    nothing.
    """
    if not typecheck.is_list(sources):
      raise TypeError("Not a list of sources: %s" % sources)
    for source in sources:
      self.add_source(source)

  def get_expanded_sources(self):
    sources = []
    for source in self.get_sources():
      if isinstance(source, RuleWithSources):
        sources.extend(source.get_expanded_sources())
      else:
        sources.append(source)
    return sources

  def get_sources(self):
    return self._sources

class rule(type):

  def __new__(mcls, name, bases, d):
    d.setdefault("abstract", False)
    cls = type.__new__(mcls, name, bases, d)
    if Primitive in bb.object.get_all_subclasses(cls):
      name = mcls.gen_primitive_name(cls)
      register_primitive(cls, name)
      factory = RuleClassFactory(cls)
      register_primitive(factory, "%s_factory" % name)
    return cls

  @staticmethod
  def gen_primitive_name(cls):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class Rule(Primitive):
  """Within a BUILD file we have a number of named rules describing the build
  outputs.
  """

  __metaclass__ = rule

  is_language_dependent = False

  # Interfaces
  WithSources = RuleWithSources

  def __init__(self, target=None, name=None, execute=None, deps=[]):
    """Each rule has a name that identifies it within existed context. In case
    name wasn't provided, it becomes a target and vice-versa.
    """
    if not target and not name:
      raise Exception("target and/or name have to be provided")
    if name and not typecheck.is_string(name):
      raise TypeError("name has to be a string: %s,%s" % (name, target))
    self._target = target
    if not name:
      if typecheck.is_string(target):
        name = target
      elif typecheck.is_class(target) or typecheck.is_function(target):
        name = target.__name__
      else:
        name = "i%d" % id(target)
    self._name = name
    self._description = None
    self._address = None
    self._address = self.locate()
    self._dependencies = [] # TODO: deprecated
    self._properties = dict()
    self._build_dir = None
    # TODO: test on windows and other systems!
    self.set_build_dir(path_utils.join(
        bb.config.user_settings.get("b3", "builddir"), os.getcwd()[1:]))
    if hasattr(self.__class__, "properties"):
      self.add_properties(self.__class__.properties)
    register_rule(self)
    if execute:
      if not callable(execute):
        raise TypeError()
      self.execute = types.MethodType(execute, self)
    # Defer dependency resolution after parsing the current BUILD file to
    # allow for forward references
    self._post_init(self._finalize_deps, deps)

  def __eq__(self, other):
    result = other and (type(self) == type(other)) and \
        (self.get_address() == other.get_address())
    return result

  def __hash__(self):
    return hash(self.get_address())

  def __repr__(self):
    return "%s(%s)" % (type(self).__name__, self.get_address())

  def locate(self):
    context = Context.locate()
    return Address(context.buildfile, self.get_name())

  def get_address(self):
    return self._address

  def set_build_dir(self, path):
    if not typecheck.is_string(path):
      raise TypeError()
    self._build_dir = path

  def get_build_dir(self):
    return self._build_dir

  def buildpath(self, path, recursive=True):
    """Path will be created if it doesn't exist."""
    if typecheck.is_list(path):
      path = path_utils.join(*path)
    elif not typecheck.is_string(path):
      raise TypeError("path can be only a string or list")
    path = path_utils.join(self.get_build_dir(), path)
    if path_utils.exists(path):
      return path
    return path_utils.touch(path, recursive=recursive)

  def _post_init(self, func, *args, **kwargs):
    """Registers a command `func` to invoke after this rule's BUILD file is
    parsed.
    """
    Context.locate().on_context_exit(func, *args, **kwargs)

  def _walk_deps(self, walked, work, predicate=None):
    for rule in self.get_dependencies():
      if rule not in walked and isinstance(rule, Rule):
        walked.add(rule)
        if not predicate or predicate(rule):
          additional_rules = work(rule)
          if hasattr(rule, '_walk_deps'):
            rule._walk_deps(walked, work, predicate)
          if additional_rules:
            for additional_rule in additional_rules:
              if hasattr(additional_rule, '_walk_deps'):
                additional_rule._walk_deps(walked, work, predicate)

  def get_target(self):
    return self._target

  def set_description(self, description):
    if not typecheck.is_string(description):
      raise TypeError()
    self._description = description
    return self

  def get_name(self):
    """Returns the name of this target."""
    return self._name

  def add_properties(self, properties):
    for property_ in properties:
      self.add_property(property_)

  def add_property(self, property_):
    name, value = property_
    self._properties[name] = value

  def remove_property(self, name):
    del self._properties[name]

  def get_property_value(self, name):
    return self._properties.get(name, None)

  def execute(self):
    raise NotImplementedError()

  def resolve(self):
    for dep in self.get_dependencies():
      #dep.resolve()
      dep.execute()

  def get_dependency_graph(self):
    """Returns directed dependency tree."""
    nodes = []
    def _collect_subgraph_nodes(roots):
      nodes.extend(roots)
      for root in roots:
        _collect_subgraph_nodes(dependency_graph.successors(root))
    _collect_subgraph_nodes([self])
    return dependency_graph.subgraph(nodes)

  def get_common_languages(self):
    common_langs = set()
    for _, node in bfs(self.get_dependency_graph(), self):
      langs = []
      if isinstance(node, Fork):
        for child in self.get_dependency_graph().successors(node):
          lang = child.get_property_value("programming_language")
          if lang:
            langs.append(lang)
      else:
        langs = node.get_property_value("programming_language") or []
      if not langs:
        print "WARNING:", node, "doesn't have 'programming_language' property"
        continue
      if not common_langs:
        common_langs = set(langs)
      else:
        common_langs = common_langs.intersection(set(langs))
      if not common_langs:
        print "ERROR"
        break
    return common_langs

  def add_dependency(self, dep):
    rule = None
    if typecheck.is_tuple(dep) or typecheck.is_list(dep):
      rule = Fork(name="r%d" % hash(dep), deps=dep)
    else:
      rule = isinstance(dep, Rule) and dep or parse_address(dep)
    if rule:
      dep = rule
    else:
      if callable(dep):
        dep = new.instancemethod(dep, self, self.__class__)
        extra_deps = dep(self.target)
        if extra_deps:
          self.add_dependencies(extra_deps)
        return
    dependency_graph.add_edge(self, dep)
    self._dependencies.append(dep)

  def is_valid_dependency(self, dep):
    return True

  def set_dependencies(self, deps):
    """Sets the list of targets this target is dependent on."""
    self._dependencies = []
    self.add_dependencies(deps)

  def add_dependencies(self, deps):
    if not typecheck.is_list(deps) and not typecheck.is_tuple(deps):
      raise TypeError("%s: deps has to be a list or tuple, got %s" %
                      (self, type(deps)))
    for dep in deps:
      self.add_dependency(dep)

  def get_dependencies(self):
    """Returns list of dependencies of this target."""
    return dependency_graph.successors(self)

  def _finalize_deps(self, deps=[]):
    self.add_dependencies(deps)

  def walk_deps(self, work, predicate=None):
    """Performs a walk of this rule's dependency graph visiting each node
    exactly once. If a predicate is supplied it will be used to test each rule
    before handing the rule to work and descending.  Work can return rules in
    which case these will be added to the walk candidate set if not already
    walked.
    """
    self._walk_deps(set(), work, predicate)

class Address(object):
  """Represents a BUILD file rule address."""

  def __init__(self, buildfile, target):
    self.buildfile = buildfile
    self.target = target

  def __eq__(self, other):
    result = other and (type(other) == Address) and (
      self.buildfile.canonical_relpath == other.buildfile.canonical_relpath) and \
      (self.target == other.target)
    return result

  def __hash__(self):
    value = 17
    value *= 37 + hash(self.buildfile.canonical_relpath)
    value *= 37 + hash(self.target)
    return value

  def __ne__(self, other):
    return not self.__eq__(other)

  def __repr__(self):
    return "%s:%s" % (self.buildfile, self.target)

class Fork(Rule):

  def __init__(self, target=None, name=None, deps=[]):
    Rule.__init__(self, target, name, deps=deps)

class ContextError(Exception):
  """Inidicates an action that requires a BUILD file parse context was attempted
  outside any.
  """

class Context(object):
  """Defines the content of a parseable BUILD file rule and provides a
  mechanism for rules to discover their content when invoked via eval.
  """

  _active = collections.deque([])

  def __init__(self, buildfile):
    self.buildfile = buildfile
    self._parsed = False

  @staticmethod
  def locate():
    """Attempts to find the current root directory and buildfile. If there is
    an active parse context (see do_in_context), then it is returned.
    """
    if not Context._active:
      raise ContextError('No parse context active.')
    return Context._active[-1]

  def on_context_exit(self, func, *args, **kwargs):
    """ Registers a command to invoke just before this parse context is
    exited. It is an error to attempt to register an on_context_exit action
    outside an active parse context.
    """
    if not hasattr(self, '_on_context_exit'):
      raise ContextError('Can only register context exit actions when a parse'
                         'context is active')
    if not callable(func):
      raise TypeError('func must be a callable object')
    self._on_context_exit.append((func, args, kwargs))

  @staticmethod
  @contextmanager
  def activate(ctx):
    """Activates the given Context."""
    if hasattr(ctx, '_on_context_exit'):
      raise ContextError('Context actions registered outside this parse context'
                         'arg active')
    try:
      Context._active.append(ctx)
      ctx._on_context_exit = []
      yield
    finally:
      for func, args, kwargs in ctx._on_context_exit:
        func(*args, **kwargs)
      del ctx._on_context_exit
      Context._active.pop()

  def parse(self, **globalargs):
    """The entrypoint to parsing of a BUILD file. Changes the working directory
    to the BUILD file directory and then evaluates the BUILD file with the
    ROOT_DIR and __file__ globals set in addition to any globals specified as
    kwargs.  As rule methods are parsed they can examine the stack to find these
    globals and thus locate themselves for the purposes of finding files (see
    locate() and bind()).
    """
    if self.buildfile not in _parsed_contexts:
      buildfile_family = tuple(self.buildfile.family())
      _parsed_contexts.update(buildfile_family)
      pants_context = {}
      # Inject b3 primitives
      ast = compile("from bb.tools.b3.primitives import *", "<string>", "exec")
      python.Compatibility.exec_function(ast, pants_context)
      with Context.activate(self):
        start = os.path.abspath(os.curdir)
        try:
          os.chdir(self.buildfile.parent_path)
          for buildfile in buildfile_family:
            self.buildfile = buildfile
            eval_globals = copy.copy(pants_context)
            eval_globals.update({
              'ROOT_DIR': buildfile.root_dir,
              '__file__': buildfile.full_path,
            })
            eval_globals.update(globalargs)
            python.Compatibility.exec_function(buildfile.code(), eval_globals)
        finally:
          os.chdir(start)

  def do_in_context(self, work):
    """Executes the callable work in this parse context."""
    if not callable(work):
      raise TypeError('work must be a callable object')
    with Context.activate(self):
      return work()

  def __str__(self):
    return 'Context(BUILD:%s)' % self.buildfile

class BuildFile(object):
  """This class represents BUILD file."""

  _CANONICAL_NAME = "BUILD"
  _NAME_REGEXP = re.compile('^%s(\.[a-z]+)?$' % _CANONICAL_NAME)

  def __init__(self, root_dir, relpath, must_exist=True):
    path = os.path.abspath(os.path.join(root_dir, relpath))
    buildfile = os.path.join(path, BuildFile._CANONICAL_NAME) \
        if os.path.isdir(path) else path
    if os.path.isdir(buildfile):
      raise IOError("%s is a directory" % buildfile)
    if must_exist:
      if not os.path.exists(buildfile):
        raise IOError("BUILD file does not exist at: %s" % (buildfile))
      if not BuildFile._is_buildfile_name(os.path.basename(buildfile)):
        raise IOError("%s is not a BUILD file" % buildfile)
      if not os.path.exists(buildfile):
        raise IOError("BUILD file does not exist at: %s" % buildfile)
    self.root_dir = root_dir
    self.full_path = buildfile
    self.name = os.path.basename(self.full_path)
    self.parent_path = os.path.dirname(self.full_path)
    self._bytecode_path = os.path.join(self.parent_path, '.%s.%s.pyc' %
                                       (self.name, python.PythonIdentity.get()))
    self.relpath = os.path.relpath(self.full_path, self.root_dir)
    self.canonical_relpath = os.path.join(os.path.dirname(self.relpath),
                                          BuildFile._CANONICAL_NAME)

  def __hash__(self):
    return hash(self.full_path)

  def __eq__(self, other):
    result = other and (type(other) == BuildFile) and \
        (self.full_path == other.full_path)
    return result

  def __repr__(self):
    return self.relpath

  def code(self):
    """Returns the code object for this BUILD file."""
    if (os.path.exists(self._bytecode_path)
        and os.path.getmtime(self.full_path) <= \
          os.path.getmtime(self._bytecode_path)):
      with open(self._bytecode_path, 'rb') as bytecode:
        return marshal.load(bytecode)
    else:
      with open(self.full_path, 'rb') as source:
        code = compile(source.read(), self.full_path, 'exec')
        with open(self._bytecode_path, 'wb') as bytecode:
          marshal.dump(code, bytecode)
        return code

  @staticmethod
  def _is_buildfile_name(name):
    return BuildFile._NAME_REGEXP.match(name)

  def get_all_addresses(self):
    global _addresses_by_buildfile
    def lookup():
      if self in _addresses_by_buildfile:
        return _addresses_by_buildfile[self]
      else:
        return []
    addresses = lookup()
    if addresses:
      return addresses
    else:
      Context(self).parse()
      return lookup()

  def siblings(self):
    """Returns an iterator over all the BUILD files co-located with this BUILD
    file not including this BUILD file itself.
    """
    for build in glob1(self.parent_path, 'BUILD*'):
      if self.name != build and BuildFile._is_buildfile_name(build):
        siblingpath = os.path.join(os.path.dirname(self.relpath), build)
        if not os.path.isdir(os.path.join(self.root_dir, siblingpath)):
          yield BuildFile(self.root_dir, siblingpath)

  def family(self):
    """Returns an iterator over all the BUILD files co-located with this BUILD
    file including this BUILD file itself.  The family forms a single logical
    BUILD file composed of the canonical BUILD file and optional sibling build
    files each with their own extension, eg: BUILD.extras.
    """
    yield self
    for sibling in self.siblings():
      yield sibling
