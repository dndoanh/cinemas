import utils.messages as msg
from handlers.io.console_io_handler import ConsoleIOHandler
from handlers.io.io_handler import IOHandler
from models.cinema import Cinema
from utils.validation import validate_title_rows_seats_per_row


class CinemaCreationHandler:
    def __init__(self, io_handler: IOHandler = None) -> None:
        """Initialize the handler for cinema creation.
        Args:
            io_handler(IOHandler): the handler of input and output.
                Use console input and output by default.
        """
        if io_handler is None:
            io_handler = ConsoleIOHandler()
        self.io_handler = io_handler

    def run(self) -> Cinema:
        """Start cinema creation process.
        Returns:
            a new object of Cinema.
        """
        self.io_handler.output(msg.MSG_BEGIN)
        movie_title, rows, seats_per_row = self._input_title_rows_seats_per_row()
        cinema = Cinema(movie_title, rows, seats_per_row)
        return cinema

    def _input_title_rows_seats_per_row(self) -> tuple:
        """Input movie title, rows and seats per row.
        Returns:
            a tuple of movie title, rows and seats per row.
        """
        is_valid_input = False
        movie_title, rows, seats_per_row = None, None, None
        while not is_valid_input:
            title_rows_seats_per_row_str = self.io_handler.input()
            is_valid, movie_title, rows, seats_per_row = (
                validate_title_rows_seats_per_row(title_rows_seats_per_row_str)
            )
            if not is_valid:
                self.io_handler.output(msg.MSG_INVALID_MOVIE_TITLE_ROWS_SEATS_PER_ROW)
            else:
                is_valid_input = True
        return movie_title, rows, seats_per_row
