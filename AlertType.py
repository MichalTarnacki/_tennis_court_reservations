from enum import Enum


class AlertType:
    DayFull = 0
    InvalidName = 1
    InvalidNumberOfReservation = 2
    InvalidDate = 3
    DateFromThePast = 4
    DateTooClose = 5
    NotANumber = 6
    NumberOutOfRange = 7
