from typing import List

import utils.constants as consts
import utils.messages as msg
from models.seat import Seat


def generate_booking_id(last_booking_number: int) -> str:
    """Generate new booking id with prefix 'GIC'
    Args:
        last_booking_number(int): last booking id number.
    Returns:
        new booking id.
    """
    next_id = "0000" + str(last_booking_number + 1)
    return f"{consts.BOOKING_ID_PREFIX}{next_id[len(next_id) - 4 :]}"


def get_furthest_row_idx(seat_map: List[List[Seat]]) -> int:
    """Get the furthest row index which is start row to reserve.
    Args:
        seat_map(List[List[Seat]]): the seat map which contains two-dimensional array of Seat.
    Returns:
        an index of the row which has at least one Empty seat.
    """
    furthest_row_idx = 0
    while furthest_row_idx < len(seat_map):
        if any(
            [
                seat
                for seat in seat_map[furthest_row_idx]
                if seat.state == consts.SEAT_STATE_EMPTY
            ]
        ):
            return furthest_row_idx
        furthest_row_idx += 1
    raise ValueError(msg.MSG_INVALID_NO_EMPTY_SEAT)


def generate_default_seats(seat_map: List[List[Seat]], num_tickets: int) -> List[Seat]:
    """Algorithm to generate default seats reservation:
    1. Begin at the furthest row and reserve all available seats in middle-most manner.
    2. If there are not enough seats available in the current row, proceed to the next row closer to the screen, reserving seats in a middle-most manner.
    Args:
        seat_map(List[List[Seat]]): the seat map which contains two-dimensional array of Seat.
        num_tickets(int): number of tickets to reserve.
    Returns:
        a list of seats for reservation.
    """
    result_seats = []
    start_row = get_furthest_row_idx(seat_map)
    while len(result_seats) < num_tickets:
        result_seats = _reserve_row_by_mid_most(
            seat_map, start_row, num_tickets, result_seats
        )
        start_row += 1
    return result_seats


def _reserve_row_by_mid_most(
    seat_map: List[List[Seat]],
    start_row: int,
    num_tickets: int,
    result_seats: List[Seat],
) -> List[Seat]:
    """Reverse seats by looking at specified row by middle most strategy.
    Args:
        seat_map(List[List[Seat]]): the seat map which contains two-dimensional array of Seat.
        start_row(int): the row index to start looking up.
        num_tickets(int): number of tickets to reserve.
        result_seats(List[Seat]): a list of seats which are reserved.
    Returns:
        a list of seats for reservation.
    """
    mid_col = (len(seat_map[0]) - 1) // 2
    right_col, left_col = mid_col + 1, mid_col - 1
    result_seats = _reserve_at_mid(
        seat_map, start_row, mid_col, num_tickets, result_seats
    )
    while len(result_seats) < num_tickets and (
        right_col < len(seat_map[0]) or left_col > -1
    ):
        result_seats = _reserve_at_right(
            seat_map, start_row, right_col, num_tickets, result_seats
        )
        result_seats = _reserve_at_left(
            seat_map, start_row, left_col, num_tickets, result_seats
        )
        right_col += 1
        left_col -= 1
    return result_seats


def _reserve_at_mid(
    seat_map: List[List[Seat]],
    start_row: int,
    mid_col: int,
    num_tickets: int,
    result_seats,
) -> List[Seat]:
    """Possible to reserve at mid"""
    if (
        len(result_seats) < num_tickets
        and seat_map[start_row][mid_col].state == consts.SEAT_STATE_EMPTY
    ):
        seat_map[start_row][mid_col].update_state(consts.SEAT_STATE_RESERVED)
        result_seats.append(seat_map[start_row][mid_col])
    return result_seats


def _reserve_at_right(
    seat_map: List[List[Seat]],
    start_row: int,
    right_col: int,
    num_tickets: int,
    result_seats,
) -> List[Seat]:
    """Possible to reserve at right"""
    if (
        len(result_seats) < num_tickets
        and seat_map[start_row][right_col].state == consts.SEAT_STATE_EMPTY
    ):
        seat_map[start_row][right_col].update_state(consts.SEAT_STATE_RESERVED)
        result_seats.append(seat_map[start_row][right_col])
    return result_seats


