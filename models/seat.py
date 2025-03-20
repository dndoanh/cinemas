import utils.constants as consts


class Seat:

    def __init__(self, row: int, col: int, state: str) -> None:
        """Initialize an object of the seat.
        Args:
            row (int): the row index of the seat
            col (int): the column index of the seat
            state (str): a string to represent the state of the seat.
                The state must be one of following: Empty, Reserved, Booked
        """
        self.row = row
        self.col = col
        if state not in [consts.SEAT_STATE_EMPTY, consts.SEAT_STATE_RESERVED, consts.SEAT_STATE_BOOKED]:
            raise ValueError("Invalid seat state. The seat state must be one of [Empty, Reserved, Booked].")
        self.state = state

    def __eq__(self, other) -> bool:
        """Do compare the seat with another based on whether same row index and column index or not.
        Args:
             other (Seat): another seat to compare.
        Returns:
            a boolean value to indicate same seat or not.
        """
        return self.row == other.row and self.col == other.col

    def __str__(self) -> str:
        """Do represent the string of the seat.
        If the state is Empty, then display dot symbol(.).
        If the state is Reserved, then display character o.
        If the state is Empty, then display sharp symbol(#).

        Returns:
            a string value to represent the state for display.
        """
        if self.state == consts.SEAT_STATE_EMPTY:
            return consts.DISPLAY_EMPTY
        elif self.state == consts.SEAT_STATE_RESERVED:
            return consts.DISPLAY_RESERVED
        else:
            return consts.DISPLAY_BOOKED

    def update_state(self, new_state: str) -> None:
        """Do update the state of the seat to new state.
        Args:
            new_state(str): new state of the seat.
        """
        if new_state not in [consts.SEAT_STATE_EMPTY, consts.SEAT_STATE_RESERVED, consts.SEAT_STATE_BOOKED]:
            raise ValueError("Invalid seat state. The seat state must be one of [Empty, Reserved, Booked].")
        self.state = new_state
