from src.classes.database_instance import db


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


def delete_temperature_data(id):
    """
    Törli a hőmérsékleti adatot az adatbázisból a megadott id alapján.
    Visszatérési érték: True, ha a törlés sikeres volt, különben False.
    """
    try:
        # Id létezésének ellenőrzése
        df = db.query('''
            SELECT COUNT(id) as count 
            FROM homerseklet 
            WHERE id = ''' + id + ''';
        ''')

        if df.at[0, "count"] < 1:
            print("Nincs törölhető adat a megadott azonosítóval.")
            return False

        # Törlés végrehajtása
        db.execute('''
            DELETE FROM homerseklet 
            WHERE id = ''' + id + ''';
        ''')

        # Sikeres törlés üzenet kiírása, ha a törlés megtörtént
        print("A megadott hőmérsékleti adat sikeresen törölve.")
        return True

    except Exception as e:
        print(f"Hiba történt a törlés során: {e}")
        return False


