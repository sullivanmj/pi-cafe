"""The main script entry-point for pi-cafe."""

import sys
import typing

from picafe.brewing.heatingdevicecontrol import HeatingDevice
from picafe.brewing.heatingdevicecontrol import get_heating_devices
from picafe.brewing.brewcontrol import ManualBrewController


COLUMN_SEPARATOR = ' | '
FIRST_COLUMN_TITLE = 'index'
SECOND_COLUMN_TITLE = 'description'


def main():
    """Run a pi-cafe brew cycle.

    The brew cycle will either start the single WeMo device that it
    detects, or prompt the user to select a WeMo device if more than
    one WeMo device is detected.
    """
    print('Welcome to Pi Cafe.')

    try:
        selected_device = select_heating_device()
    except CanceledDeviceSelection:
        print('Please come again. Goodbye.')
        return
    except NoDevicesDetectedError:
        print('No devices were detected. Please ensure that a device is '
              'available.')
        return

    brew_controller = ManualBrewController(selected_device)

    input('Press ENTER to start brewing.')

    brew_controller.start_brew()

    input('Press ENTER to stop brewing.')

    brew_controller.stop_brew()

    print('Brew cycle complete.')
    print('Enjoy your beverage.')


def select_heating_device() -> HeatingDevice:
    """Select a heating device.

    If there is only one heating device detected, then that device will
    be selected. If there is more than one device, then the user will
    be prompted to select the desired device.
    """
    print('Fetching Heating devices...')

    devices = get_heating_devices()

    if len(devices) == 0:
        raise NoDevicesDetectedError
    elif len(devices) == 1:
        return devices[0]
    else:
        return get_valid_device_selection(devices)


def get_valid_device_selection(
        devices: typing.List[HeatingDevice])-> HeatingDevice:
    """

    """
    while True:
        try:
            selected_index = prompt_for_device_selection(devices)
            break
        except InvalidDeviceSelectionError:
            print(f'''Please enter a device identifier between 0 and
                      {len(devices) - 1}''')

    return devices[selected_index]


def prompt_for_device_selection(devices: typing.List[HeatingDevice]) -> int:
    """Prompt the user to select from a list of devices.

    The user can select a device by entering the index presented next
    to the device, or they can cancel by electing to not enter an
    index.
    """

    print(f'{FIRST_COLUMN_TITLE}{COLUMN_SEPARATOR}{SECOND_COLUMN_TITLE}')

    for index in range(len(devices)):
        print_device_with_index(index, devices[index])

    print()

    device_count = len(devices)

    prompt = f'Please enter your selection (0 through {device_count - 1}): '
    selection = input(prompt)

    try:
        int_selection = int(selection)
    except ValueError:
        raise InvalidDeviceSelectionError

    if int_selection < 0 or int_selection >= device_count:
        raise InvalidDeviceSelectionError

    return int_selection


def print_device_with_index(index: int, device: HeatingDevice) -> None:
    index_string = repr(index)
    index_string_length = len(index_string)
    desired_string_length = len(FIRST_COLUMN_TITLE) + len(COLUMN_SEPARATOR)
    index_string_padding = ' ' * (desired_string_length - index_string_length)

    print(f'{index_string}{index_string_padding}{device}')


def initialize_application():
    """Run the application when called as a script.

    When the module is run as a script by the python interpreter, this
    method will invoke the :function:`picafe.picafe.main` function.
    Otherwise, nothing will happen.
    """
    if __name__ == '__main__':
        sys.exit(main())


initialize_application()


class InvalidDeviceSelectionError(Exception):
    pass


class NoDevicesDetectedError(Exception):
    pass


class CanceledDeviceSelection(Exception):
    pass
