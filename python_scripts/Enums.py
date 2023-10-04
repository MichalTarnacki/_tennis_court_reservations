from enum import Enum


class DataType(Enum):
    AnyInput = 9
    FileName = 8
    FileFormat = 7
    DaysToPrint = 6
    Continue = 5
    Name = 1
    Date = 2
    Duration = 3
    DateCancel = 4


class AlertType:
    SaveSuccessful = 17
    WrongDateOrder = 16
    InvalidFormat = 15
    FileAlreadyExists = 14
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


class ActionOption(Enum):
    Make = 1
    Cancel = 2
    Print = 3
    Save = 4
    Exit = 5
