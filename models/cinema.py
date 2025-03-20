import utils.constants as consts
from models.booking import Booking
from models.seat import Seat
from utils.booking_utils import build_index_map, generate_booking_id, generate_default_seats, generate_seats_by_position


class Cinema:

    def __init__(self, movie_title: str, rows: int, seats_per_row: int) -> None:
        """Initialize an object of the cinema.
             rows * seats_per_row empty seats.
        Args:
            movie_title(str): the title of the movie.
            rows(str): number of rows in of the cinema.
            seats_per_row(str): number of seats in each row.
        """
        self.movie_title = movie_title
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seat_map = [[Seat(row, col, consts.SEAT_STATE_EMPTY) for col in range(seats_per_row)] for row in range(rows)]
        self.index_map = build_index_map(rows, seats_per_row)
        self.last_booking_number = 0
        self.bookings = []
        self.processing_mode = None
        self.current_booking: None | Booking = None
        self.current_checking: None | Booking = None

    @property
    def available_seats(self) -> int:
        return sum([sum([self.seat_map[row][col].state == consts.SEAT_STATE_EMPTY for col in range(self.seats_per_row)]) for row in range(self.rows)])

    def start_booking(self) -> None:
        """Start processing in booking mode."""
        self.processing_mode = consts.PROCESSING_BOOKING_MODE

    def exit_processing(self) -> None:
        """End processing."""
        self.processing_mode = None

    def create_default_booking(self, num_seats) -> None:
        """Auto create new booking reservation.
        Args:
            num_seats(int): number of seats to order.
        Returns:
            a booking with default reserved seats.
        """
        booking_id = generate_booking_id(self.last_booking_number)
        seats = generate_default_seats(self.seat_map, num_seats)
        self.current_booking = Booking(booking_id, consts.BOOKING_STATUS_RESERVED, seats)

    def change_seat_position(self, start_position: str) -> None:
        """Re-generate booking seats for the specific starting position.
        Args:
            start_position(str): starting seat position.
        """
        self.current_booking.release_reserved_seats()
        num_seats = len(self.current_booking.seats)
        start_row, start_col = self.index_map[start_position]
        seats = generate_seats_by_position(self.seat_map, num_seats, start_row, start_col)
        self.current_booking.update_seats(seats)

    def confirm_booking(self) -> None:
        """Confirm current booking."""
        self.current_booking.update_status(consts.BOOKING_STATUS_CONFIRMED)
        self.bookings.append(self.current_booking)
        self.current_booking = None
        self.last_booking_number += 1

    def start_checking(self) -> None:
        """Start processing in checking mode."""
        self.processing_mode = consts.PROCESSING_CHECKING_MODE

    def check_booking(self, booking_id: str) -> None:
        """Do check the booking with given booking id."""
        bookings = [booking for booking in self.bookings if booking.booking_id == booking_id]
        if any(bookings):
            self.current_checking = bookings[0]

    def screen_display(self) -> str:
        """Display the current state of the cinema in string format.
        Returns:
             a string to display on the screen.
        """
        display_str = "Selected seats:\n"
        display_str += " ".join(list("SCREEN")) + "\n"
        for row in range(self.rows - 1, -1, -1):
            line_str = consts.ALPHABET_LIST[row]
            for col in range(self.seats_per_row):
                if self.processing_mode == consts.PROCESSING_CHECKING_MODE and any(
                    [seat for seat in self.current_checking.seats if seat.row == row and seat.col == col]
                ):
                    line_str += consts.DISPLAY_RESERVED
                else:
                    line_str += str(self.seat_map[row][col])
            display_str += " ".join(list(line_str)) + "\n"
        bottom_line_str = " "
        for col in range(1, self.seats_per_row + 1):
            bottom_line_str += " " + str(col)
        display_str += bottom_line_str + "\n"
        return display_str
