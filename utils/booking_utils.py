from typing import List

import utils.constants as consts
from models.seat import Seat


def generate_booking_id(last_booking_number: int) -> str:
    """Generate new booking id with prefix 'GIC'
    Args:
        last_booking_number(int): last booking id number.
    Returns:
        new booking id.
    """
    next_id = "0000" + str(last_booking_number + 1)
    return f"{consts.BOOKING_ID_PREFIX}{next_id[len(next_id) - 4:]}"


def get_furthest_row_idx(seat_map: List[List[Seat]]) -> int:
    """Get the furthest row index which is start row to reserve.
    Args:
        seat_map(List[List[Seat]]): the seat map which contains two-dimensional array of Seat.
    Returns:
        an index of the row which has at least one Empty seat.
    """
    furthest_row_idx = 0
    while furthest_row_idx < len(seat_map):
        if any([seat for seat in seat_map[furthest_row_idx] if seat.state == consts.SEAT_STATE_EMPTY]):
            return furthest_row_idx
        furthest_row_idx += 1
    raise ValueError("There is no row which has at least one Empty seat.")


def generate_default_seats(seat_map: List[List[Seat]], num_tickets: int) -> List[Seat]:
    """Do generate default seats reservation
    Args:
        seat_map(List[List[Seat]]): the seat map which contains two-dimensional array of Seat.
        num_tickets(int): number of tickets to reserve.
    Returns:
        a list of seats for reservation.
    """
    result_seats = []
    start_row = get_furthest_row_idx(seat_map)
    while len(result_seats) < num_tickets:
        result_seats = reserve_row_by_mid_most(seat_map, start_row, num_tickets, result_seats)
        start_row += 1
    return result_seats


def reserve_row_by_mid_most(seat_map: List[List[Seat]], start_row: int, no_of_seats: int, result_seats: List[Seat]) -> List[Seat]:
    """Reverse seats by looking at specified row by middle most strategy.
    Args:
        seat_map(List[List[Seat]]): the seat map which contains two-dimensional array of Seat.
        start_row(int): the row index to start looking up.
        no_of_seats(int): number of tickets to reserve.
        result_seats(List[Seat]): a list of seats which are reserved.
    Returns:
        a list of seats for reservation.
    """
    mid_col = (len(seat_map[0]) - 1) // 2
    # possible to reserve at mid
    if len(result_seats) < no_of_seats and seat_map[start_row][mid_col].state == consts.SEAT_STATE_EMPTY:
        seat_map[start_row][mid_col].update_state(consts.SEAT_STATE_RESERVED)
        result_seats.append(seat_map[start_row][mid_col])
    right_col = mid_col + 1
    left_col = mid_col - 1
    while len(result_seats) < no_of_seats and (right_col < len(seat_map[0]) or left_col > -1):
        # possible to reserve at right
        if len(result_seats) < no_of_seats and seat_map[start_row][right_col].state == consts.SEAT_STATE_EMPTY:
            seat_map[start_row][right_col].update_state(consts.SEAT_STATE_RESERVED)
            result_seats.append(seat_map[start_row][right_col])
        right_col += 1
        # possible to reserve at left
        if len(result_seats) < no_of_seats and seat_map[start_row][left_col].state == consts.SEAT_STATE_EMPTY:
            seat_map[start_row][left_col].update_state(consts.SEAT_STATE_RESERVED)
            result_seats.append(seat_map[start_row][left_col])
        left_col -= 1
    return result_seats


def reserve_row_by_right_most(seat_map: List[List[Seat]], start_row: int, start_col: int, no_of_seats: int, result_seats: List[Seat]) -> List[Seat]:
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


def generate_seats_by_position(seat_map: List[List[Seat]], no_of_seats: int, start_row: int, start_col: int) -> List[Seat]:
    """Do generate seats at specific position for reservation.
    Args:
        seat_map(List[List[Seat]]): the seat map which contains two-dimensional array of Seat.
        no_of_seats(int): number of tickets to reserve.
        start_row(int): the row index to start looking up.
        start_col(int): the column index to start looking up.
    Returns:
        a list of seats for reservation.
    """
    result_seats = []
    result_seats = reserve_row_by_right_most(seat_map, start_row, start_col, no_of_seats, result_seats)
    if len(result_seats) < no_of_seats:
        start_row += 1
        if start_row == len(seat_map):
            start_row = 0
        while len(result_seats) < no_of_seats:
            result_seats = reserve_row_by_mid_most(seat_map, start_row, no_of_seats, result_seats)
            start_row += 1
            if start_row == len(seat_map):
                start_row = 0
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
