import os.path

from src.classes.database_instance import db
from src.classes.queries import one_panel_query, two_panel_query, all_panel_query
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def display_panel(df,adag_id=None,panel_id=None,adag_id_2=None,panel_id_2=None):
    if df is not None and not df.empty:
        print("Lekérdezett hőmérsékleti adatok:")
        print(df)

        df['datumido'] = pd.to_datetime(df['datumido'])

        # Ha csak adag_id van, akkor minden panel hőmérsékletét folyamatos vonallal jelenítjük meg
        if panel_id_2 is None:
            unique_panels = df['hutopanel_id'].unique()
            colors = plt.cm.get_cmap('tab10', len(unique_panels))  # Különböző színek

            for idx, panel in enumerate(unique_panels):
                panel_data = df[df['hutopanel_id'] == panel]
                plt.plot(panel_data['datumido'], panel_data['homerseklet'],
                         color=colors(idx), label=f'{panel} panel hőmérséklete')

            plt.title(f'{adag_id}. adag hőmérséklete - Összes panel')

        # Ha van adag_id és hutopanel_id, megjelenítjük a mediánt, móduszt és átlagot
        elif panel_id is not None:

            plt.plot(df['datumido'], df['homerseklet'], color='b',
                     label=f'{panel_id} panel hőmérséklete')

            avg_temp = df['homerseklet'].mean()
            median_temp = df['homerseklet'].median()
            mode_temp = df['homerseklet'].mode()[0]

            plt.axhline(y=avg_temp, color='orange', linestyle='--', label='Átlag')
            plt.axhline(y=median_temp, color='green', linestyle='--', label='Medián')
            plt.axhline(y=mode_temp, color='purple', linestyle='--', label='Módusz')

            plt.title(f'{adag_id}. adag hőmérséklete a {panel_id}. panelen')


        plt.xlabel("Idő")
        plt.ylabel("Hőmérséklet (°C)")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Kép mentése teljes képernyővel
        plt.savefig(os.path.join(r'../db_creator/output', f'adag_{adag_id}_panelek_homerseklet.png'),
                    bbox_inches='tight', dpi=300)
        plt.show()
    else:
        print("Nem található ilyen hűtőpanel vagy adag azonosító az adatbázisban.")

def query_temperature_data_use(adag_id, *args):
    print('.....Hömérsékleti adatok lekérdezése.....')

    df = None

    try:
        if len(args) == 0:
            df = db.query(all_panel_query, (adag_id,))
            display_panel(df, adag_id)

        elif len(args) == 1:
            df = db.query(one_panel_query, (adag_id, args[0]))
            display_panel(df, adag_id, args[0])

        elif len(args) == 3:
            df = db.query(two_panel_query, (adag_id, args[0], args[1], args[2]))
            display_panel(df, adag_id, args[0], args[1], args[2])
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
    panel_id = input("Kérjük, adja meg a hutopanel_id-t:")
    adag_id = input("Kérjük, adja meg az adag_id-t:")
    panel_id_2 = input("Kérjük, adja meg a másik hutopanel_id-t:")
    adag_id_2 = input("Kérjük, adja meg a másik adag_id-t:")

    query_temperature_data_use(adag_id, panel_id, adag_id_2, panel_id_2)
    print('két panel bemutatása')


def show_all_panel():
    adag_id = input("Kérjük, adja meg az adag_id-t:")
    query_temperature_data_use(adag_id)
    print('az összes panel bemutatása')
