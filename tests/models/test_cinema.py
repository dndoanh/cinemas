import pytest

import utils.constants as consts
from models.cinema import Cinema


@pytest.mark.parametrize("movie_title, rows, seats_per_row", [("Inception", 8, 10)])
def test_initialization(movie_title, rows, seats_per_row):
    cinema = Cinema(movie_title, rows, seats_per_row)
    assert isinstance(cinema, Cinema)
    assert cinema.movie_title == movie_title
    assert cinema.rows == rows
    assert cinema.seats_per_row == seats_per_row
    assert cinema.available_seats == rows * seats_per_row
    assert cinema.last_booking_number == 0
    assert cinema.bookings == []
    assert cinema.processing_mode is None
    assert cinema.current_booking is None
    assert cinema.current_checking is None
    for row in range(rows):
        for col in range(seats_per_row):
            col_str = f"0{col+1}"
            col_str = col_str[len(col_str) - 2 :]
            key = f"{consts.ALPHABET_LIST[row]}{col_str}"
            assert key in cinema.index_map
            assert cinema.index_map[key] == (row, col)


@pytest.mark.parametrize("movie_title, rows, seats_per_row", [("Inception", 8, 10)])
def test_start_booking(movie_title, rows, seats_per_row):
    cinema = Cinema(movie_title, rows, seats_per_row)
    cinema.start_booking()
    assert cinema.processing_mode == "Booking_Mode"


@pytest.mark.parametrize(
    "movie_title, rows, seats_per_row",
    [
        (
            "Inception",
            8,
            10,
        )
    ],
)
def test_exit_processing(movie_title, rows, seats_per_row):
    cinema = Cinema(movie_title, rows, seats_per_row)
    cinema.start_checking()
    assert cinema.processing_mode == "Checking_Mode"
    cinema.exit_processing()
    assert cinema.processing_mode is None


@pytest.mark.parametrize(
    "cinema, num_seats, booking_id, screen_display",
    [
        (
            Cinema("Inception", 8, 10),
            4,
            "GIC0001",
            [
                "Selected seats:",
                "S C R E E N",
                "H . . . . . . . . . .",
                "G . . . . . . . . . .",
                "F . . . . . . . . . .",
                "E . . . . . . . . . .",
                "D . . . . . . . . . .",
                "C . . . . . . . . . .",
                "B . . . . . . . . . .",
                "A . . . o o o o . . .",
                "  1 2 3 4 5 6 7 8 9 10",
            ],
        )
    ],
)
def test_create_default_booking(cinema, num_seats, booking_id, screen_display):
    cinema.create_default_booking(num_seats)
    assert cinema.current_booking.booking_id == booking_id
    assert cinema.current_booking.status == consts.BOOKING_STATUS_RESERVED
    assert len(cinema.current_booking.seats) == num_seats
    assert all(seat.state == consts.SEAT_STATE_RESERVED for seat in cinema.current_booking.seats)
    display_str = cinema.screen_display()
    for line in screen_display:
        assert line in display_str


@pytest.mark.parametrize(
    "cinema, num_seats, start_position, booking_id, screen_display",
    [
        (
            Cinema("Inception", 8, 10),
            4,
            "B03",
            "GIC0001",
            [
                "Selected seats:",
                "S C R E E N",
                "H . . . . . . . . . .",
                "G . . . . . . . . . .",
                "F . . . . . . . . . .",
                "E . . . . . . . . . .",
                "D . . . . . . . . . .",
                "C . . . . . . . . . .",
                "B . . o o o o . . . .",
                "A . . . . . . . . . .",
                "  1 2 3 4 5 6 7 8 9 10",
            ],
        )
    ],
)
def test_change_seat_position(cinema, num_seats, start_position, booking_id, screen_display):
    cinema.create_default_booking(num_seats)
    cinema.change_seat_position(start_position)
    assert cinema.current_booking.booking_id == booking_id
    assert cinema.current_booking.status == consts.BOOKING_STATUS_RESERVED
    assert len(cinema.current_booking.seats) == num_seats
    assert all(seat.state == consts.SEAT_STATE_RESERVED for seat in cinema.current_booking.seats)
    display_str = cinema.screen_display()
    for line in screen_display:
        assert line in display_str


@pytest.mark.parametrize(
    "cinema, num_seats, booking_id, screen_display",
    [
        (
            Cinema("Inception", 8, 10),
            4,
            "GIC0001",
            [
                "Selected seats:",
                "S C R E E N",
                "H . . . . . . . . . .",
                "G . . . . . . . . . .",
                "F . . . . . . . . . .",
                "E . . . . . . . . . .",
                "D . . . . . . . . . .",
                "C . . . . . . . . . .",
                "B . . # # # # . . . .",
                "A . . . . . . . . . .",
                "  1 2 3 4 5 6 7 8 9 10",
            ],
        )
    ],
)
def test_confirm_booking(cinema, num_seats, booking_id, screen_display):
    cinema.create_default_booking(num_seats)
    cinema.confirm_booking()
    assert cinema.bookings[0].booking_id == booking_id
    assert cinema.bookings[0].status == consts.BOOKING_STATUS_CONFIRMED
    assert len(cinema.bookings[0].seats) == num_seats
    assert all(seat.state == consts.SEAT_STATE_BOOKED for seat in cinema.bookings[0].seats)
    assert cinema.current_booking is None
    assert cinema.last_booking_number == 1
    display_str = cinema.screen_display()
    for line in screen_display:
        assert line in display_str


@pytest.mark.parametrize("movie_title, rows, seats_per_row", [("Inception", 8, 10)])
def test_start_checking(movie_title, rows, seats_per_row):
    cinema = Cinema(movie_title, rows, seats_per_row)
    cinema.start_checking()
    assert cinema.processing_mode == "Checking_Mode"


@pytest.mark.parametrize(
    "cinema, num_seats, booking_id, screen_display",
    [
        (
            Cinema("Inception", 8, 10),
            4,
            "GIC0001",
            [
                "Selected seats:",
                "S C R E E N",
                "H . . . . . . . . . .",
                "G . . . . . . . . . .",
                "F . . . . . . . . . .",
                "E . . . . . . . . . .",
                "D . . . . . . . . . .",
                "C . . . . . . . . . .",
                "B . . . . . . . . . .",
                "A . . . o o o o . . .",
                "  1 2 3 4 5 6 7 8 9 10",
            ],
        )
    ],
)
def test_check_booking(cinema, num_seats, booking_id, screen_display):
    cinema.create_default_booking(num_seats)
    cinema.confirm_booking()
    cinema.start_checking()
    cinema.check_booking(booking_id)
    assert cinema.current_checking.booking_id == booking_id
    assert cinema.current_checking.status == consts.BOOKING_STATUS_CONFIRMED
    assert len(cinema.current_checking.seats) == num_seats
    assert all(seat.state == consts.SEAT_STATE_BOOKED for seat in cinema.current_checking.seats)
    display_str = cinema.screen_display()
    for line in screen_display:
        assert line in display_str
