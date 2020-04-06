import mock
import pytest


def test_init():
    from picafe import picafe
    with mock.patch.object(picafe, "main", return_value=42):
        with mock.patch.object(picafe, "__name__", "__main__"):
            with mock.patch.object(picafe.sys, 'exit') as mock_exit:
                picafe.init()
                assert mock_exit.call_args[0][0] == 42
