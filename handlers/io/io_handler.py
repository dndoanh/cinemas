from abc import ABC, abstractmethod


class IOHandler(ABC):
    @abstractmethod
    def input(self) -> str:
        """Handle input."""
        raise NotImplementedError("input() should be implemented in subclasses.")

    @abstractmethod
    def output(self, output_str: str) -> None:
        """Handle output."""
        raise NotImplementedError("output() should be implemented in subclasses.")

    @abstractmethod
    def exit(self) -> None:
        """Handle exit."""
        raise NotImplementedError("exit() should be implemented in subclasses.")
