MSG_BEGIN = (
    "Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:"
)
MSG_WELCOME = "Welcome to GIC Cinemas\n[1] Book tickets for {movie_title} ({seats_available} seats available)\n[2] Check bookings\n[3] Exit\nPlease enter your selection:"
MSG_INPUT_NUMBER_OF_TICKETS = (
    "Enter number of tickets to book, or enter blank to go back to main menu:"
)
MSG_INPUT_SEATING_POSITION = (
    "Enter blank to accept seat selection, or enter new seating position:"
)
MSG_INPUT_BOOKING_ID = "Enter booking id, or enter blank to go back to main menu:"
MSG_OUTPUT_SUCCESSFULLY_RESERVED = (
    "Successfully reserved {num_tickets} {movie_title} tickets."
)
MSG_OUTPUT_BOOKING_ID = "Booking id: {booking_id}"
MSG_OUTPUT_BOOKING_CONFIRMED = "Booking id: {booking_id} confirmed."
MSG_OUTPUT_GOODBYE = "Thank you for using GIC Cinemas system. Bye!"
MSG_INVALID_MOVIE_TITLE_ROWS_SEATS_PER_ROW = (
    "Invalid movie title or rows or seats per row. Please try again."
)
MSG_INVALID_MENU_SELECTION = "Invalid menu selection. Please try again."
MSG_INVALID_NUMBER_OF_TICKETS = "Invalid number of tickets. Please try again."
MSG_INVALID_SEATING_POSITION = "Invalid seating position. Please try again."
MSG_INVALID_BOOKING_ID = "Invalid booking id. Please try again."
MSG_NOT_EXIST_BOOKING_ID = "Booking id [{booking_id}] does not exist. Please try again."
MSG_INVALID_EXCEEDING_NUMBER_OF_TICKETS = (
    "Sorry, there are only {num_seats} seats available."
)
MSG_INVALID_STATE = (
    "Invalid seat state. The seat state must be one of [Empty, Reserved, Booked]."
)
MSG_INVALID_STATUS = (
    "Invalid booking status. The status must be either Reserved or Confirmed."
)
MSG_INVALID_STATUS_RESERVED = (
    "Invalid booking seats. For Reserved booking, all seat's state must be Reserved."
)
MSG_INVALID_STATUS_CONFIRMED = (
    "Invalid booking seats. For Confirmed booking, all seat's state must be Booked."
)
MSG_INVALID_NO_EMPTY_SEAT = "There is no Empty seat."
MSG_INFO_SELECTED_SEATS = "Selected seats:\n"
MSG_INFO_SCREEN = "SCREEN"
