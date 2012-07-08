#!/usr/bin/env python

class OS(object):
    def main(self):
        """This method implements OS's activity. You may override this method in
        subclass.
        """
        self.kernel.start()

class Kernel(object):
    def __init__(self):
        print self.banner()
        print "Initialize kernel"

    def start(self):
        self.test()
        print "Start kernel"
        try:
            if self.has_scheduler():
                while True:
                    self.get_scheduler().move()
                    self.switch_thread()
        except KeyboardInterrupt, e:
            self.stop()
        except SystemExit, e:
            self.stop()

    def stop(self):
        """Shutdown everything and perform a clean system stop."""
        print "Kernel stopped"
        sys.exit(0)

    def add_thread(self, *args, **kargs):
        """Add a new thread to the kernel. Return thread's object. Can be used
        as a thread factory.

        Note: this method is available in all modes, so be carefull to
        make changes."""
        if not len(args) and not len(kargs):
            raise Kernel.Exception("Nothing to process")
        if len(args) == 1:
            thread = self.select_thread(args[0])
            if thread:
                raise Exception("Thread '%s' has been already added"
                                % thread.get_name())
        if type(args[0]) is types.StringType:
            # Create a new thread instance
            thread = Thread(*args)
        else:
            thread = args[0]
        self.echo("Add thread '%s'" % thread.get_name())
        self.__threads[ thread.get_name() ] = thread
        # Introduce thread to scheduler
        self.get_scheduler().enqueue_thread(thread)
        # Register available commands
        #self.add_commands(thread.get_commands())
        return thread

    def warning(self, text):
        lineno = inspect.getouterframes(inspect.currentframe())[2][2]
        fname = inspect.getmodule(inspect.stack()[2][0]).__file__
        self.echo("%s:%d:WARNING: %s" % (fname, lineno, text))

    def echo(self, data):
        if not isinstance(data, types.StringType):
            data = str(data)
        print data

    def test(self):
        print "Test kernel"
        if not self.get_num_threads():
            raise Kernel.Exception("At least one thread has to be added")
        # Test the system for unknown devices
        if self.get_unknown_devices():
            self.warning("Unknown devices: %s" % ", ".join([str(device) for device
                                                in self.get_unknown_devices()]))

    def panic(self, text):
        """Halt the system.

        Display a message, then perform cleanups with stop. Concerning
        the application this allows to stop a single process, while
        all other processes are running.
        """
        lineno = inspect.getouterframes(inspect.currentframe())[2][2]
        fname = inspect.getmodule(inspect.stack()[2][0]).__file__
        print "%s:%d:PANIC: %s" % (fname, lineno, text)
        # XXX we do not call stop() method here to do no stop the system twice.
        # exit() function will raise SystemExit exception, which will actually
        # call kernel's stop. See start() method for more information.
        self.stop()

    def banner(self):
        """Return nice BB OS banner."""
        return "BBOS Kernel v0.2.0." + \
            re.search('(\d+)', re.escape(__version__)).group(1) + ""

