from handlers.booking_handler import BookingHandler


def main() -> None:
    handler = BookingHandler()
    handler.start()


if __name__ == "__main__":
    main()
