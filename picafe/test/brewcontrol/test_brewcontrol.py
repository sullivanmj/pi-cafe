import mock
import pytest

import threading
import datetime
import time
from picafe.brewcontrol import TimedBrewController


def test_timedbrewcontroller_start_brew_starts_device():
    # arrange
    mock_device_controller = mock.Mock()
    duration = mock.Mock()
    brew_controller = TimedBrewController(duration, mock_device_controller)

    # act
    brew_controller.start_brew()

    # assert
    mock_device_controller.power_on.assert_called_once()


def test_timedbrewcontroller_calls_stop_duration_after_specified_duration():
    # arrange
    mock_device_controller = mock.Mock()
    duration = datetime.timedelta(seconds=0.005)
    brew_controller = TimedBrewController(duration, mock_device_controller)

    # act
    brew_controller.start_brew()

    # assert
    mock_device_controller.power_off.assert_not_called()
    time.sleep(0.02)
    mock_device_controller.power_off.assert_called_once()


def test_timedbrewcontroller_powers_off_device():
    # arrange
    mock_device_controller = mock.Mock()
    duration = datetime.timedelta(seconds=0.001)
    brew_controller = TimedBrewController(duration, mock_device_controller)

    # act
    brew_controller.start_brew()
    time.sleep(0.02)

    # assert
    mock_device_controller.power_off.assert_called_once()


def test_timedbrewcontroller_cancel_stops_device():
    # arrange
    mock_device_controller = mock.Mock()
    duration = mock.Mock()
    brew_controller = TimedBrewController(duration, mock_device_controller)

    # act
    brew_controller.cancel_brew()

    # assert
    mock_device_controller.power_off.assert_called_once()


def test_timedbrewcontroller_cancel_cancels_timer_early():
    # arrange
    mock_device_controller = mock.Mock()
    duration = datetime.timedelta(hours=5)
    brew_controller = TimedBrewController(duration, mock_device_controller)
    time_before_cancel = datetime.datetime.now()

    # act
    brew_controller.cancel_brew()

    # assert
    mock_device_controller.power_off.assert_called_once()
    assert datetime.datetime.now() - time_before_cancel < duration
