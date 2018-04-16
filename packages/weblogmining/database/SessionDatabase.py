import pandas, math
from .SQLiteDatabase import SQLiteDatabase
from .sql_structure import *
from .sql_data_helper.get_web_mining_rlength import get_length, get_user_id, get_id, get_unixtime


class SessionDatabase(object):
    def __init__(self, database: SQLiteDatabase):
        self.__database = database

    def load_data(self, input_file: str, stt_seconds: int) -> None:
        self.__drop_structure()
        self.__create_structure()

        df = pandas.read_table(input_file, header=None,
                               names=['ip', 'cookie', 'dtime', 'unixtime', 'request_method', 'url', 'http_version',
                                      'status_code', 'referrer', 'agent'])
        df.to_sql('web_mining', self.__database.connection, if_exists='append', index=False)
        self.__database.connection.commit()

        self.__pos_processing(stt_seconds)

    def rlength_heuristic(self, navigation_ratio: float) -> None:
        data = self.__database.cursor.execute(get_web_mining_rlength()).fetchall()

        average_event_intensity = self.__database.cursor.execute(get_average_event_intensity()).fetchone()[0]
        c = - math.log(1 - navigation_ratio) / average_event_intensity

        session_id = 1
        group_ids = []
        current_user_id = get_user_id(data[0])

        for item in data:
            if get_user_id(item) != current_user_id:
                if len(group_ids) > 0:
                    self.__database.cursor.execute(update_web_mining_session_id(session_id, group_ids))
                    group_ids = []
                current_user_id = get_user_id(item)
                session_id = 1

            group_ids.append(get_id(item))

            if get_length(item) is None or get_length(item) > c:
                self.__database.cursor.execute(update_web_mining_session_id(session_id, group_ids))
                session_id += 1
                group_ids = []

        if len(group_ids) > 0:
            print(group_ids)
            print("Error rlength_heuristic")

        self.__database.connection.commit()

    def __drop_structure(self) -> None:
        self.__database.executescript(drop_tables())

    def __create_structure(self) -> None:
        self.__database.executescript(create_tables())

    def __pos_processing(self, stt_seconds: int) -> None:
        self.__database.executescript(web_mining_fill_user_id())
        self.__database.executescript(web_mining_fill_length(stt_seconds))
