import abc
from typing import List
import pywemo

STATE_OFF = 0
STATE_ON = 1


class HeatingDevice(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return (hasattr(subclass, 'name')
                and callable(subclass.name)
                and hasattr(subclass, 'power_on')
                and callable(subclass.power_on)
                and hasattr(subclass, 'power_off')
                and callable(subclass.power_off)
                or NotImplemented)

    @abc.abstractproperty
    def name(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def power_on(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def power_off(self) -> None:
        raise NotImplementedError


def get_heating_devices() -> List[HeatingDevice]:
    return get_wemo_devices()


class WemoDeviceWrapper(HeatingDevice):
    def __init__(self, pywemo_device: pywemo.WeMoDevice) -> None:
        self.pywemo_device = pywemo_device

    @property
    def name(self) -> str:
        return self.pywemo_device.name

    def power_on(self) -> None:
        if (self.pywemo_device.get_state() == STATE_OFF):
            self.pywemo_device.on()

    def power_off(self) -> None:
        if (self.pywemo_device.get_state() == STATE_ON):
            self.pywemo_device.off()


def wrap_wemo_device(pywemo_device: pywemo.WeMoDevice) -> WemoDeviceWrapper:
    return WemoDeviceWrapper(pywemo_device)


def get_wemo_devices() -> List[WemoDeviceWrapper]:
    devices = []
    pywemo_devices = pywemo.discover_devices()

    for pywemo_device in pywemo_devices:
        pywemo_wrapper = wrap_wemo_device(pywemo_device)
        devices.append(pywemo_wrapper)

    return devices
