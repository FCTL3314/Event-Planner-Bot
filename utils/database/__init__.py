import utils.database.sqlite_database

from data.config import db_route

database = sqlite_database.SQLiteDatabase(db_route)