def _reserve_at_left(
    seat_map: List[List[Seat]],
    start_row: int,
    left_col: int,
    num_tickets: int,
    result_seats,
) -> List[Seat]:
    """Possible to reserve at left"""
    if (
        len(result_seats) < num_tickets
        and seat_map[start_row][left_col].state == consts.SEAT_STATE_EMPTY
    ):
        seat_map[start_row][left_col].update_state(consts.SEAT_STATE_RESERVED)
        result_seats.append(seat_map[start_row][left_col])
    return result_seats


def _reserve_row_by_right_most(
    seat_map: List[List[Seat]],
    start_row: int,
    start_col: int,
    no_of_seats: int,
    result_seats: List[Seat],
) -> List[Seat]:
    """Reverse seats by looking at specified row by right most strategy.
    Args:
        seat_map(List[List[Seat]]): the seat map which contains two-dimensional array of Seat.
        start_row(int): the row index to start looking up.
        start_col(int): the column index to start looking up.
        no_of_seats(int): number of tickets to reserve.
        result_seats(List[Seat]): a list of seats which are reserved.
    Returns:
        a list of seats for reservation.
    """
    while len(result_seats) < no_of_seats and start_col < len(seat_map[0]):
        if seat_map[start_row][start_col].state == consts.SEAT_STATE_EMPTY:
            seat_map[start_row][start_col].update_state(consts.SEAT_STATE_RESERVED)
            result_seats.append(seat_map[start_row][start_col])
        start_col += 1
    return result_seats


def generate_seats_by_position(
    seat_map: List[List[Seat]], num_tickets: int, start_row: int, start_col: int
) -> List[Seat]:
    """Algorithm to generate seats reservation at specific position:
        1. Begin at the specified position (`start_row`, `start_col`) and reserve all available seats to the right of the cinema hall.
        2. If there are not enough seats available in the current row, proceed to the next row closer to the screen, reserving seats in a middle-most manner.
        3. If there are still not enough seats, return the `start_row` and continue reserving all seats available at the current row and next row further from the screen, again in a middle-most manner.
    Args:
        seat_map(List[List[Seat]]): the seat map which contains two-dimensional array of Seat.
        num_tickets(int): number of tickets to reserve.
        start_row(int): the row index to start looking up.
        start_col(int): the column index to start looking up.
    Returns:
        a list of seats for reservation.
    """
    result_seats = []
    result_seats = _reserve_row_by_right_most(
        seat_map, start_row, start_col, num_tickets, result_seats
    )
    result_seats = _generate_seats_mid_most(
        seat_map, num_tickets, start_row, result_seats
    )
    return result_seats


def _generate_seats_mid_most(
    seat_map: List[List[Seat]],
    num_tickets: int,
    start_row: int,
    result_seats: List[Seat],
) -> List[Seat]:
    """Generate seats by middle most."""
    next_row = start_row
    goto_closer_row = True
    while len(result_seats) < num_tickets:
        next_row += 1 if goto_closer_row else -1
        if next_row == len(seat_map):
            next_row = start_row
            goto_closer_row = False
        result_seats = _reserve_row_by_mid_most(
            seat_map, next_row, num_tickets, result_seats
        )
    return result_seats


def build_index_map(rows: int, cols: int) -> dict:
    """Build index map for all seats in the cinema.
    Args:
        rows(int): number of rows
        cols(int): number of columns
    Returns:
         a dictionary contains all indexes.
    """
    index_map = {}
    for row in range(rows):
        for col in range(cols):
            col_str = f"0{col + 1}"
            col_str = col_str[len(col_str) - 2 :]
            key = f"{consts.ALPHABET_LIST[row]}{col_str}"
            index_map[key] = (row, col)
    return index_map
