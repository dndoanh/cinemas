from abc import ABC, abstractmethod

from handlers.io.console_io_handler import ConsoleIOHandler
from handlers.io.io_handler import IOHandler
from models.cinema import Cinema


class CinemaHandler(ABC):
    def __init__(self, io_handler: IOHandler = None) -> None:
        """Initialize the handler for cinema.
        Args:
            io_handler(IOHandler): the handler of input and output.
                Use console input and output by default.
        """
        if io_handler is None:
            io_handler = ConsoleIOHandler()
        self.io_handler = io_handler

    @abstractmethod
    def run(self, cinema: Cinema) -> None:
        """Start run the handler."""
        raise NotImplementedError("run() should be implemented in subclasses.")
