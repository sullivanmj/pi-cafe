"""The main script entry-point for pi-cafe."""

import sys


def main():
    """Run a pi-cafe brew cycle.

    The brew cycle will either start the single WeMo device that it
    detects, or prompt the user to select a WeMo device if more than
    one WeMo device is detected.
    """
    print('Welcome to Pi Cafe.')
    print('Starting brew cycle.')


def initialize_application():
    """Run the application when called as a script.

    When the module is run as a script by the python interpreter, this
    method will invoke the :function:`picafe.picafe.main` function.
    Otherwise, nothing will happen.
    """
    if __name__ == '__main__':
        sys.exit(main())


initialize_application()
