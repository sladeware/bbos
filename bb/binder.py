class Extension(object):
    """Interface!"""
    def on_add(self, project):
        """This event will be called each time the extension will be added to
        the project. Initially it's called from project.add_source() or
        project.add_extension()."""
        raise NotImplementedError

    def on_remove(self, project):
        """This event will be called each time the extension will be removed
        from the project. Initially it's called from project.remove_source()
        or project.remove_extension()."""
        raise NotImplementedError

    def on_build(self, project):
        """Called each time before the project is going to be built."""
        raise NotImplementedError

    def on_load(self, project):
        """Called each time before the project os going to be load."""
        raise NotImplementedError

_wrappers = {}

def get_wrapper(klass):
    if not klass.__name__ in _wrappers:
        return None
    return _wrappers[klass.__name__]

def wrap(obj):
    wrapper = get_wrapper(obj.__class__)
    if not wrapper:
        return None
    return wrapper(obj)

class Wrapper(Extension):
    """Interface!"""
    mapping = {}

    def __init__(self, target):
        Extension.__init__(self)
        for (event, action) in self.mapping.items():
            method = MethodType(action, target)
            setattr(self, event, method)

    @classmethod
    def bind(_, event, klass):
        def decorate(action):
            target_klass = klass
            if not isinstance(target_klass, Extension):
                target_klass = get_wrapper(klass)
                if not target_klass:
                    target_klass = type('_' + klass.__name__, (Wrapper,), dict(mapping={}))
                    _wrappers[klass.__name__] = target_klass
                target_klass.mapping[event] = action
            return action
        return decorate

