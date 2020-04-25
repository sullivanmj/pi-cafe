import mock
import pytest
import pywemo
from picafe.brewcontrol import devicecontrol


def test_wemodevicewrapper_gets_correct_name():
    # arrange
    mock_wemo_device = mock.Mock(pywemo.WeMoDevice)
    mock_wemo_device.name = mock.Mock()
    wemo_wrapper = devicecontrol.WemoDeviceWrapper(mock_wemo_device)

    # act
    name = wemo_wrapper.name

    # assert
    assert mock_wemo_device.name is name


def test_wemodevicewrapper_turn_on_turns_on_device_when_off():
    mock_wemo_device = mock.Mock(pywemo.WeMoDevice)
    on_func = mock.Mock()
    mock_wemo_device.on = on_func
    get_state_func = mock.Mock(return_value=devicecontrol.STATE_OFF)
    mock_wemo_device.get_state = get_state_func
    wemo_wrapper = devicecontrol.WemoDeviceWrapper(mock_wemo_device)

    wemo_wrapper.power_on()

    on_func.assert_called_once()


def test_wemodevicewrapper_turn_on_does_nothing_when_on():
    mock_wemo_device = mock.Mock(pywemo.WeMoDevice)
    on_func = mock.Mock()
    mock_wemo_device.on = on_func
    mock_wemo_device.get_state = mock.Mock(return_value=devicecontrol.STATE_ON)
    wemo_wrapper = devicecontrol.WemoDeviceWrapper(mock_wemo_device)

    wemo_wrapper.power_on()

    on_func.assert_not_called()


def test_wemodevicewrapper_turn_off_turns_off_device_when_on():
    mock_wemo_device = mock.Mock(pywemo.WeMoDevice)
    off_func = mock.Mock()
    mock_wemo_device.off = off_func
    mock_wemo_device.get_state = mock.Mock(return_value=devicecontrol.STATE_ON)
    wemo_wrapper = devicecontrol.WemoDeviceWrapper(mock_wemo_device)

    wemo_wrapper.power_off()

    off_func.assert_called_once()


def test_wemodevicewrapper_turn_off_does_nothing_when_off():
    mock_wemo_device = mock.Mock(pywemo.WeMoDevice)
    off_func = mock.Mock()
    mock_wemo_device.off = off_func
    get_state_func = mock.Mock(return_value=devicecontrol.STATE_OFF)
    mock_wemo_device.get_state = get_state_func
    wemo_wrapper = devicecontrol.WemoDeviceWrapper(mock_wemo_device)

    wemo_wrapper.power_off()

    off_func.assert_not_called()
