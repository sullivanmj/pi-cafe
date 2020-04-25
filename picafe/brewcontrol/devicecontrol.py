import pywemo

STATE_OFF = 0
STATE_ON = 1


def get_devices():
    all_devices = []
    pywemo_devices = pywemo.discover_devices()

    for pywemo_device in pywemo_devices:
        pywemo_wrapper = wrap_wemo_device(pywemo_device)
        all_devices.append(pywemo_wrapper)


def wrap_wemo_device(pywemo_device):
    return WemoDeviceWrapper(pywemo_device)


class WemoDeviceWrapper:
    def __init__(self, pywemo_device):
        self.pywemo_device = pywemo_device

    @property
    def name(self):
        return self.pywemo_device.name

    def power_on(self):
        if (self.pywemo_device.get_state() == STATE_OFF):
            self.pywemo_device.on()

    def power_off(self):
        if (self.pywemo_device.get_state() == STATE_ON):
            self.pywemo_device.off()
