import utils.database.sqlite_database

from data.config import DB_ROUTE

database = sqlite_database.SQLiteDatabase(DB_ROUTE)
