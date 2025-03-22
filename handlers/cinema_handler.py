import utils.messages as msg
from handlers.check_bookings_handler import CheckBookingsHandler
from handlers.cinema_creation_handler import CinemaCreationHandler
from handlers.io.console_io_handler import ConsoleIOHandler
from handlers.io.io_handler import IOHandler
from handlers.ticket_booking_handler import TicketBookingHandler
from models.cinema import Cinema
from utils.validation import validate_menu_selection


class CinemaHandler:
    def __init__(
        self,
        io_handler: IOHandler = None,
        cinema_creation_handler: CinemaCreationHandler = None,
    ) -> None:
        """Initialize the handler for Cinema booking management system.
        Args:
            io_handler(IOHandler): the handler of input and output.
                Use console input and output by default.
            cinema_creation_handler(CinemaCreationHandler): the handler of cinema creation.
        """
        if io_handler is None:
            io_handler = ConsoleIOHandler()
        if cinema_creation_handler is None:
            cinema_creation_handler = CinemaCreationHandler()
        self.io_handler: IOHandler = io_handler
        self.cinema_handler: CinemaCreationHandler = cinema_creation_handler
        self.cinema: Cinema | None = None

    def start(self) -> None:
        """Start the cinema booking process."""
        self.cinema = self.cinema_handler.create_cinema()
        self._main_menu()

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
        ticket_handler = TicketBookingHandler(self.cinema)
        ticket_handler.start()
        self._main_menu()

    def _check_bookings(self) -> None:
        """Process check bookings."""
        check_bookings_handler = CheckBookingsHandler(self.cinema)
        check_bookings_handler.start()
        self._main_menu()

    def _input_menu_selection(self) -> str:
        """Select an option from the menu."""
        is_valid_selection = False
        selection = None
        menu_str = msg.MSG_WELCOME.format(
            movie_title=self.cinema.movie_title,
            seats_available=self.cinema.available_seats,
        )
        while not is_valid_selection:
            self.io_handler.output_handler(menu_str)
            selection_str = self.io_handler.input_handler()
            is_valid, selection = validate_menu_selection(selection_str)
            if not is_valid:
                self.io_handler.output_handler(msg.MSG_INVALID_MENU_SELECTION)
            else:
                is_valid_selection = True
        return selection

    def _exit(self):
        """Exit booking system."""
        self.io_handler.output_handler(msg.MSG_OUTPUT_GOODBYE)
