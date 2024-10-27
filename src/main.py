from src.classes.database_manager import DatabaseManager

DB_PATH = 'database/ivkemence.db'

# Főprogram indítás

# Adatbázis objektum inicializálás
db_connection = DatabaseManager(database_file=DB_PATH)

df = db_connection.query("SELECT * FROM adagok;")


if df is not None:
    print(df)

db_connection.close()
