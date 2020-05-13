"""The main script entry-point for pi-cafe."""

import sys
import picafe.brewcontrol.heatingdevicecontrol as heatingdevicecontrol
import picafe.brewcontrol.brewcontrol


def main():
    """Run a pi-cafe brew cycle.

    The brew cycle will either start the single WeMo device that it
    detects, or prompt the user to select a WeMo device if more than
    one WeMo device is detected.
    """
    print('Welcome to Pi Cafe.')

    selected_device = select_heating_device()
    brew_controller = picafe.brewcontrol.brewcontrol.ManualBrewController(
        selected_device)

    brew_controller.start_brew()

    input('Press ENTER to stop brewing.')

    brew_controller.stop_brew()

    print('Brew cycle complete.')
    print('Enjoy your beverage.')

def select_heating_device() -> heatingdevicecontrol.HeatingDevice:
    """Select a heating device.

    If there is only one heating device detected, then that device will
    be selected. If there is more than one device, then the user will
    be prompted to select the desired device.
    """
    devices = heatingdevicecontrol.get_heating_devices()

    if devices.count() == 0:
        return None
    elif devices.count() == 1:
        return devices[0]
    else:
        return prompt_user_to_select_device(devices)


def prompt_user_to_select_device(
    devices: List[heatingdevicecontrol.HeatingDevice]) \
        -> heatingdevicecontrol.HeatingDevice:
    """Prompt the user to select from a list of devices.

    The user can select a device by entering the index presented next
    to the device, or they can cancel by electing to not enter an
    index.
    """
    pass


def initialize_application():
    """Run the application when called as a script.

    When the module is run as a script by the python interpreter, this
    method will invoke the :function:`picafe.picafe.main` function.
    Otherwise, nothing will happen.
    """
    if __name__ == '__main__':
        sys.exit(main())


initialize_application()


class NoDeviceSelectedError(Exception):
    pass
