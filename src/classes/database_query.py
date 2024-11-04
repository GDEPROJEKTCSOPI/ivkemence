
from src.classes.database_instance import db
from src.classes.queries import portion_query,temp_query,panel_query
def query_portion_data():
    print('Elérhető adag adatok lekérdezése')

    try:
        df = db.query(portion_query)

        if df is not None and not df.empty:
            print("Lekérdezhető adagok:")
            print(df)
        else:
            print("Nem található adat.")

    except Exception as e:
        print("Hiba történt a lekérdezés során:", e)

def query_panel_data():
    print('Elérhető panel adatok lekérdezése')

    df=db.query(panel_query)

    if df is not None and not df.empty:
        print("Lekérdezhető panelek:")
        print(df)
    else:
        print("Nem található ilyen hűtőpanel az adatbázisban.")

def query_temperature_data(hutopanel_id, adag_id):
    print('Hömérsékleti adatok lekérdezése')

    try:
        df = db.query(temp_query, (hutopanel_id, adag_id))

        if df is not None and not df.empty:
            print("Lekérdezett hőmérsékleti adatok:")
            print(df)
        else:
            print("Nem található ilyen hűtőpanel vagy adag azonosító az adatbázisban.")

    except Exception as e:
        print("Hiba történt a lekérdezés során:", e)