class Thread(OS.Object):
    """The thread is an atomic unit action within the BB
    operating system, which describes application specific actions
    wrapped into a single context of execution.

    The following example shows how to create a new thread and add it
    to the kernel::

        class Demo(Thread):
            NAME="DEMO"

            @Thread.runner
            def hello_world(self):
                print "Hello world!"

        thread = kernel.add_thread(Demo())

    Which is equivalent to::

        def hello_world():
            print "Hello world!"
        thread = kernel.add_thread(Thread("DEMO", hello_world))
    """

    # This constant keeps marked runners sorted by owner class. The content of
    # this variable is formed by decorator @runner.
    RUNNER_PER_CLASS = dict()

    def __init__(self, name=None, runner=None, port_name=None):
        """This constructor should always be called with keyword arguments.
        Arguments are:

        name is the thread name. This name should be unique within system
        threads. By default is None.

        target is callable object to be invoked by the start() method.
        Default is None, meaning nothing is called.
        """
        OS.Object.__init__(self)
        self.__name = None
        if name:
            self.set_name(name)
        elif hasattr(self, "NAME"):
            self.set_name(getattr(self, "NAME"))
        self.__commands = ()
        # Start working with runner initialization
        self.__runner = None
        if runner:
            self.set_runner(runner)
        else:
            self.__detect_runner_method()
        self.__port_name = None
        if port_name:
            self.set_port_name(port_name)

    @classmethod
    def runner(cls, runner):
        """Mark target method as thread's entry point or runner."""
        # Search for the target class to which target function belongs
        runner_cls = caller(2)
        # Save the target for a nearest future when the __init__ method will
        # we called for the target_cls class.
        Thread.RUNNER_PER_CLASS[runner_cls] = runner.__name__
        return runner

    def __detect_runner_method(self):
        # Okay, let us search for the runner in methods marked with
        # help of @runner decorator.
        cls = self.__class__
        if cls.__name__ in Thread.RUNNER_PER_CLASS:
            # Since the runner here is represented by a function it will be
            # converted to a method for a given instance. Then this method
            # will be stored as attribute 'target'.
            runner_method_name = Thread.RUNNER_PER_CLASS[cls.__name__]
            runner = getattr(self, runner_method_name)
            self.set_runner(runner)

    def set_port_name(self, name):
        # TODO: check port existance.
        self.__port_name = name

    def get_port_name(self):
        return self.__port_name

    def set_name(self, name):
        """Set the given name as thread's name."""
        self.__name = type_check.verify_string(name)

    def get_name(self):
        return self.__name

    def set_runner(self, runner):
        self.__runner = runner

    def get_runner(self):
        """Returns runner. By default returns None value."""
        return self.__runner

    def get_runner_name(self):
        """Returns name of the runner which is the function name::

            def hello_world():
                print "Hello world!"

            thread = Thread("HELLO_WORLD", hello_world)
            print thread.get_runner_name()

        As result we will have string ``hello_world``.

        By default if runner was not defined, returns ``None``.
        """
        if self.get_runner():
            return self.get_runner().__name__
        return None

    def start(self):
        """Start the thread's activity. It arranges for the object's run()
        method.
        """
        self.run()

    def run(self):
        """This method represents thread's activity. You may override this
        method in a subclass. The standard run() method invokes the callable
        object passed to the object's constructor as the target argument.
        """
        runner = self.get_runner()
        if not runner:
            raise Kernel.Exception("Runner wasn't defined")
        runner()

    # TODO(team): The following methods provide support for pickle which is
    # already obsolete. This will allow user to pickle Thread instance. Priously
    # I was trying to use this to be able copy thread instance to the file and
    # then load it. On this moment we do not use this feature. I'm still keeping
    # it here while it's not disturb me.

    def __getstate__(self):
      corrected_dict = self.__dict__.copy() # copy the dict since we change it
      if type(corrected_dict['target']) is types.MethodType:
        del corrected_dict['target']
      return corrected_dict

    def __setstate__(self, dict_):
      self.__dict__.update(dict_)
      self.__detect_runner_method()

    def __str__(self):
        """Returns a string containing a concise, human-readable
        description of this object.
        """
        return "<Thread %s>" % self.get_name()

class Message(object):
    """A message passed between threads."""
    def __init__(self, command=None, data=None, sender=None):
        self.__command = None
        self.__sender = None
        self.__data = None
        if command:
            self.set_command(command)
        self.set_sender(sender or get_running_thread().get_name())
        if data:
            self.set_data(data)
        self.__owner = self.get_sender()

    def get_owner(self):
        return self.__owner

    def set_command(self, command):
         self.__command = type_check.verify_string(command)

    def get_command(self):
        return self.__command

    def get_sender(self):
        return self.__sender

    def set_sender(self, sender):
        self.__sender = sender

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

verify_message_command = type_check.verify_string

