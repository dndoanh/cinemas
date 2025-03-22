from handlers.booking_handler import BookingHandler


def main() -> None:
    booking_handler = BookingHandler()
    booking_handler.run()


if __name__ == "__main__":
    main()
