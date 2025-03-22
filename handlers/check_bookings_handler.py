import utils.constants as consts
import utils.messages as msg
from handlers.io.console_io_handler import ConsoleIOHandler
from handlers.io.io_handler import IOHandler
from models.cinema import Cinema
from utils.validation import validate_string_input


class CheckBookingsHandler:
    def __init__(self, cinema: Cinema, io_handler: IOHandler = None) -> None:
        """Initialize the handler for check bookings.
        Args:
            cinema(Cinema): the cinema object.
            io_handler(IOHandler): the handler of input and output.
                Use console input and output by default.
        """
        if io_handler is None:
            io_handler = ConsoleIOHandler()
        self.io_handler = io_handler
        self.cinema = cinema

    def start(self) -> None:
        """Start check bookings process."""
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
            self.io_handler.output_handler(msg.MSG_INPUT_BOOKING_ID)
            booking_id_str = self.io_handler.input_handler()
            if booking_id_str == "":
                booking_id = None
                break
            is_valid, booking_id = validate_string_input(booking_id_str)
            if not is_valid:
                self.io_handler.output_handler(msg.MSG_INVALID_BOOKING_ID)
            else:
                is_booking_id_exist = self.cinema.is_booking_id_exist(booking_id)
                if not is_booking_id_exist:
                    self.io_handler.output_handler(
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
        self.io_handler.output_handler(
            msg.MSG_OUTPUT_BOOKING_ID.format(booking_id=booking_id)
        )
        self.io_handler.output_handler(self.cinema.screen_display())
