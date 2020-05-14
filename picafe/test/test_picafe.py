import mock
import pytest


def test_initialize_application_calls_main():
    from picafe import __main__
    with mock.patch.object(__main__, "main", return_value=42):
        with mock.patch.object(__main__, "__name__", "__main__"):
            with mock.patch.object(__main__.sys, 'exit') as mock_exit:
                __main__.initialize_application()
                assert mock_exit.call_args[0][0] == 42
