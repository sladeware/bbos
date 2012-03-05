#!/usr/bin/env python

class BoardConfig(object):
    def get_eeprom_size(self):
        return self.EEPROM_SIZE

    def get_baudrate(self):
        return self.BAUDRATE

class DemoBoardConfig(BoardConfig):
    BAUDRATE = 115200
    EEPROM_SIZE = 32768

class QuickStartBoardConfig(BoardConfig):
    BAUDRATE = 115200
    EEPROM_SIZE = 32768

class CustomBoardConfig(BoardConfig):
    EEPROM_SIZE = 32768
    # Baud rate to use for all interprop communications
    BAUDRATE = 115200

class Config(object):

    class Action(object):
        """Describes information about a command line action."""
        def __init__(self, function, usage, short_desc, long_desc='',
                     error_desc=None, options=lambda obj, parser: None,
                     uses_basepath=True):
            """Initializer for the class attributes."""
            self.function = function
            self.usage = usage
            self.short_desc = short_desc
            self.long_desc = long_desc
            self.error_desc = error_desc
            self.options = options
            self.uses_basepath = uses_basepath

        def __call__(self, cfg):
            """Invoke this Action on the specified Config.

            This calls the function of the appropriate name on Config, and
            respects polymophic overrides.

            Returns the result of the function call."""
            #method = getattr(cfg, self.function)
            #return method()
            return self.function(cfg)

    actions = dict()

    @classmethod
    def action(cls, name, **kargs):
        def action_catcher(function):
            cls.actions[name] = Config.Action(function, **kargs)
            return function
        return action_catcher

    def __init__(self, argv):
        """Initializer. Parses the command line and selects the action
        to use."""
        self.argv = argv
        self.parser = self.__get_option_parser()
        self.parser.disable_interspersed_args()
        # Copy supported actions
        self.actions = Config.actions

        #for action in self.actions.itervalues():
        #    action.options(self, self.parser)

        self.options, self.args = self.parser.parse_args(argv[1:])
        if len(self.args) < 1:
            self.print_help_and_exit()

        # Parse action
        action = self.args.pop(0)
        if action not in self.actions:
            self.parser.error("Unknown action: '%s'\n%s" %
                              (action, self.parser.get_description()))
        self.action = self.actions[action]

        if self.options.help:
            self.print_help_and_exit()

        self.parser, self.options = self.action_related_parser(self.action)

        if self.options.help:
            self.print_help_and_exit()

        if self.options.output_file:
            if os.path.exists(self.options.output_file):
                os.remove(self.options.output_file)
            hdlr = logging.FileHandler(self.options.output_file)
            logging.getLogger().addHandler(hdlr)
        else:
            logging.getLogger().addHandler(logging.NullHandler())
        # Setup logging level
        logging.getLogger().setLevel(logging.DEBUG)

        # Execute required action
        self.action(self)

    def action_related_parser(self, action):
        """Creates parser with documentation specific to 'action'."""
        parser = self.__get_option_parser()
        parser.set_usage(action.usage)
        parser.set_description('%s\n%s' % (action.short_desc, action.long_desc))
        action.options(self, parser)
        options, self.args = parser.parse_args(self.args) # XXX
        return parser, options

    def print_help_and_exit(self, exit_code=2):
        self.parser.print_help()
        sys.exit(exit_code)

    def get_action_descriptions(self):
        """Returns a formatted string containing the short_descs for all actions."""
        action_names = self.actions.keys()
        action_names.sort()
        desc = ''
        for action_name in action_names:
            desc += '  %s: %s\n' % (action_name, self.actions[action_name].short_desc)
        return desc

    def __get_option_parser(self):

        class Formatter(optparse.IndentedHelpFormatter):
            """Custom help formatter that does not reformat the description."""

            def format_description(self, description):
                """Very simple formatter."""
                return description + '\n'

        desc = self.get_action_descriptions()
        desc = ('Action must be one of:\n%s'
                'Use \'help <action>\' for a detailed description.') % desc

        parser = optparse.OptionParser(
            prog=os.path.basename(self.argv[0]),
            usage="%prog [options] <action>",
            description=desc,
            formatter=Formatter(),
            add_help_option=False,
            )
        parser.add_option("-h", "--help", action="store_true", dest='help',
                          help="Show this help message and exit.")
        parser.add_option("-o", "--output-file", action="store",
                          dest="output_file",
                          help="Log message to file.")
        return parser

class ActionOptions(object):
    @classmethod
    def upload_options(cls, cfg, parser):
        parser.add_option("-s", "--serial-port", dest="serial_port", nargs=1,
                          type="string", metavar="DEVICE",
                          default=DEFAULT_SERIAL_PORTS.get(os.name, "none"),
                          help="Select the serial port device. The default is %default.")

    @classmethod
    def multicog_spi_upload_options(cls, cfg, parser):
        cls.upload_options(cfg, parser)
        for cogid in range(1, PropellerP8X32.NR_COGS + 1):
            parser.add_option("-%d" % cogid, "--cog%d" % cogid,
                              dest="cog%d" % cogid, nargs=1, type="string",
                              metavar="filename", default=None,
                              help="Select filename to be loaded. The default is %default.")

@Config.action('dump_header',
               usage="",
               short_desc='Dump header information for binary file.',
               uses_basepath=False)
def dump_header(cfg, run_fn=None):
    # http://forums.parallax.com/showthread.php?117526-eeprom-file-format
    fname = cfg.args.pop(0)
    print "Binary file : %s" % fname
    fh = open(fname)
    data = ''.join(fh.readlines())
    print "Size        : %d (bytes)" % len(data)
    hdr = None
    if fname.endswith(".elf"):
        hdr = ElfHeader()
        memmove(addressof(hdr), data, sizeof(ElfHeader))
    else:
        hdr = SpinHeader()
        memmove(addressof(hdr), data, sizeof(SpinHeader))
    print str(hdr)
    fh.close()
    exit(0)

