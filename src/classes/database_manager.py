import sqlite3
import pandas as pd


class DatabaseManager:

    # Konstruktor ami az adatbázis kapcsolatot létrehozza
    def __init__(self, database_file):
        self.database_file = database_file

        try:
            self.db_connection = sqlite3.connect(self.database_file, timeout=5)
        except Exception as e:
            print(e)
            exit(10)

    # Eljárás commitolni való SQL utasításokhoz (INSERT, UPDATE, DELETE)
    def execute(self, sql: str):
        try:
            self.db_connection.cursor().execute(sql)
            self.db_connection.commit()
        except Exception as e:
            print(e)

    # Eljárás commintolni való tömeges SQL utasításokhoz (INSERT, UPDATE, DELETE)
    def execute_many(self, sql: str, data: list):
        try:
            self.db_connection.cursor().executemany(sql, data)
            self.db_connection.commit()
        except Exception as e:
            print(e)

    # Függvény queryhez, ami egy pandas dataframemel tér vissza (SELECT)
    def query(self, sql: str):
        try:
            return pd.read_sql_query(sql, self.db_connection)
        except Exception as e:
            print(e)
            return None

    def close(self):
        self.db_connection.close()

