import pytest

from models.seat import Seat
from utils.booking_utils import generate_booking_id, generate_default_seats, generate_seats_by_position, get_furthest_row_idx


@pytest.mark.parametrize("last_booking_number, result", [(0, "GIC0001"), (1, "GIC0002"), (9998, "GIC9999")])
def test_generate_booking_id(last_booking_number, result):
    booking_id = generate_booking_id(last_booking_number)
    assert booking_id == result


@pytest.mark.parametrize(
    "rows, cols, booked_seats, expected_furthest_row_index",
    [
        (8, 10, [], 0),
        (8, 10, [(0, 5)], 0),
        (2, 1, [(0, 0)], 1),
    ],
)
def test_get_furthest_row_index(rows, cols, booked_seats, expected_furthest_row_index):
    seat_map = [[Seat(row, col, "Empty") for col in range(cols)] for row in range(rows)]
    for row, col in booked_seats:
        seat_map[row][col].update_state("Booked")
    furthest_row_index = get_furthest_row_idx(seat_map)
    assert furthest_row_index == expected_furthest_row_index


@pytest.mark.parametrize(
    "rows, cols, booked_seats",
    [
        (0, 0, []),
        (1, 1, [(0, 0)]),
        (2, 2, [(0, 0), (0, 1), (1, 0), (1, 1)]),
    ],
)
def test_get_furthest_row_index_with_errors(rows, cols, booked_seats):
    seat_map = [[Seat(row, col, "Empty") for col in range(cols)] for row in range(rows)]
    for row, col in booked_seats:
        seat_map[row][col].update_state("Booked")
    with pytest.raises(ValueError):
        furthest_row_index = get_furthest_row_idx(seat_map)


@pytest.mark.parametrize(
    "rows, cols, booked_seats, num_tickets, expected_seats",
    [
        (8, 10, [], 4, [Seat(0, 3, "Reserved"), Seat(0, 4, "Reserved"), Seat(0, 5, "Reserved"), Seat(0, 6, "Reserved")]),
        (
            8,
            10,
            [(1, 2), (1, 3), (1, 4), (1, 5)],
            12,
            [
                Seat(0, 0, "Reserved"),
                Seat(0, 1, "Reserved"),
                Seat(0, 2, "Reserved"),
                Seat(0, 3, "Reserved"),
                Seat(0, 4, "Reserved"),
                Seat(0, 5, "Reserved"),
                Seat(0, 6, "Reserved"),
                Seat(0, 7, "Reserved"),
                Seat(0, 8, "Reserved"),
                Seat(0, 9, "Reserved"),
                Seat(1, 6, "Reserved"),
                Seat(1, 7, "Reserved"),
            ],
        ),
        (
            3,
            3,
            [(0, 1)],
            6,
            [Seat(0, 0, "Reserved"), Seat(0, 2, "Reserved"), Seat(1, 0, "Reserved"), Seat(1, 1, "Reserved"), Seat(1, 2, "Reserved"), Seat(2, 1, "Reserved")],
        ),
        (
            3,
            3,
            [],
            9,
            [
                Seat(0, 0, "Reserved"),
                Seat(0, 1, "Reserved"),
                Seat(0, 2, "Reserved"),
                Seat(1, 0, "Reserved"),
                Seat(1, 1, "Reserved"),
                Seat(1, 2, "Reserved"),
                Seat(2, 0, "Reserved"),
                Seat(2, 1, "Reserved"),
                Seat(2, 2, "Reserved"),
            ],
        ),
    ],
)
def test_generate_default_seats(rows, cols, booked_seats, num_tickets, expected_seats):
    seat_map = [[Seat(row, col, "Empty") for col in range(cols)] for row in range(rows)]
    for row, col in booked_seats:
        seat_map[row][col].update_state("Booked")
    result_seats = generate_default_seats(seat_map, num_tickets)
    assert len(result_seats) == num_tickets
    assert all(seat in expected_seats and seat.state == "Reserved" for seat in result_seats)


@pytest.mark.parametrize(
    "rows, cols, booked_seats, num_tickets, start_row, start_col, expected_seats",
    [
        (8, 10, [], 4, 1, 2, [Seat(1, 2, "Reserved"), Seat(1, 3, "Reserved"), Seat(1, 4, "Reserved"), Seat(1, 5, "Reserved")]),
        (
            3,
            3,
            [],
            6,
            1,
            1,
            [Seat(1, 1, "Reserved"), Seat(1, 2, "Reserved"), Seat(2, 0, "Reserved"), Seat(2, 1, "Reserved"), Seat(2, 2, "Reserved"), Seat(0, 1, "Reserved")],
        ),
        (
            3,
            3,
            [],
            9,
            1,
            1,
            [
                Seat(0, 0, "Reserved"),
                Seat(0, 1, "Reserved"),
                Seat(0, 2, "Reserved"),
                Seat(1, 0, "Reserved"),
                Seat(1, 1, "Reserved"),
                Seat(1, 2, "Reserved"),
                Seat(2, 0, "Reserved"),
                Seat(2, 1, "Reserved"),
                Seat(2, 2, "Reserved"),
            ],
        ),
        (
            3,
            3,
            [(1, 1)],
            6,
            1,
            1,
            [Seat(1, 2, "Reserved"), Seat(2, 0, "Reserved"), Seat(2, 1, "Reserved"), Seat(2, 2, "Reserved"), Seat(0, 1, "Reserved"), Seat(0, 2, "Reserved")],
        ),
    ],
)
def test_generate_seats_by_position(rows, cols, booked_seats, num_tickets, start_row, start_col, expected_seats):
    seat_map = [[Seat(row, col, "Empty") for col in range(cols)] for row in range(rows)]
    for row, col in booked_seats:
        seat_map[row][col].update_state("Booked")
    result_seats = generate_seats_by_position(seat_map, num_tickets, start_row, start_col)
    assert len(result_seats) == num_tickets
    assert all(seat in expected_seats and seat.state == "Reserved" for seat in result_seats)
