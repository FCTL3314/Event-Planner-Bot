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

    def create_tables(self):
        self.__cur.execute("""
        CREATE TABLE IF NOT EXISTS channels (
        channel_id PRIMARY KEY,
        channel_name text)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS groups (
        group_id PRIMARY KEY,
        group_name text)""")

    def add_channel(self, channel_id, channel_name):
        self.__cur.execute(f"""
        INSERT INTO channels (channel_id, channel_name) VALUES ({channel_id}, '{channel_name}')""")

    def remove_channel(self, channel_id):
        self.__cur.execute(f"""DELETE FROM channels WHERE channel_id = {channel_id}""")

    def add_group(self, group_id, group_name):
        self.__cur.execute(f"""
                INSERT INTO groups (group_id, group_name) VALUES ({group_id}, '{group_name}')""")

    def remove_group(self, group_id):
        self.__cur.execute(f"""DELETE FROM groups WHERE group_id = {group_id}""")

    def get_channels(self):
        self.__cur.execute(f"""SELECT * FROM channels""")
        return self.__cur.fetchall()

    def get_groups(self):
        self.__cur.execute(f"""SELECT * FROM groups""")
        return self.__cur.fetchall()
