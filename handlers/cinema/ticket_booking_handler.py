import utils.messages as msg
from handlers.cinema.cinema_handler import CinemaHandler
from handlers.io.io_handler import IOHandler
from models.cinema import Cinema
from utils.validation import validate_number_of_tickets, validate_string_input


class TicketBookingHandler(CinemaHandler):
    def __init__(self, io_handler: IOHandler = None):
        """Initialize the handler for ticket booking."""
        super().__init__(io_handler)
        self.cinema = None

    def run(self, cinema: Cinema) -> None:
        """Start ticket booking process.
        Args:
            cinema(Cinema): a given cinema to process ticket booking.
        """
        self.cinema = cinema
        self.cinema.start_booking()
        num_tickets = self._input_number_of_tickets()
        if num_tickets is not None:
            self._auto_create_reservation(num_tickets)
            self._confirm_booking()
        self.cinema.exit_processing()

    def _auto_create_reservation(self, num_tickets: int) -> None:
        """Auto create a booking reservation.
        Args:
            num_tickets(int): number of tickets to reserve.
        """
        self.cinema.create_default_booking(num_tickets)
        self.io_handler.output(
            msg.MSG_OUTPUT_SUCCESSFULLY_RESERVED.format(
                num_tickets=num_tickets, movie_title=self.cinema.movie_title
            )
        )

    def _confirm_booking(self) -> None:
        """Confirm or change the seating position."""
        is_booking_confirmed = False
        while not is_booking_confirmed:
            self._display_current_booking()
            seating_position = self._input_seating_position()
            if seating_position is None:
                booking_id = self.cinema.current_booking.booking_id
                self.cinema.confirm_booking()
                self.io_handler.output(
                    msg.MSG_OUTPUT_BOOKING_CONFIRMED.format(booking_id=booking_id)
                )
                break
            else:
                self.cinema.change_seating_position(seating_position)

    def _input_number_of_tickets(self) -> int:
        """Input the number of tickets.
        Returns:
            a number ot tickets to reserve.
        """
        is_valid_input = False
        num_tickets = None
        while not is_valid_input:
            self.io_handler.output(msg.MSG_INPUT_NUMBER_OF_TICKETS)
            num_tickets_str = self.io_handler.input()
            if num_tickets_str == "":
                num_tickets = None
                break
            is_valid, num_tickets = validate_number_of_tickets(num_tickets_str)
            if not is_valid:
                self.io_handler.output(msg.MSG_INVALID_NUMBER_OF_TICKETS)
            else:
                if num_tickets > self.cinema.available_seats:
                    self.io_handler.output(
                        msg.MSG_INVALID_EXCEEDING_NUMBER_OF_TICKETS.format(
                            num_seats=self.cinema.available_seats
                        )
                    )
                else:
                    is_valid_input = True
        return num_tickets

    def _input_seating_position(self) -> str:
        """Input seating position to relocate seats.
        Returns:
            a seating position.
        """
        is_valid_input = False
        seating_position = None
        while not is_valid_input:
            self.io_handler.output(msg.MSG_INPUT_SEATING_POSITION)
            seating_position_str = self.io_handler.input()
            if seating_position_str == "":
                seating_position = None
                break
            is_valid, seating_position = validate_string_input(seating_position_str)
            if not is_valid:
                self.io_handler.output(msg.MSG_INVALID_SEATING_POSITION)
            else:
                is_seating_exist = self.cinema.is_seating_position_exist(
                    seating_position
                )
                if not is_seating_exist:
                    self.io_handler.output(msg.MSG_INVALID_SEATING_POSITION)
                else:
                    is_valid_input = True
        return seating_position

    def _display_current_booking(self) -> None:
        """Display the current booking and seat map to output."""
        booking_id = self.cinema.current_booking.booking_id
        self.io_handler.output(msg.MSG_OUTPUT_BOOKING_ID.format(booking_id=booking_id))
        self.io_handler.output(self.cinema.screen_display())
