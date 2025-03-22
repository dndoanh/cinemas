import sys

from handlers.io.io_handler import IOHandler


class ConsoleIOHandler(IOHandler):
    def input(self) -> str:
        """Handle input with console."""
        return input()

    def output(self, output_str: str) -> None:
        """Handle output with console."""
        print(output_str)

    def exit(self) -> None:
        """Handle system exit with console."""
        sys.exit(0)
