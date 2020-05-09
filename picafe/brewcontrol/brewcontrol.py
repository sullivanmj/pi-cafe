import datetime
import picafe.brewcontrol

from .devicecontrol import PiCafeDevice

from threading import Timer

STATE_STOPPED = 0
STATE_BREWING = 1


class TimedBrewController:
    def __init__(self,
                 duration: datetime.timedelta,
                 device_controller: PiCafeDevice) -> None:
        self.timer = Timer(duration.total_seconds(), self.__stop_brew)
        self.device_controller = device_controller

    def start_brew(self) -> None:
        self.device_controller.power_on()
        self.timer.start()

    def __stop_brew(self) -> None:
        self.device_controller.power_off()

    def cancel_brew(self) -> None:
        self.__stop_brew()
        self.timer.cancel()


class TemperatureBrewController:
    def __init__(self,
                 fahrenheitTarget: float,
                 device_controller: PiCafeDevice) -> None:
        self.fahrenheitTarget = fahrenheitTarget
        self.device_controller = device_controller

    def start_brew(self) -> None:
        self.device_controller.power_on()

    def __stop_brew(self) -> None:
        self.device_controller.power_off()

    def cancel_brew(self) -> None:
        self.stop_brew()
