import pytest

from models.seat import Seat


@pytest.mark.parametrize("row, col, state", [(1, 2, "Empty"), (1, 3, "Reserved"), (1, 4, "Booked")])
def test_initialization(row, col, state):
    seat = Seat(row, col, state)
    assert isinstance(seat, Seat)
    assert seat.row == row
    assert seat.col == col
    assert seat.state == state


@pytest.mark.parametrize("row, col, state", [(1, 2, None), (1, 3, ""), (1, 4, "Abc")])
def test_initialization_with_invalid_seat_state(row, col, state):
    with pytest.raises(ValueError):
        seat = Seat(row, col, state)


@pytest.mark.parametrize(
    "seat, another_seat, result",
    [
        (Seat(1, 2, "Empty"), Seat(3, 5, "Empty"), False),
        (Seat(1, 2, "Reserved"), Seat(3, 5, "Reserved"), False),
        (Seat(1, 2, "Booked"), Seat(3, 5, "Booked"), False),
        (Seat(1, 2, "Empty"), Seat(1, 2, "Empty"), True),
        (Seat(1, 2, "Empty"), Seat(1, 2, "Reserved"), True),
        (Seat(1, 2, "Empty"), Seat(1, 2, "Booked"), True),
    ],
)
def test_eq_operator(seat, another_seat, result):
    actual_result = seat == another_seat
    assert actual_result == result


@pytest.mark.parametrize(
    "seat, display_str",
    [
        (Seat(1, 2, "Empty"), "."),
        (Seat(1, 2, "Reserved"), "o"),
        (Seat(1, 2, "Booked"), "#"),
    ],
)
def test_str(seat, display_str):
    assert str(seat) == display_str


@pytest.mark.parametrize(
    "seat, new_state",
    [(Seat(1, 2, "Empty"), "Reserved"), (Seat(1, 2, "Reserved"), "Booked"), (Seat(1, 2, "Booked"), "Reserved")],
)
def test_update_state(seat, new_state):
    seat.update_state(new_state)
    assert seat.state == new_state


@pytest.mark.parametrize(
    "seat, new_state",
    [(Seat(1, 2, "Empty"), None), (Seat(1, 2, "Reserved"), ""), (Seat(1, 2, "Booked"), "Pre-booked")],
)
def test_update_state_with_invalid_new_state(seat, new_state):
    with pytest.raises(ValueError):
        seat.update_state(new_state)
