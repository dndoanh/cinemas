from typing import Optional

import utils.messages as msg
from handlers.cinema.cinema_creation_handler import CinemaCreationHandler
from handlers.cinema.cinema_handler_factory import CinemaHandlerFactory
from handlers.io.console_io_handler import ConsoleIOHandler
from handlers.io.io_handler import IOHandler
from models.cinema import Cinema
from utils.validation import validate_menu_selection


class BookingHandler:
    def __init__(self, io_handler: IOHandler = None) -> None:
        """Initialize the handler for Cinema booking management system.
        Args:
            io_handler(IOHandler): the handler of input and output.
                Use console input and output by default.
        """
        if io_handler is None:
            io_handler = ConsoleIOHandler()
        self.io_handler: IOHandler = io_handler
        self.cinema: Optional[Cinema] = None

    def run(self) -> None:
        """Run the cinema booking processes."""
        self.cinema = CinemaCreationHandler().run()
        self._main_menu()

    def _main_menu(self) -> None:
        """Display main menu."""
        option = self._input_menu_selection()
        self._get_handler(option)

    def _get_handler(self, option: str) -> None:
        """Process ticket booking.
        Args:
            option(str): a menu selection.
        """
        cinema_handler = CinemaHandlerFactory.get_handler(option)
        cinema_handler.run(self.cinema)
        self._main_menu()

    def _input_menu_selection(self) -> str:
        """Select an option from the menu.
        Returns:
            a menu selection.
        """
        is_valid_selection = False
        selection = None
        menu_str = msg.MSG_WELCOME.format(
            movie_title=self.cinema.movie_title,
            seats_available=self.cinema.available_seats,
        )
        while not is_valid_selection:
            self.io_handler.output(menu_str)
            selection_str = self.io_handler.input()
            is_valid, selection = validate_menu_selection(selection_str)
            if not is_valid:
                self.io_handler.output(msg.MSG_INVALID_MENU_SELECTION)
            else:
                is_valid_selection = True
        return selection
