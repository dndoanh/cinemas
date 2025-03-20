from abc import ABC, abstractmethod


class IOHandler(ABC):

    @abstractmethod
    def input_handler(self) -> str:
        """Handle input."""
        raise NotImplementedError("input_handler should be implemented in subclasses.")

    @abstractmethod
    def output_handler(self, output_str: str) -> None:
        """Handle output."""
        raise NotImplementedError("output_handler should be implemented in subclasses.")
