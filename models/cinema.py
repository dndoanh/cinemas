import utils.constants as consts
import utils.messages as msg
from models.booking import Booking
from models.seat import Seat
from utils.booking_utils import (
    build_index_map,
    generate_booking_id,
    generate_default_seats,
    generate_seats_by_position,
)


class Cinema:
    def __init__(self, movie_title: str, rows: int, seats_per_row: int) -> None:
        """Initialize an object of the cinema.
             rows * seats_per_row empty seats.
        Args:
            movie_title(str): the title of the movie.
            rows(str): number of rows in of the cinema.
            seats_per_row(str): number of tickets in each row.
        """
        self.movie_title = movie_title
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seat_map = [
            [Seat(row, col, consts.SEAT_STATE_EMPTY) for col in range(seats_per_row)]
            for row in range(rows)
        ]
        self.index_map = build_index_map(rows, seats_per_row)
        self.last_booking_number = 0
        self.bookings = {}
        self.processing_mode = None
        self.current_booking: None | Booking = None
        self.current_checking: None | Booking = None

    @property
    def available_seats(self) -> int:
        return sum(
            [
                sum(
                    [
                        self.seat_map[row][col].state == consts.SEAT_STATE_EMPTY
                        for col in range(self.seats_per_row)
                    ]
                )
                for row in range(self.rows)
            ]
        )

    def start_booking(self) -> None:
        """Start processing in booking mode."""
        self.processing_mode = consts.PROCESSING_BOOKING_MODE

    def exit_processing(self) -> None:
        """End processing."""
        self.processing_mode = None
        self.current_booking = None
        self.current_checking = None

    def create_default_booking(self, num_tickets: int) -> None:
        """Auto create new booking reservation.
        Args:
            num_tickets(int): number of tickets to order.
        Returns:
            a booking with default reserved seats.
        """
        if num_tickets > self.available_seats:
            raise ValueError(
                msg.MSG_INVALID_EXCEEDING_NUMBER_OF_TICKETS.format(
                    num_seats=self.available_seats
                )
            )
        booking_id = generate_booking_id(self.last_booking_number)
        seats = generate_default_seats(self.seat_map, num_tickets)
        self.current_booking = Booking(
            booking_id, consts.BOOKING_STATUS_RESERVED, seats
        )

    def is_seating_position_exist(self, seating_position: str) -> bool:
        """Check whether given seat position exist in seat map or not.
        Args:
            seating_position(str): the seat position in row and column format. E.g. A08
        Returns:
            a boolean value to indicate the seat position exist or not.
        """
        seating_position = seating_position.upper()
        return seating_position in self.index_map

    def change_seating_position(self, seating_position: str) -> None:
        """Re-generate booking seats with the specific starting position.
        Args:
            seating_position(str): seating position.
        """
        seating_position = seating_position.upper()
        if not self.is_seating_position_exist(seating_position):
            raise KeyError(msg.MSG_INVALID_SEATING_POSITION)
        self.current_booking.release_reserved_seats()
        num_seats = len(self.current_booking.seats)
        start_row, start_col = self.index_map[seating_position]
        seats = generate_seats_by_position(
            self.seat_map, num_seats, start_row, start_col
        )
        self.current_booking.update_seats(seats)

    def confirm_booking(self) -> None:
        """Confirm current booking."""
        self.current_booking.update_status(consts.BOOKING_STATUS_CONFIRMED)
        booking_id = self.current_booking.booking_id
        self.bookings[booking_id] = self.current_booking
        self.current_booking = None
        self.last_booking_number += 1

    def is_booking_id_exist(self, booking_id: str) -> bool:
        """Check whether given booking id exist in seat map or not.
        Args:
            booking_id(str): the booking id
        Returns:
            a boolean value to indicate the booking id exist or not.
        """
        booking_id = booking_id.upper()
        return booking_id in self.bookings

    def start_checking(self) -> None:
        """Start processing in checking mode."""
        self.processing_mode = consts.PROCESSING_CHECKING_MODE

    def check_booking(self, booking_id: str) -> None:
        """Do check the booking with given booking id."""
        booking_id = booking_id.upper()
        if self.is_booking_id_exist(booking_id):
            self.current_checking = self.bookings[booking_id]
        else:
            raise ValueError(msg.MSG_NOT_EXIST_BOOKING_ID.format(booking_id=booking_id))

    def screen_display(self) -> str:
        """Display the current state of the cinema in string format.
        Returns:
             a string to display on the screen.
        """
        top_lines = self._get_top_lines()
        mid_lines = self._get_mid_lines()
        bottom_lines = self._get_bottom_lines()
        return f"{top_lines}{mid_lines}{bottom_lines}"

    def _get_top_lines(self) -> str:
        """Get top lines of the screen."""
        screen_line = " ".join(list(msg.MSG_INFO_SCREEN))
        dash_line = "-" * self.seats_per_row * 2
        return f"{msg.MSG_INFO_SELECTED_SEATS}{screen_line}\n{dash_line}\n"

    def _get_mid_lines(self) -> str:
        """Get middle lines of the screen."""
        mid_lines = ""
        for row in range(self.rows - 1, -1, -1):
            line_str = consts.ALPHABET_LIST[row]
            for col in range(self.seats_per_row):
                if self.processing_mode == consts.PROCESSING_CHECKING_MODE and any(
                    [
                        seat
                        for seat in self.current_checking.seats
                        if seat.row == row and seat.col == col
                    ]
                ):
                    line_str += consts.DISPLAY_RESERVED
                else:
                    line_str += str(self.seat_map[row][col])
            mid_lines += " ".join(list(line_str)) + "\n"
        return mid_lines

    def _get_bottom_lines(self) -> str:
        """Get bottom lines of the screen."""
        bottom_line = " "
        for col in range(1, self.seats_per_row + 1):
            bottom_line += " " + str(col)
        return bottom_line
