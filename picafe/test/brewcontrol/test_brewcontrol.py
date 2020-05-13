import mock
import pytest

import threading
import datetime
import time

from picafe.brewcontrol import ManualBrewController
from picafe.brewcontrol import TimedBrewController
from picafe.brewcontrol import HeatingDevice


class TestTimedBrewController:
    def test_start_brew_starts_device(self):
        # arrange
        mock_device_controller = mock.Mock(HeatingDevice)
        duration = datetime.timedelta(0)
        brew_controller = TimedBrewController(duration, mock_device_controller)

        # act
        brew_controller.start_brew()

        # assert
        mock_device_controller.power_on.assert_called_once()

    def test_device_is_not_stopped_before_specified_duration(self):
        # arrange
        mock_device_controller = mock.Mock(HeatingDevice)
        duration = datetime.timedelta(seconds=0.005)
        brew_controller = TimedBrewController(duration, mock_device_controller)

        # act
        brew_controller.start_brew()

        # assert
        mock_device_controller.power_off.assert_not_called()
        time.sleep(0.02)
        mock_device_controller.power_off.assert_called_once()

    def test_device_is_stopped_after_specified_duration(self):
        # arrange
        mock_device_controller = mock.Mock(HeatingDevice)
        duration = datetime.timedelta(seconds=0.001)
        brew_controller = TimedBrewController(duration, mock_device_controller)

        # act
        brew_controller.start_brew()
        time.sleep(0.02)

        # assert
        mock_device_controller.power_off.assert_called_once()

    def test_cancel_stops_device(self):
        # arrange
        mock_device_controller = mock.Mock(HeatingDevice)
        duration = datetime.timedelta(seconds=5)
        brew_controller = TimedBrewController(duration, mock_device_controller)
        start_time = datetime.datetime.now()

        # act
        brew_controller.cancel_brew()

        # assert
        mock_device_controller.power_off.assert_called_once()
        # ensure the test is valid
        assert datetime.datetime.now() - duration < start_time


class TestManualBrewController:
    def test_start_starts_device(self):
        # arrange
        mock_device_controller = mock.Mock(HeatingDevice)
        duration = datetime.timedelta(0)
        brew_controller = ManualBrewController(mock_device_controller)

        # act
        brew_controller.start_brew()

        # assert
        mock_device_controller.power_on.assert_called_once()

    def test_cancel_stops_device(self):
        # arrange
        mock_device_controller = mock.Mock(HeatingDevice)
        brew_controller = ManualBrewController(mock_device_controller)

        # act
        brew_controller.cancel_brew()

        # assert
        mock_device_controller.power_off.assert_called_once()

    def test_stop_stops_device(self):
        # arrange
        mock_device_controller = mock.Mock(HeatingDevice)
        brew_controller = ManualBrewController(mock_device_controller)

        # act
        brew_controller.stop_brew()

        # assert
        mock_device_controller.power_off.assert_called_once()
