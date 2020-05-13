import abc
import datetime
import picafe.brewcontrol

from .heatingdevicecontrol import HeatingDevice

from threading import Timer

STATE_STOPPED = 0
STATE_BREWING = 1


class BrewController(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return (hasattr(subclass, 'start_brew')
                and callable(subclass.start_brew)
                and hasattr(subclass, 'cancel_brew')
                and callable(subclass.cancel_brew)
                or NotImplemented)

    @abc.abstractmethod
    def start_brew(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def cancel_brew(self) -> None:
        raise NotImplementedError


class ManualBrewController(BrewController):
    def __init__(self, device_controller: HeatingDevice) -> None:
        self.device_controller = device_controller

    def start_brew(self) -> None:
        print('Starting manual brew cycle.')
        self.device_controller.power_on()

    def stop_brew(self) -> None:
        print('Stopping manual brew cycle.')
        self.device_controller.power_off()

    def cancel_brew(self) -> None:
        self.stop_brew()


class TimedBrewController(BrewController):
    def __init__(self,
                 duration: datetime.timedelta,
                 device_controller: HeatingDevice) -> None:
        self.timer = Timer(duration.total_seconds(), self.__end_brew)
        self.device_controller = device_controller

    def start_brew(self) -> None:
        self.device_controller.power_on()
        self.timer.start()

    def __end_brew(self) -> None:
        self.device_controller.power_off()

    def cancel_brew(self) -> None:
        self.__end_brew()
        self.timer.cancel()


class TemperatureBrewController(BrewController):
    def __init__(self,
                 fahrenheitTarget: float,
                 device_controller: HeatingDevice) -> None:
        self.fahrenheitTarget = fahrenheitTarget
        self.device_controller = device_controller

    def start_brew(self) -> None:
        self.device_controller.power_on()

    def __end_brew(self) -> None:
        self.device_controller.power_off()

    def cancel_brew(self) -> None:
        self.__end_brew()
