import math
from abc import ABC, abstractmethod
from .SQLiteDatabase import SQLiteDatabase
from .sql_structure import get_average_event_intensity


class LengthHeuristic(ABC):
    def __init__(self, database: SQLiteDatabase):
        self.__database = database

    @property
    def _database(self) -> SQLiteDatabase:
        return self.__database

    @abstractmethod
    def max_allowed_time(self) -> float:
        pass

    @abstractmethod
    def session_type(self) -> str:
        pass


class RLengthHeuristic(LengthHeuristic):
    def __init__(self, navigation_ratio: float, database: SQLiteDatabase):
        super().__init__(database)
        self.__navigation_ratio = navigation_ratio
        self.__average_event_intensity = self._database.cursor.execute(get_average_event_intensity()).fetchone()[0]

    def max_allowed_time(self) -> float:
        return - math.log(1 - self.__navigation_ratio) / self.__average_event_intensity

    def session_type(self) -> str:
        return 'session_id_rlength'


class STTQLengthHeuristic(LengthHeuristic):
    def __init__(self, stt_q: float, database: SQLiteDatabase):
        super().__init__(database)
        self.__stt_q = stt_q

    def max_allowed_time(self) -> float:
        return self.__stt_q

    def session_type(self) -> str:
        return 'session_id_sttq'
