import utils.constants as consts
import utils.messages as msg
from handlers.io.console_io_handler import ConsoleIOHandler
from handlers.io.io_handler import IOHandler
from models.cinema import Cinema
from utils.validation import validate_menu_selection, validate_number_of_tickets, validate_string_input, validate_title_rows_seats_per_row


class BookingHandler:

    def __init__(self, io_handler: IOHandler = None) -> None:
        """Initialize the handler for booking system.
        Args:
            io_handler(IOHandler): the handler of input and output.
            Use console input and output by default.
        """
        if io_handler is None:
            io_handler = ConsoleIOHandler()
        self.io_handler = io_handler
        self.cinema = None

    def start(self) -> None:
        """Start the cinema booking process."""
        self._create_cinema()
        self._main_menu()

    def _create_cinema(self) -> None:
        """Create a new cinema with given input of movie title, rows, seats per row."""
        self.io_handler.output_handler(msg.MSG_BEGIN)
        movie_title, rows, seats_per_row = self._input_title_rows_seats_per_row()
        self.cinema = Cinema(movie_title, rows, seats_per_row)

    def _main_menu(self) -> None:
        """Display main menu."""
        menu = self._input_menu_selection()
        if menu == "1":
            self._ticket_booking()
        elif menu == "2":
            self._check_bookings()
        else:
            self._exit()

    def _ticket_booking(self) -> None:
        """Process ticket booking."""
        self.cinema.start_booking()
        num_tickets = self._input_number_of_tickets()
        if num_tickets is not None:
            self._auto_create_booking(num_tickets)
            self._confirm_booking()
        self.cinema.exit_processing()
        self._main_menu()

    def _check_bookings(self) -> None:
        """Process check bookings."""
        self.cinema.start_checking()
        while True:
            booking_id = self._input_booking_id()
            if booking_id is None:
                break
            else:
                self.cinema.check_booking(booking_id)
                self._screen_display_output()
        self.cinema.exit_processing()
        self._main_menu()

    def _auto_create_booking(self, num_tickets: int) -> None:
        """Auto booking creation."""
        self.cinema.create_default_booking(num_tickets)
        self.io_handler.output_handler(msg.MSG_OUTPUT_SUCCESSFULLY_RESERVED.format(num_tickets=num_tickets, movie_title=self.cinema.movie_title))

    def _confirm_booking(self) -> None:
        """Confirm or change the seating position."""
        is_booking_confirmed = False
        while not is_booking_confirmed:
            self._screen_display_output()
            seating_position = self._input_seating_position()
            if seating_position is None:
                booking_id = self.cinema.current_booking.booking_id
                self.cinema.confirm_booking()
                self.io_handler.output_handler(msg.MSG_OUTPUT_BOOKING_CONFIRMED.format(booking_id=booking_id))
                break
            else:
                self.cinema.change_seating_position(seating_position)

    def _input_title_rows_seats_per_row(self) -> tuple:
        """Input movie title, rows, seats per row."""
        is_valid_input = False
        movie_title, rows, seats_per_row = None, None, None
        while not is_valid_input:
            title_rows_seats_per_row_str = self.io_handler.input_handler()
            is_valid, movie_title, rows, seats_per_row = validate_title_rows_seats_per_row(title_rows_seats_per_row_str)
            if not is_valid:
                self.io_handler.output_handler(msg.MSG_INVALID_MOVIE_TITLE_ROWS_SEATS_PER_ROW)
            else:
                is_valid_input = True
        return movie_title, rows, seats_per_row

    def _input_menu_selection(self) -> str:
        """Select an option from the menu."""
        is_valid_selection = False
        selection = None
        menu_str = msg.MSG_WELCOME.format(movie_title=self.cinema.movie_title, seats_available=self.cinema.available_seats)
        while not is_valid_selection:
            self.io_handler.output_handler(menu_str)
            selection_str = self.io_handler.input_handler()
            is_valid, selection = validate_menu_selection(selection_str)
            if not is_valid:
                self.io_handler.output_handler(msg.MSG_INVALID_MENU_SELECTION)
            else:
                is_valid_selection = True
        return selection

    def _input_number_of_tickets(self) -> int:
        """Input the number of tickets."""
        is_valid_input = False
        num_tickets = None
        while not is_valid_input:
            self.io_handler.output_handler(msg.MSG_INPUT_NUMBER_OF_TICKETS)
            num_tickets_str = self.io_handler.input_handler()
            if num_tickets_str == "":
                num_tickets = None
                break
            is_valid, num_tickets = validate_number_of_tickets(num_tickets_str)
            if not is_valid:
                self.io_handler.output_handler(msg.MSG_INVALID_NUMBER_OF_TICKETS)
            else:
                if num_tickets > self.cinema.available_seats:
                    self.io_handler.output_handler(msg.MSG_INVALID_EXCEEDING_NUMBER_OF_TICKETS.format(num_seats=self.cinema.available_seats))
                else:
                    is_valid_input = True
        return num_tickets

    def _input_seating_position(self) -> str:
        """Input seating position to relocate seats."""
        is_valid_input = False
        seating_position = None
        while not is_valid_input:
            self.io_handler.output_handler(msg.MSG_INPUT_SEATING_POSITION)
            seating_position_str = self.io_handler.input_handler()
            if seating_position_str == "":
                seating_position = None
                break
            is_valid, seating_position = validate_string_input(seating_position_str)
            if not is_valid:
                self.io_handler.output_handler(msg.MSG_INVALID_SEATING_POSITION)
            else:
                is_seating_exist = self.cinema.is_seating_position_exist(seating_position)
                if not is_seating_exist:
                    self.io_handler.output_handler(msg.MSG_INVALID_SEATING_POSITION)
                else:
                    is_valid_input = True
        return seating_position

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
                    self.io_handler.output_handler(msg.MSG_INVALID_BOOKING_ID)
                else:
                    is_valid_input = True
        return booking_id

    def _screen_display_output(self) -> None:
        """Display the current booking id and seat map to output."""
        booking_id = (
            self.cinema.current_booking.booking_id if self.cinema.processing_mode == consts.PROCESSING_BOOKING_MODE else self.cinema.current_checking.booking_id
        )
        self.io_handler.output_handler(msg.MSG_OUTPUT_BOOKING_ID.format(booking_id=booking_id))
        self.io_handler.output_handler(self.cinema.screen_display())

    def _exit(self):
        """Exit booking system."""
        self.io_handler.output_handler(msg.MSG_OUTPUT_GOODBYE)