class Messenger(Thread):
    """This class is a special form of thread, which allows to automatically
    provide an action for received message by using specified map of predefined
    handlers.

    The following example shows the most simple case how to define a new message
    handler by using :func:`Messenger.message_handler` decorator::

        class SerialMessenger(Messenger):
            @Messenger.message_handler("SERIAL_OPEN")
            def serial_open_handler(self, message):
                print "Open serial connection"

    Or the same example, but without decorator::

        class SerialMessenger(Messenger):
            def __init__(self):
                Messenger.__init__(self)
                self.add_message_handler("SERIAL_OPEN", self.serial_open_handler)

            def serial_open_handler(self, message):
                print "Open serial connection"

    When a :class:`SerialMessenger` object receives a ``SERIAL_OPEN`` message,
    the message is directed to :func:`SerialMessenger.serial_open_handler`
    handler for the actual processing.

    .. note::

      In order to privent any conflicts with already defined methods the message
      handler should be named by concatinating `_handler` postfix to the the
      name of handler, e.g. ``serial_open_handler``.
    """

    MESSAGE_HANDLERS_MAP_PER_CLASS = dict()
    PORT_NAME_FORMAT = "MESSENGER_PORT_%d"
    PORT_SIZE = 2
    COUNTER_PER_PORT_NAME_FORMAT = dict()

    def __init__(self, name=None, port_name=None, port_name_format=None,
                 port_size=None):
        Thread.__init__(self, name, port_name=port_name)
        # Define the format of port name or set default if required
        if not port_name_format:
            port_name_format = self.PORT_NAME_FORMAT
        if not port_name_format in self.COUNTER_PER_PORT_NAME_FORMAT:
            self.COUNTER_PER_PORT_NAME_FORMAT[port_name_format] = 0
        # If port name was not provided it will be generated automatically by
        # using appropriate name format
        if not port_name:
            self.COUNTER_PER_PORT_NAME_FORMAT[port_name_format] += 1
            counter = self.COUNTER_PER_PORT_NAME_FORMAT[port_name_format]
            port_name = port_name_format % counter
            if not port_size:
                port_size = self.PORT_SIZE
            get_running_kernel().add_port(Port(port_name, port_size))
        self.set_port_name(port_name)
        self.__message_handlers_map = dict()
        self.__default_message_handlers()

    def __default_message_handlers(self):
        """Set default message handlers from
        Messenger.MESSAGE_HANDLERS_BY_CLASS if such were defined."""
        cls_name = self.__class__.__name__
        if not cls_name in Messenger.MESSAGE_HANDLERS_MAP_PER_CLASS:
            return
        message_handlers_map = \
            Messenger.MESSAGE_HANDLERS_MAP_PER_CLASS[cls_name]
        for command, handler in message_handlers_map.items():
            self.add_message_handler(command, handler)

    @classmethod
    def message_handler(dec_cls, cmd):
        """A special decorator to reduce a few unnecessary steps to add a new
        message handler. See :func:`add_message_handler` for more details.
        """
        verify_message_command(cmd)
        target_cls_name = caller(2)
        if not target_cls_name in table:
            Messenger.MESSAGE_HANDLERS_MAP_PER_CLASS[target_cls_name] = dict()
        def catch_message_handler(handler):
            Messenger.MESSAGE_HANDLERS_MAP_PER_CLASS[target_cls_name][cmd] = handler
            return handler
        return catch_message_handler

    def add_message_handler(self, command, handler):
        """Maps a command extracted from a message to the specified handler
        function.
        """
        if not callable(handler):
            raise Exception("The handler %s has to be callable." % handler)
        if self.has_message_handler(command):
            print "WARNING: The handler %s of the message %s will be redefined"\
                % (self.find_message_handler(command))
        self.__message_handlers_map[command] = handler

    def get_supported_messages(self):
        """Returns a list of messages for which the messenger has handlers.
        """
        return self.__message_handlers_map.keys()

    def has_message_handler(self, command):
        """This method is alias to :func:`find_message_handler`, but it returns
        True if handler was found or ``False`` otherwise.
        """
        return not not self.find_message_handler(command)

    def find_message_handler(self, command):
        """Returns message handler if there is a handler for command,
        or ``None`` if there is no such handler.
        """
        if not command in self.get_supported_messages():
            return None
        handler = self.__message_handlers[command]
        return handler

    # TODO: create a unique runner.
    def run(self):
        """The messenger's logic."""
        message = get_running_kernel().receive_message()
        if not message:
            return
        command = message.get_command()
        handler = self.find_message_handler(command)
        if not handler:
            raise Exception("Unknown command '%s'" % command)
        handler(message)

