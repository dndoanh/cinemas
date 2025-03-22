import pytest

from handlers.cinema_handler import CinemaHandler


def test_invalid_movie_title_rows_seats_per_row(monkeypatch, capfd):
    inputs = iter(["Inception810", "Inception 8 10", "3"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    handler = CinemaHandler()
    expected_output = "Invalid movie title or rows or seats per row. Please try again."
    handler.start()
    output, err = capfd.readouterr()
    assert expected_output in output


def test_invalid_menu_selection(monkeypatch, capfd):
    inputs = iter(["Inception 8 10", "5", "3"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    handler = CinemaHandler()
    expected_output = "Invalid menu selection. Please try again."
    handler.start()
    output, err = capfd.readouterr()
    assert expected_output in output


def test_invalid_number_of_tickets(monkeypatch, capfd):
    inputs = iter(["Inception 8 10", "1", "A12", "4", "", "3"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    handler = CinemaHandler()
    expected_output = "Invalid number of tickets. Please try again."
    handler.start()
    output, err = capfd.readouterr()
    assert expected_output in output


def test_exit_without_booking_any_ticket(monkeypatch, capfd):
    inputs = iter(["Inception 8 10", "1", "", "3"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    handler = CinemaHandler()
    expected_output = "Welcome to GIC Cinemas"
    handler.start()
    output, err = capfd.readouterr()
    assert output.count(expected_output) == 2


@pytest.mark.parametrize("seating_position", ["   ", "B500"])
def test_invalid_seating_position(monkeypatch, capfd, seating_position):
    inputs = iter(["Inception 8 10", "1", "4", seating_position, "", "3"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    handler = CinemaHandler()
    expected_output = "Invalid seating position. Please try again."
    handler.start()
    output, err = capfd.readouterr()
    assert expected_output in output


@pytest.mark.parametrize(
    "booking_id, expected_output",
    [
        ("   ", "Invalid booking id. Please try again."),
        ("ABC5000", "Booking id [ABC5000] does not exist. Please try again."),
    ],
)
def test_invalid_booking_id(monkeypatch, capfd, booking_id, expected_output):
    inputs = iter(["Inception 8 10", "1", "4", "", "2", booking_id, "", "3"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    handler = CinemaHandler()
    handler.start()
    output, err = capfd.readouterr()
    assert expected_output in output
