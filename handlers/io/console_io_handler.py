from handlers.io.io_handler import IOHandler


class ConsoleIOHandler(IOHandler):

    def input_handler(self) -> str:
        """Handle input with console."""
        return input()

    def output_handler(self, output_str: str) -> None:
        """Handle output with console."""
        print(output_str)
