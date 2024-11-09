import os.path

from src.classes.database_instance import db
from src.classes.queries import calculate_stat,one_panel_query, two_panel_query, all_panel_query,all_portion_query
import pandas as pd
import matplotlib.pyplot as plt
import time


def display_panel(df,df2=None,adag_id=None,panel_id=None,panel_id_2=None):
    if df is not None and not df.empty:
        print("Lekérdezett hőmérsékleti adatok:")
        print(df)

        df['datumido'] = pd.to_datetime(df['datumido'])

        # Ha csak adag_id van, akkor minden panel hőmérsékletét folyamatos vonallal jelenítjük meg
        if panel_id_2 is None and panel_id is None:
            unique_panels = df['hutopanel_id'].unique()
            colors = plt.cm.get_cmap('tab10', len(unique_panels))  # Különböző színek

            for idx, panel in enumerate(unique_panels):
                panel_data = df[df['hutopanel_id'] == panel]
                plt.plot(panel_data['datumido'], panel_data['homerseklet'],
                         color=colors(idx), label=f'{panel} panel hőmérséklete')

            plt.title(f'{adag_id}. adag hőmérséklete az összes panelen')

            file_suffix = f"osszes_panel_{adag_id}_adag"


        elif panel_id_2 is not None and panel_id is not None:
            unique_panels = df['hutopanel_id'].unique()
            colors = plt.cm.get_cmap('tab10', len(unique_panels))

            for idx, panel in enumerate(unique_panels):
                panel_data = df[df['hutopanel_id'] == panel]
                plt.plot(panel_data['datumido'], panel_data['homerseklet'],
                         color=colors(idx), label=f'{panel} panel hőmérséklete')

            plt.title(f'{adag_id}. adag hőmérséklete {panel_id} és a {panel_id_2} paneleken')
            file_suffix = f"{adag_id}_adag_{panel_id}_es_{panel_id_2}_panelek"

        elif panel_id_2 is None and panel_id is not None:

            plt.plot(df['datumido'], df['homerseklet'], color='b',
                     label=f'{panel_id} panel hőmérséklete')

            if df2 is not None and not df2.empty:
                atlag = df2['atlag'].iloc[0]
                min_temp = df2['min_temp'].iloc[0]
                max_temp = df2['max_temp'].iloc[0]
                median = df['homerseklet'].median()
                modusz = df['homerseklet'].mode()[0]

                plt.axhline(y=atlag, color='#007bff', label='Átlag')
                plt.axhline(y=min_temp, color='#ff5722',  label='Minimum')
                plt.axhline(y=max_temp, color='#9c27b0',  label='Maximum')
                plt.axhline(y=median, color='#8bc34a',  label='Medián')
                plt.axhline(y=modusz, color='#ffeb3b', label='Módusz')

            if adag_id is not None:
                plt.title(f'{adag_id}. adag hőmérséklete a {panel_id}. panelen')
                file_suffix = f"{adag_id}_adag_{panel_id}_panel"
            elif adag_id is None:
                plt.title(f'Összes adag hőmérséklete a {panel_id}. panelen')
                file_suffix = f"osszes_adag_{panel_id}_panel"
            else:
                file_suffix = "unknown_case"


        plt.xlabel("Idő")
        plt.ylabel("Hőmérséklet (°C)")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Kép mentése teljes képernyővel
        plt.savefig(os.path.join(r'../db_creator/output', f'{time.time()}_{file_suffix}_homerseklet.png'),
                    bbox_inches='tight', dpi=300)
        plt.show()

    else:
        print("Nem található ilyen hűtőpanel vagy adag azonosító az adatbázisban.")

def query_temperature_data_use(*args):
    print('.....Hömérsékleti adatok lekérdezése.....')

    df = None
    df2=None

    try:
        if len(args) == 1:
            df = db.query(all_panel_query, (args[0],))
            display_panel(df, adag_id=args[0])

        elif len(args) == 2:
            df = db.query(one_panel_query, (args[0], args[1]))
            df2 = db.query(calculate_stat, (args[0],args[1]))
            display_panel(df, df2=df2, adag_id=args[0], panel_id=args[1])

        elif len(args) == 3:
            df = db.query(two_panel_query, (args[0], args[1],args[0], args[2]))
            display_panel(df, adag_id=args[0], panel_id=args[1], panel_id_2=args[2])
        else:
            print("Túl sok argumentumot adtál meg.")

    except Exception as e:
        print("Hiba történt a lekérdezés során:", e)


def show_panel():
    panel_id = input("Kérjük, adja meg a hutopanel_id-t:")
    adag_id = input("Kérjük, adja meg az adag_id-t:")

    query_temperature_data_use(adag_id, panel_id)
    print('egy panel bemutatása')


def show_two_panel():
    adag_id = input("Kérjük, adja meg az adag_id-t:")
    panel_id = input("Kérjük, adja meg a hutopanel_id-t:")
    panel_id_2 = input("Kérjük, adja meg a másik hutopanel_id-t:")

    query_temperature_data_use(adag_id, panel_id, panel_id_2)
    print('két panel bemutatása')


def show_all_panel():
    adag_id = input("Kérjük, adja meg az adag_id-t:")
    query_temperature_data_use(adag_id)
    print('az összes panel bemutatása')

def show_all_portion():
    panel_id = input("Kérjük, adja meg a hutopanel_id-t:")
    print('.....Hömérsékleti adatok lekérdezése.....')

    df = None

    try:
        df = db.query(all_portion_query, (panel_id,))
        display_panel(df, panel_id=panel_id)

    except Exception as e:
        print("Hiba történt a lekérdezés során:", e)

    print('az összes adag bemutatása az adott penelen')
