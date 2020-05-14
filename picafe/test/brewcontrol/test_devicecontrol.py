import mock
import pytest
import pywemo
from picafe.brewing import heatingdevicecontrol


def test_getdevices_wraps_each_pywemo_device_with_wemodevicewrapper():
    # arrange
    mock_wemo_device_1 = mock.Mock(pywemo.WeMoDevice)
    mock_wemo_device_2 = mock.Mock(pywemo.WeMoDevice)
    mock_wemo_device_3 = mock.Mock(pywemo.WeMoDevice)
    mock_devices = [mock_wemo_device_1, mock_wemo_device_2, mock_wemo_device_3]
    pywemo.discover_devices = mock.Mock(return_value=mock_devices)

    # act
    devices = heatingdevicecontrol.get_heating_devices()

    # assert
    pywemo.discover_devices.assert_called_once()

    assert all(device.pywemo_device in mock_devices for device in devices)
    assert devices.__len__() == mock_devices.__len__()


def test_wemodevicewrapper_gets_correct_name():
    # arrange
    mock_wemo_device = mock.Mock(pywemo.WeMoDevice)
    mock_wemo_device.name = mock.Mock()
    wemo_wrapper = heatingdevicecontrol.WemoDeviceWrapper(mock_wemo_device)

    # act
    name = wemo_wrapper.name

    # assert
    assert mock_wemo_device.name is name


def test_wemodevicewrapper_turn_on_turns_on_device_when_off():
    # arrange
    mock_wemo_device = mock.Mock(pywemo.WeMoDevice)
    on_func = mock.Mock()
    mock_wemo_device.on = on_func
    get_state_func = mock.Mock(return_value=heatingdevicecontrol.STATE_OFF)
    mock_wemo_device.get_state = get_state_func
    wemo_wrapper = heatingdevicecontrol.WemoDeviceWrapper(mock_wemo_device)

    # act
    wemo_wrapper.power_on()

    # assert
    on_func.assert_called_once()


def test_wemodevicewrapper_turn_on_does_nothing_when_on():
    # arrange
    mock_wemo_device = mock.Mock(pywemo.WeMoDevice)
    on_func = mock.Mock()
    mock_wemo_device.on = on_func
    mock_wemo_device.get_state = mock.Mock(
        return_value=heatingdevicecontrol.STATE_ON)
    wemo_wrapper = heatingdevicecontrol.WemoDeviceWrapper(mock_wemo_device)

    # act
    wemo_wrapper.power_on()

    # assert
    on_func.assert_not_called()


def test_wemodevicewrapper_turn_off_turns_off_device_when_on():
    # arrange
    mock_wemo_device = mock.Mock(pywemo.WeMoDevice)
    off_func = mock.Mock()
    mock_wemo_device.off = off_func
    mock_wemo_device.get_state = mock.Mock(
        return_value=heatingdevicecontrol.STATE_ON)
    wemo_wrapper = heatingdevicecontrol.WemoDeviceWrapper(mock_wemo_device)

    # act
    wemo_wrapper.power_off()

    # assert
    off_func.assert_called_once()


def test_wemodevicewrapper_turn_off_does_nothing_when_off():
    # arrange
    mock_wemo_device = mock.Mock(pywemo.WeMoDevice)
    off_func = mock.Mock()
    mock_wemo_device.off = off_func
    get_state_func = mock.Mock(return_value=heatingdevicecontrol.STATE_OFF)
    mock_wemo_device.get_state = get_state_func
    wemo_wrapper = heatingdevicecontrol.WemoDeviceWrapper(mock_wemo_device)

    # act
    wemo_wrapper.power_off()

    # assert
    off_func.assert_not_called()
