from enum import Enum


class AlertType:
    InvalidDateShort = 13
    CancelSuccessful = 11
    DayFull = 0
    InvalidName = 1
    InvalidNumberOfReservation = 2
    InvalidDate = 3
    DateFromThePast = 4
    DateTooClose = 5
    NotANumber = 6
    NumberOutOfRange = 7
    Success = 8
    DateTooCloseToCancel = 9
    ReservationDoesntExist = 10
