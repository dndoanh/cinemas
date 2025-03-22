import pytest

from handlers.io.console_io_handler import ConsoleIOHandler
from handlers.io.io_handler import IOHandler


@pytest.mark.parametrize("input_value, received_value", [("", ""), ("Jim", "Jim")])
def test_input(monkeypatch, input_value, received_value):
    monkeypatch.setattr("builtins.input", lambda: input_value)
    io_handler = ConsoleIOHandler()
    assert io_handler.input() == received_value


@pytest.mark.parametrize(
    "output_value, expected_output_value",
    [(None, "None\n"), ("", "\n"), ("Hello World", "Hello World\n")],
)
def test_output(capfd, output_value, expected_output_value):
    io_handler: IOHandler = ConsoleIOHandler()
    io_handler.output(output_value)
    output, err = capfd.readouterr()
    assert expected_output_value == output
