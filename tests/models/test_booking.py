import pytest

from models.booking import Booking
from models.seat import Seat


@pytest.mark.parametrize(
    "booking_id, status, seats", [("ABC0001", "Reserved", [Seat(1, 2, "Reserved")]), ("ABC0001", "Confirmed", [Seat(1, 2, "Booked"), Seat(1, 3, "Booked")])]
)
def test_initialization(booking_id, status, seats):
    booking = Booking(booking_id, status, seats)
    assert isinstance(booking, Booking)
    assert booking.booking_id == booking_id
    assert booking.status == status
    assert booking.seats == seats


@pytest.mark.parametrize(
    "booking_id, status, seats",
    [
        (None, "Reserved", [Seat(1, 2, "Reserved")]),
        ("", "Reserved", [Seat(1, 2, "Reserved")]),
        ("ABC0001", None, [Seat(1, 2, "Reserved")]),
        ("ABC0001", "", [Seat(1, 2, "Reserved")]),
        ("ABC0001", "Pre-confirmed", [Seat(1, 2, "Reserved")]),
        ("ABC0001", "Reserved", [Seat(1, 2, "Empty"), Seat(1, 3, "Reserved")]),
        ("ABC0001", "Reserved", [Seat(1, 2, "Reserved"), Seat(1, 3, "Booked")]),
        ("ABC0001", "Confirmed", [Seat(1, 2, "Empty"), Seat(1, 3, "Reserved")]),
        ("ABC0001", "Confirmed", [Seat(1, 2, "Reserved"), Seat(1, 3, "Booked")]),
        ("ABC0001", "Confirmed", [Seat(1, 2, "Empty"), Seat(1, 3, "Booked")]),
    ],
)
def test_invalid_booking(booking_id, status, seats):
    with pytest.raises(ValueError):
        Booking(booking_id, status, seats)


@pytest.mark.parametrize(
    "booking, new_status, new_state",
    [
        (Booking("ABC0001", "Reserved", [Seat(1, 2, "Reserved"), Seat(1, 3, "Reserved")]), "Confirmed", "Booked"),
        (Booking("ABC0001", "Confirmed", [Seat(1, 2, "Booked"), Seat(1, 3, "Booked")]), "Reserved", "Reserved"),
    ],
)
def test_update_status(booking, new_status, new_state):
    booking.update_status(new_status)
    assert booking.status == new_status
    assert all([seat.state == new_state for seat in booking.seats])


@pytest.mark.parametrize(
    "booking, new_status",
    [
        (Booking("ABC0001", "Reserved", [Seat(1, 2, "Reserved"), Seat(1, 3, "Reserved")]), None),
        (Booking("ABC0001", "Reserved", [Seat(1, 2, "Reserved"), Seat(1, 3, "Reserved")]), ""),
        (Booking("ABC0001", "Confirmed", [Seat(1, 2, "Booked"), Seat(1, 3, "Booked")]), "Pre-confirmed"),
    ],
)
def test_update_status_with_invalid_new_status(booking, new_status):
    with pytest.raises(ValueError):
        booking.update_status(new_status)