@Config.action('help', usage='%prog help <action>',
               short_desc='Print help for a specific action.',
               uses_basepath=False)
def help(cfg, action=None):
    """Prints help for a specific action.

    Expects cfg.args[0], or 'action', to contain the name of the action in
    question. Exits the program after printing the help message."""
    if not action:
        if len(cfg.args) != 1 or cfg.args[0] not in cfg.actions:
            cfg.parser.error('Expected a single action argument. ' +
                             'Must be one of:\n' +
                             cfg.get_action_descriptions())
        action = cfg.args[0]
    action = cfg.actions[action]
    cfg.parser, unused_options = cfg.action_related_parser(action)
    cfg.print_help_and_exit(exit_code=0)

@Config.action('extract_binary_image',
               usage="",
               short_desc='Extract binary image from ELF.',
               uses_basepath=False)
def extract_binary_image(cfg, run_fn=None):
    src_fname = cfg.args.pop(0)
    dst_fname = cfg.args.pop(0)

    print "Source file: %s (%d bytes)" % (src_fname, os.path.getsize(src_fname))

    ctx = ElfContext(src_fname)
    (start, image_size) = ctx.get_program_size()
    print "Image start: 0x%08x" % start
    print "Image size: %d byte(s)" % image_size

    image_buf = [chr(0)] * image_size

    # load each program section
    for i in range(ctx.hdr.phnum):
        program = ctx.load_program_table_entry(i)
        if not program:
            print "Can not load program table entry %d" % i
        print "Load program table entry", i
        print str(program)
        buf = ctx.load_program_segment(program)
        if not buf:
            print "Can not load program section %d" % i
        for j in range(program.filesz):
            image_buf[program.paddr - start + j] = buf[j]

    # fixup the header to point past the spin bytecodes and generated PASM code
    #hdr = SpinHeader()
    #memmove(addressof(hdr), ''.join(image_buf), sizeof(SpinHeader))
    #print  hdr.clk_speed
    #hdr.vbase = image_size #Word.split_by_bytes(image_size)
    #hdr.dbase = image_size + 2 * 4 #Word.split_by_bytes(image_size + 2 * 4) # stack markers
    #hdr.dcurr = hdr.dbase + 4 #Word.split_by_bytes(hdr.dbase + 4)
    #image_buf = list(hdr) + image_buf[sizeof(SpinHeader):]

    img = ''.join(image_buf)
    x = c_char_p(img)
    hdr_p = cast(x, POINTER(SpinHeader))
    hdr_p.contents.vbase = image_size
    print hdr_p.contents.clk_speed
    hdr_p.contents.dbase = image_size + 2 * 4
    hdr_p.contents.dcurr = hdr_p.contents.dbase + 4

    print "Writing image to the destination file:", dst_fname
    dst_fh = open(dst_fname, "w")
    dst_fh.write(img)#"".join(image_buf))
    dst_fh.close()

@Config.action('edit_header',
               usage="",
               short_desc='Edit header information for binary file.',
               uses_basepath=False)
def edit_header(cfg, run_fn=None):
    pass

@Config.action('image_size',
               usage="",
               short_desc="Get image size.",
               uses_basepath=False)
def image_size(cfg, run_fn=None):
    pass



@Config.action('spi_upload',
               usage="",
               options=ActionOptions.upload_options,
               short_desc="Upload binary image.",
               uses_basepath=False)
def upload(cfg, run_fh=None):
    filenames = cfg.args
    assert len(filenames)
    # Select and read the file to be uploaded
    filename = filenames[0]
    fdata = None
    fh = open(filename, "rb")
    try:
        fdata = fh.read()
    finally:
        fh.close()
    # Instanciate uploader and connect to the target device
    uploader = StandardSPIUploader(port=cfg.options.serial_port)
    try:
        uploader.connect()
        uploader.upload(data=fdata)
    except (SystemExit, KeyboardInterrupt):
        print "Process has been interrupted"
        pass
    except Exception, e:
        print e
        exit(0)
    finally:
        uploader.disconnect()
    exit(0)

@Config.action('multicog_spi_upload',
               usage='%prog [options] multicog_spi_upload <filename>',
               options=ActionOptions.multicog_spi_upload_options,
               short_desc='Upload binary images, each for specific cog.',
               long_desc="""
The 'multicog_spi_upload' command uploads binary images to specific cogs.""",
               uses_basepath=False)
def multicog_spi_upload(cfg, run_fn=None):
    # Start process filenames and cogs.
    # Loading of equal binaries to different cogs is allowed.
    filenames = cfg.args
    free_cogs = range(1, PropellerP8X32.NR_COGS + 1)
    cogid_to_filename_mapping = dict()
    # Start process mappings from command line options
    for cogid in range(1, PropellerP8X32.NR_COGS + 1):
        filename = getattr(cfg.options, "cog%d" % cogid, None)
        if filename:
            cogid_to_filename_mapping[cogid] = filename
            free_cogs.remove(cogid)
    # Process filenames without specified cog id's
    if len(filenames) > len(free_cogs):
        print "Too many filenames."
        exit(0)
    for i in range(len(filenames)):
        if not os.path.exists(filenames[i]):
            raise Exception("File %s doesn't exist." % filenames[i])
        cogid_to_filename_mapping[free_cogs[i]] = filenames[i]
    multicog_spi_upload(cogid_to_filename_mapping, cfg.options.serial_port)
