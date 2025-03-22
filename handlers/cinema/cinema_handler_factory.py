from handlers.cinema.check_bookings_handler import CheckBookingsHandler
from handlers.cinema.cinema_handler import CinemaHandler
from handlers.cinema.exit_handler import ExitHandler
from handlers.cinema.ticket_booking_handler import TicketBookingHandler


class CinemaHandlerFactory:
    @staticmethod
    def get_handler(option: str) -> CinemaHandler:
        """Get the handler base on given option to start next steps."""
        match option:
            case "1":
                return TicketBookingHandler()
            case "2":
                return CheckBookingsHandler()
            case "3":
                return ExitHandler()