class Driver(OS.Object, OS.Object.Metadata):
    """A BB device driver controls a hardware primitive or device, represented
    by :class:`bb.hardware.devices.device.Device`. Interaction with drivers is
    done through :class:`DriverManager`, which can be obtained via
    :func:`HardwareManagement.find_driver_manager`.

    The following example shows the most simple case how to define a
    new action handler by using :func:`Driver.action_handler` decorator::

        class SerialDriver(Driver):
            def __init__(self):
                Driver.__init__(self, "SERIAL_DRIVER")

            @Driver.action_handler("SERIAL_OPEN")
            def open_handler(self, device):
                print "Open serial connection"

    Or the same example, but without decorator::

        class SerialDriver(Driver):
            def __init__(self):
                Driver.__init__(self, "SERIAL_DRIVER")
                self.add_action_handler("SERIAL_OPEN", self.serial_open_handler)

            def serial_open_handler(self, message):
                print "Open serial connection"

    Note, in order to privent any conflicts with already defined
    methods the action handler should be named by concatinating
    ``_handler`` postfix to the the name of handler,
    e.g. ``serial_open_handler()``."""

    MESSENGER_CLASS = Messenger

    ACTION_HANDLERS_MAP_PER_CLASS = dict()

    def __init__(self, name=None, version=None):
        self.__name = None
        if name:
            self.set_name(name)
        self.__version = None
        if version:
            self.set_version(version)
        # Internal table of actions and their handlers.
        self.__action_handlers_map = dict()
        self.__default_action_handlers_map()
        self.__messenger = None
        if self.MESSENGER_CLASS:
            self.__messenger = self.MESSENGER_CLASS()

    def get_messenger(self):
        """Returns the :class:`Messenger` that controls driver activity. By
        default returns ``None`` if messenger wasn't specified.
        """
        return self.__messenger

    def __default_action_handlers_map(self):
        """Set default action handlers from
        Driver.ACTION_HANDLERS_MAP_PER_CLASS if such were defined.
        """
        cls_name = self.__class__.__name__
        # Whether we have predefined action handlers
        if not cls_name in Driver.ACTION_HANDLERS_MAP_PER_CLASS:
            return
        for action, handler in Driver.ACTION_HANDLERS_MAP_PER_CLASS[cls_name].items():
            self.add_message_handler(command, handler)

    @classmethod
    def action_handler(dec_cls, action):
        """A special decorator to reduce a few unnecessary steps to
        add a new action handler. See :func:`add_action_handler` for more
        details.
        """
        type_check.verify_string(action)
        target_cls_name = caller(2)
        if not target_cls_name in table:
            Driver.ACTION_HANDLERS_MAP_PER_CLASS[target_cls_name] = dict()
        # Define a sepcial action catcher
        def catch_action_handler(handler):
            Driver.ACTION_HANDLERS_MAP_PER_CLASS[target_cls_name][cmd] = handler
            return handler
        # Return our catcher
        return catch_action_handler

    def add_action_handler(self, action, handler):
        """Maps an action to the associated handler function."""
        if not callable(handler):
            raise Exception("Handler must be callable.")
        if self.has_action_handler(action):
            print "WARNING: A handler '%s' is already associated with "\
                                "action '%s'" % (handler, action)
        self.__action_handlers[action] = handler

    def is_supported_action(self, action):
        """Whether appropriate handler was defined for a given
        action.
        """
        return action in self.get_supported_actions()

    def get_supported_actions(self):
        return self.__action_handlers_map.keys()

    def find_action_handler(self, action):
        """Returns action handler if there is a handler for action,
        or ``None`` if there is no such handler.
        """
        if not self.is_supported_action(action):
            return None
        handler = self.__action_handlers_map[action]
        return handler

    def attach_device(self, device):
        """Called by hardware manager to query the existence of a specific
        device and whether this driver can control it.
        """
        raise NotImplementedError("Please, implement this!")

    def detach_device(self, device):
        """Called by hardware manager when the device is removed in order to
        free it from driver's (system) control.
        """
        raise NotImplementedError("Please, implement this!")

def verify_driver(driver):
    if not isinstance(driver, Driver):
        raise Exception("Expected Driver type; received %s (is %s)" %
                        (driver, driver.__class__.__name__))

class DriverManager(object):
    """This class represents an interface to interract with :class:`Driver`
    objects inside of the system.

    It is system responsibility to create and work with this manager. However
    developer may use the manager in order to define all device controled by
    particular driver.
    """

    def __init__(self, driver):
        self.__driver = None
        self.__devices = list()
        self.__set_driver(driver)

    def __set_driver(self, driver):
        """Private method used to select a driver that has to be managed by
        this manager.
        """
        #verify_driver(driver)
        self.__driver = driver

    def get_driver(self):
        """Return controled :class:`Driver` instance."""
        return self.__driver

    def add_device(self, device):
        """Add device to be controled by this :class:`Driver`."""
        verify_device(device)

    def has_device(self, device):
        pass

    def get_devices(self):
        """Return a list of all devices currently bound to the driver."""
        return self.__devices

class DeviceManager(OS.Object):
    """Every :class:`bb.hardware.devices.device.Device` in BBOS system is
    managed by an instance of this class. Device manager represents a device
    from the mapping.

    The following example shows how to register
    :class:`bb.hardware.devices.processors.propeller_p8x32.PropellerP8X32A`
    from package for kernel, which required from system to create
    :class:`DeviceManager` instance to manage this device::

        from bb.hardware.devices.processors.propeller_p8x32 import PropellerP8X32A
        device = PropellerP8X32A()
        kernel.register_device(device)
    """

    def __init__(self, device, driver=None):
        """device is a Device instance that has to be managed by this
        manager.

        driver defines a Driver instance that manages device. Please
        see Driver class."""
        OS.Object.__init__(self)
        self.__device = None
        self.__set_device(device)
        self.__driver = None
        if driver:
            self.set_driver(driver)

    def __set_device(self, device):
        verify_device(device)
        self.__device = device

    def get_device(self):
        """Return controled :class:`Device` instance."""
        return self.__device

    def set_driver(self, driver):
        """Set :class:`Driver` instance as control unit for this device."""
        verify_driver(driver)
        self.__driver = driver

    def get_driver(self):
        """Return :class:`Driver` instance that manages this device. By default
        return ``None`` value if driver was not selected.
        """
        return self.__driver

    def __str__(self):
        """Return a string containing a concise, human-readable description of
        this object.
        """
        return "Device manager of %s" % self.get_device().get_name()
