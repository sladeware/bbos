
from bb.hardware.device import Device
from bb.hardware.core import Core
from bb.utils.type_check import verify_list, is_list, is_dict

class Processor(Device):
    """Base class used for creating a BBOS processor.

    A processor contains one or more cores. It is a discrete semiconductor
    based device used for computation. For example, the PIC32MX5
    microcontroller is a processor."""

    def __init__(self, name, num_cores=0, cores=None):
        Device.__init__(self, name)
        if num_cores < 1:
            raise NotImplemented("Number of cores must be more than zero.")
        self.__num_cores = num_cores
        self.__cores = {}
        if cores:
            self.set_cores(cores)
        self.__owner = None

    def power_on(self):
        """Power on processor and its cores one by one."""
        for id, core in self.get_cores():
            core.power_on()

    def set_cores(self, cores):
        """Set a bunch of cores at once. The set of cores can be represented by
        a list (in this case processor's position in this list will be its ID)
        and by a dict (the key represents processor's ID and value - processor's
        instance)."""
        if is_list(cores) and len(cores):
            for i in range(len(cores)):
                self.set_core(cores[i], i)
        elif is_dict(cores) and len(cores):
            for id, core in cores.items():
                self.set_core(core, id)

    def set_core(self, core, id):
        """Set a processor's core associated with specified identifier. If the
        core with such ID is already presented, it will be replaced."""
        if not isinstance(core, Core):
            raise TypeError('core "%s" must be bb.os.Core sub-clas' % core)
        self.validate_core(core)
        self.validate_core_id(id)
        self.__cores[id] = core
        core.set_owner(self)

    def get_core(self, id=0):
        """Get processor's core. If core's ID is not selected, will be returned
        the first core with 0 ID."""
        self.validate_core_id(id)
        return self.__cores[id]

    def validate_core(self, core):
        if not self.is_valid_core(core):
            raise NotImplemented

    def is_valid_core(self, core):
        return True

    def validate_core_id(self, i):
        if self.get_num_cores() <= i:
            raise NotImplemented('The %s supports up to %d cores. '
                                 'You have too many: %d' %
                                 (self.__class__.__name__,
                                  self.get_num_cores(), i))

    def get_cores(self):
        return self.__cores.items()

    def get_num_cores(self):
        return self.__num_cores

    def get_mappings(self):
        mappings = []
        for core in self.get_cores():
            if not core:
              continue
            mappings.append(core.get_mapping())
        return mappings
