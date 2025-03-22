import utils.constants as consts
import utils.messages as msg
from handlers.cinema.cinema_handler import CinemaHandler
from handlers.io.io_handler import IOHandler
from models.cinema import Cinema
from utils.validation import validate_string_input


class CheckBookingsHandler(CinemaHandler):
    def __init__(self, io_handler: IOHandler = None):
        """Initialize the handler for check bookings."""
        super().__init__(io_handler)
        self.cinema = None

    def run(self, cinema: Cinema) -> None:
        """Start check bookings process."""
        self.cinema = cinema
        self.cinema.start_checking()
        while True:
            booking_id = self._input_booking_id()
            if booking_id is None:
                break
            else:
                self.cinema.check_booking(booking_id)
                self._screen_display_output()
        self.cinema.exit_processing()

    def _input_booking_id(self) -> str:
        """Input booking to check."""
        is_valid_input = False
        booking_id = None
        while not is_valid_input:
            self.io_handler.output(msg.MSG_INPUT_BOOKING_ID)
            booking_id_str = self.io_handler.input()
            if booking_id_str == "":
                booking_id = None
                break
            is_valid, booking_id = validate_string_input(booking_id_str)
            if not is_valid:
                self.io_handler.output(msg.MSG_INVALID_BOOKING_ID)
            else:
                is_booking_id_exist = self.cinema.is_booking_id_exist(booking_id)
                if not is_booking_id_exist:
                    self.io_handler.output(
                        msg.MSG_NOT_EXIST_BOOKING_ID.format(booking_id=booking_id)
                    )
                else:
                    is_valid_input = True
        return booking_id

    def _screen_display_output(self) -> None:
        """Display the current booking id and seat map to output."""
        booking_id = (
            self.cinema.current_booking.booking_id
            if self.cinema.processing_mode == consts.PROCESSING_BOOKING_MODE
            else self.cinema.current_checking.booking_id
        )
        self.io_handler.output(msg.MSG_OUTPUT_BOOKING_ID.format(booking_id=booking_id))
        self.io_handler.output(self.cinema.screen_display())
