from src.classes.database_instance import db
from src.classes.queries import panel_query,two_panel_query,all_panel_query

def query_temperature_data_use(adag_id, *args):
    print('.....Hömérsékleti adatok lekérdezése.....')

    try:
        if len(args) == 0:
            df = db.query(all_panel_query, (adag_id,))
        elif len(args) == 1:
            df = db.query(panel_query, (adag_id, args[0]))
        elif len(args) == 3:
            df = db.query(two_panel_query, (adag_id, args[0], args[1], args[2]))
        else:
            print("Túl sok argumentumot adtál meg.")

        if df is not None and not df.empty:
            print("Lekérdezett hőmérsékleti adatok:")
            print(df)
        else:
            print("Nem található ilyen hűtőpanel vagy adag azonosító az adatbázisban.")

    except Exception as e:
        print("Hiba történt a lekérdezés során:", e)
def show_panel():
    panel_id = input("Kérjük, adja meg a hutopanel_id-t:")
    adag_id = input("Kérjük, adja meg az adag_id-t:")

    query_temperature_data_use(adag_id,panel_id)
    print('egy panel bemutatása')
def show_two_panel():
    panel_id = input("Kérjük, adja meg a hutopanel_id-t:")
    adag_id = input("Kérjük, adja meg az adag_id-t:")
    panel_id_2 = input("Kérjük, adja meg a másik hutopanel_id-t:")
    adag_id_2 = input("Kérjük, adja meg a másik adag_id-t:")

    query_temperature_data_use( adag_id,panel_id,adag_id_2,panel_id_2)
    print('két panel bemutatása')
def show_all_panel():
    adag_id = input("Kérjük, adja meg az adag_id-t:")
    query_temperature_data_use(adag_id)
    print('az összes panel bemutatása')

