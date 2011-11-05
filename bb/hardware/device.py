

from bb.utils.distribution import DistributionMetadata

class Device(DistributionMetadata):
    """Every device in BBOS system is represented by an instance of this class.

    name is a string that uniquely identifies this device.

    driver defines a driver instance that manages this device. Please see Driver
    class."""
    NAME_FORMAT = "DEVICE_%d"
    COUNTER_PER_NAME_FORMAT = dict()

    def __init__(self, name=None, driver=None):
        if not name:
            name_format = self.NAME_FORMAT
            if not name_format in Device.COUNTER_PER_NAME_FORMAT:
                Device.COUNTER_PER_NAME_FORMAT[name_format] = 1
            counter = Device.COUNTER_PER_NAME_FORMAT[name_format]
            name = name_format % counter
            Device.COUNTER_PER_NAME_FORMAT[name_format] += 1
        DistributionMetadata.__init__(self, name)

    def power_on(self):
        raise NotImplemented("What the device should do when the power is on?")

    def power_off(self):
        raise NotImplemented()

    def get_owner(self):
        return self.__owner

    def set_owner(self, owner):
        self.__owner = owner
