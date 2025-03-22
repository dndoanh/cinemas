import utils.messages as msg
from handlers.cinema.cinema_handler import CinemaHandler
from handlers.io.io_handler import IOHandler
from models.cinema import Cinema


class ExitHandler(CinemaHandler):
    def __init__(self, io_handler: IOHandler = None):
        """Initialize the exit handler."""
        super().__init__(io_handler)
        self.cinema = None

    def run(self, cinema: Cinema) -> None:
        """Exit booking system."""
        self.io_handler.output(msg.MSG_OUTPUT_GOODBYE)
        self.io_handler.exit()
