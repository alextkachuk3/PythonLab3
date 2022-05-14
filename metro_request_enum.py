from enum import Enum


class MetroRequest(Enum):
    ADD_LINE = 1
    DELETE_LINE = 2
    ADD_STATION = 3
    DELETE_STATION = 4
    UPDATE_STATION = 5
    FIND_STATION_BY_NAME = 6
    COUNT_OF_LINE_STATIONS = 7
    LIST_OF_LINE_STATIONS = 8
    LIST_OF_LINES = 9
