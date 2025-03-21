from typing import List

import utils.constants as consts
from models.seat import Seat


class Booking:
    def __init__(self, booking_id: str, status: str, seats: List[Seat]):
        """Initialize an object of the booking.
        Args:
            booking_id(str): unique identifier of the booking.
            status(str): the state of the booking. Either Reserved or Confirmed.
            seats([Seat]): the list of seats belong to the booking.
                If booking status is Reserved, then all seat's state must be Reserved.
                If booking status is Confirmed, then all seat's state must be Booked.
        """
        if booking_id is None or booking_id == "":
            raise ValueError("Invalid booking id. Booking id must be not blank.")
        self.booking_id = booking_id
        if status not in [
            consts.BOOKING_STATUS_RESERVED,
            consts.BOOKING_STATUS_CONFIRMED,
        ]:
            raise ValueError(
                "Invalid booking status. The status must be either Reserved or Confirmed."
            )
        self.status = status
        if status == consts.BOOKING_STATUS_RESERVED and any(
            [seat for seat in seats if seat.state != consts.SEAT_STATE_RESERVED]
        ):
            raise ValueError(
                "Invalid booking seats. For Reserved booking, all seat's state must be Reserved."
            )
        if status == consts.BOOKING_STATUS_CONFIRMED and any(
            [seat for seat in seats if seat.state != consts.SEAT_STATE_BOOKED]
        ):
            raise ValueError(
                "Invalid booking seats. For Confirmed booking, all seat's state must be Booked."
            )
        self.seats = seats

    def update_status(self, new_status: str) -> None:
        """Do update status of the booking.
            If new status is Reserved, do update the state to Reversed for all seats.
            If new status is Confirmed, do update the state to Booked for all seats.
        Args:
            new_status(str): the new status of the booking.
        """
        if new_status not in [
            consts.BOOKING_STATUS_RESERVED,
            consts.BOOKING_STATUS_CONFIRMED,
        ]:
            raise ValueError(
                "Invalid booking status. The status must be either Reserved or Confirmed."
            )
        self.status = new_status
        new_seat_state = (
            consts.SEAT_STATE_RESERVED
            if new_status == consts.BOOKING_STATUS_RESERVED
            else consts.SEAT_STATE_BOOKED
        )
        for seat in self.seats:
            seat.update_state(new_seat_state)

    def release_reserved_seats(self) -> None:
        """Do release reserved seats
        Args:
            new_status(str): the new status of the booking.
        """
        for seat in self.seats:
            seat.update_state(consts.SEAT_STATE_EMPTY)

    def update_seats(self, new_seats: List[Seat]) -> None:
        """Do update seats with the new list.
        Args:
            new_seats(List[Seat]): the new list of seats.
        """
        self.seats = new_seats
