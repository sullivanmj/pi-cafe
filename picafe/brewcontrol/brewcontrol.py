from datetime import datetime
from datetime import timezone
from threading import Timer

STATE_STOPPED = 0
STATE_BREWING = 1


class TimedBrewController:
    def __init__(self, duration, device_controller):
        self.timer = Timer(duration, self.stop_brew)
        self.device_controller = device_controller

    def start_brew(self):
        self.stop_time = datetime.now(timezone.utc) + self.duration
        self.device_controller.power_on()
        self.timer.start()

    def stop_brew(self):
        self.device_controller.power_off()

    def cancel_brew(self):
        self.stop_brew()
        self.timer.cancel()


class TemperatureBrewController:
    def __init__(self, fahrenheitTarget, device_controller):
        self.fahrenheitTarget = fahrenheitTarget
        self.device_controller = device_controller

    def start_brew(self):
        self.device_controller.power_on()

    def stop_brew(self):
        pass

    def cancel_brew(self):
        self.stop_brew()
