from src.classes.database_instance import db


def query_portion_data():
    print('Elérhető adag adatok lekérdezése')

    try:
        df = db.query('''
            SELECT DISTINCT adag_id, start_datetime, end_datetime
            FROM adagok
        ''')

        if df is not None and not df.empty:
            print("Lekérdezhető adagok:")
            print(df)
        else:
            print("Nem található adat.")

    except Exception as e:
        print("Hiba történt a lekérdezés során:", e)

def query_panel_data():
    print('Elérhető panel adatok lekérdezése')

    df=db.query('''
        SELECT * 
        FROM hutopanelek
    ''')

    if df is not None and not df.empty:
        print("Lekérdezhető panelek:")
        print(df)
    else:
        print("Nem található ilyen hűtőpanel az adatbázisban.")

def query_temperature_data(hutopanel_id, adag_id):
    print('Hömérsékleti adatok lekérdezése')

    try:
        df = db.query('''
            SELECT * 
            FROM homerseklet
            WHERE hutopanel_id = ? AND adag_id = ?        
        ''', (hutopanel_id, adag_id))

        if df is not None and not df.empty:
            print("Lekérdezett hőmérsékleti adatok:")
            print(df)
        else:
            print("Nem található ilyen hűtőpanel vagy adag azonosító az adatbázisban.")

    except Exception as e:
        print("Hiba történt a lekérdezés során:", e)

def insert_temperature_data(hutopanel_id, adag_id, homerseklet):
    print('Hőmérsékleti adatok beszúrása...')

    df = db.query('''
        SELECT *
        FROM 
        (SELECT COUNT(hutopanel_id) FROM hutopanelek WHERE hutopanel_id = ''' + hutopanel_id +'''),
        (SELECT COUNT(adag_id) FROM adagok WHERE adag_id = ''' + adag_id + ''');
    ''')

    if df is not None:
        if df.at[0, "COUNT(hutopanel_id)"] < 1:
            print("Nem található ilyen hűtőpanel azonosító az adatbázisban")
            return

        if df.at[0, "COUNT(adag_id)"] < 1:
            print("Nem található ilyen adag azonosító az adatbázisban")
            return

        db.execute('''
            INSERT INTO homerseklet 
                (hutopanel_id, adag_id, datumido, homerseklet)
            VALUES 
                (''' + hutopanel_id + ''', ''' + adag_id + ''', datetime(), ''' + homerseklet + ''');
        ''')


def update_temperature_data(id, homerseklet):
    print('Hőmérsékleti adat felülírása...')

    df = db.query('''
        SELECT COUNT(id) FROM homerseklet WHERE id = ''' + id + ''';
    ''')

    if df is not None:
        if df.at[0, "COUNT(id)"] < 1:
            print("Nem található ilyen azonosító az adabázisban")
            return

        db.execute('''
            UPDATE homerseklet
            SET homerseklet = ''' + homerseklet + '''
            WHERE id = ''' + id + '''
        ''')


def delete_temperature_data(hutopanel_id, adag_id):
    """
    Törli a hőmérsékleti adatot az adatbázisból a megadott hutopanel_id és adag_id alapján.
    Visszatérési érték: True, ha a törlés sikeres volt, különben False.
    """
    try:
        # Hűtőpanel és adag azonosítók létezésének ellenőrzése
        df = db.query('''
            SELECT COUNT(*) as count 
            FROM homerseklet 
            WHERE hutopanel_id = ''' + hutopanel_id + ''' AND adag_id = ''' + adag_id + ''';
        ''')

        if df.at[0, "count"] < 1:
            print("Nincs törölhető adat a megadott azonosítókkal.")
            return False

        # Törlés végrehajtása
        db.execute('''
            DELETE FROM homerseklet 
            WHERE hutopanel_id = ''' + hutopanel_id + ''' AND adag_id = ''' + adag_id + ''';
        ''')

        # Sikeres törlés üzenet kiírása itt, a törlés után
        print("A megadott hőmérsékleti adat sikeresen törölve.")
        return True

    except Exception as e:
        print(f"Hiba történt a törlés során: {e}")
        return False

