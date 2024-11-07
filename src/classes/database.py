import sqlite3
import pandas as pd


class Database:

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
            cursor = self.db_connection.cursor()
            cursor.execute(sql)

            self.db_connection.commit()

            print("Érintett sorok száma: " + str(cursor.rowcount))

            cursor.close()
        except Exception as e:
            print(e)

    # Eljárás commintolni való tömeges SQL utasításokhoz (INSERT, UPDATE, DELETE)
    def execute_many(self, sql: str, data: list):
        try:
            cursor = self.db_connection.cursor()
            cursor.executemany(sql, data)

            self.db_connection.commit()

            print("Érintett sorok száma: " + str(cursor.rowcount))

            cursor.close()
        except Exception as e:
            print(e)

    def execute_transaction(self, *sql: str):
        try:
            cursor = self.db_connection.cursor()

            cursor.execute('BEGIN TRANSACTION;')
            for statement in sql:
                cursor.execute(statement)
            self.db_connection.commit()

            print("Érintett sorok száma: " + str(cursor.rowcount))
        except Exception as e:
            self.db_connection.rollback()

            print("Tranzakció sikertelen")
            print(e)
        finally:
            cursor.close()

    # Függvény queryhez, ami egy pandas dataframemel tér vissza (SELECT)
    def query(self, sql: str, params=None):
        try:
            return pd.read_sql_query(sql, self.db_connection, params=params)
        except Exception as e:
            print(e)
            return None

    def close(self):
        self.db_connection.close()

