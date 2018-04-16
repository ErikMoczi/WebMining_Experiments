import sqlite3, atexit


class SQLiteDatabase(object):
    def __init__(self, database_location: str, database_name: str = 'example.db'):
        self.__connection = sqlite3.connect(database_location + '/' + database_name)

        atexit.register(self.__clean_up)

    def __clean_up(self) -> None:
        self.__connection.commit()
        self.__connection.close()

    def executescript(self, sql_script: str) -> None:
        self.__connection.executescript(sql_script)
        self.__connection.commit()

    @property
    def connection(self) -> sqlite3.Connection:
        return self.__connection

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self.__connection.cursor()
