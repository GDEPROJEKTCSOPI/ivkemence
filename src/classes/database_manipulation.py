from src.classes.database_instance import db


def insert_temperature_data(hutopanel_id, adag_id, homerseklet):
    print('Hőmérsékleti adatok beszúrása...')

    df = db.query('''
        SELECT *
        FROM 
        (SELECT COUNT(hutopanel_id) FROM hutopanelek WHERE hutopanel_id = ''' + hutopanel_id +'''),
        (SELECT COUNT(adag_id) FROM adagok WHERE adag_id = ''' + adag_id + ''')
        ;
    ''')

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


def update_example():
    pass


def delete_example():
    pass

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

