import sqlite3


class SQLiteDatabase:
    def __init__(self, route):
        self.__conn = sqlite3.connect(database=route)
        self.__cur = self.__conn.cursor()
        self._connected = True

    def __enter__(self):
        if not self._connected:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._connected:
            self.__cur.close()
            if isinstance(exc_value, Exception):
                self.__conn.rollback()
            else:
                self.__conn.commit()
            self.__conn.close()
            self._connected = False

    def connect(self):
        self.__conn = sqlite3.connect(database=r'utils/database/bot_data.dat')
        self.__cur = self.__conn.cursor()
        self._connected = True

    def execute(self, query: str):
        self.__cur.execute(f"""{query}""")
        return self.__cur.fetchall()

    def create_tables(self):
        self.__cur.execute("""
        CREATE TABLE IF NOT EXISTS channels (
        channel_id PRIMARY KEY,
        channel_name text)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS groups (
        group_id PRIMARY KEY,
        group_name text)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS event_votes (
        chat_id bigint,
        message_id bigint,
        user_id bigint,
        first_name text,
        last_name text,
        vote varchar(16))""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS event_data (
        chat_id bigint,
        message_id bigint,
        event_name text,
        fire_button_count int,
        think_button_count int,
        fire_button_limit int,
        link_button_url text,
        link_button_name text,
        creation_date datatime)""")
