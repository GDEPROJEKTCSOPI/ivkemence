import sqlite3
import pandas as pd

#Adatbázis létrehozása és csatlakozás
path_to_db_df = r'C:\\sql\homerseklet_betoltes.db'
conn = sqlite3.connect(r'C:\\sql\homerseklet_betoltes.db')
cursor = conn.cursor()

#'Homerseklet' tábla létrehozása, most az id oszloppal
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Homerseklet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hutopanel_id INTEGER NOT NULL,
    adag_id INTEGER NOT NULL,
    datumido DATE NOT NULL,
    homerseklet REAL,
    FOREIGN KEY (hutopanel_id) REFERENCES Hutopanelek(id),
    FOREIGN KEY (adag_id) REFERENCES Adag(id)
    )
''')

#'hutopanelek_atalakitott.csv' fájl betöltése
homerseklet_df = pd.read_csv(r'C:\Users\VG\Desktop\adatbeemeles\hutopanelek_atalakitott.csv', delimiter=';')

#Adatok feldolgozása: minden panel oszlopának hozzáadása a megfelelő formátumban
combined_data = []
for panel_id in range(1, 16):  # 1-től 15-ig minden panelre
    time_column = f'Panel hőfok {panel_id} [°C] Time'       # Idő oszlop neve
    value_column = f'Panel hőfok {panel_id} [°C] ValueY'    # Hőmérséklet érték oszlop neve
    if time_column in homerseklet_df.columns and value_column in homerseklet_df.columns:
        temp_data = homerseklet_df[['Adagszam', time_column, value_column]].copy()
        temp_data.columns = ['adag_id', 'datumido', 'homerseklet']  # Oszlopok átnevezése az adatbázis számára
        temp_data['hutopanel_id'] = panel_id  # Minden panelhez a megfelelő ID hozzárendelése
        combined_data.append(temp_data)

#Az összesített adatokat egy DataFrame-be konvertáljuk
final_data = pd.concat(combined_data, ignore_index=True)

#Adatok beillesztése a 'Homerseklet' táblába
#'datumido' és 'homerseklet' oszlopokat is beillesztése
homerseklet_data = final_data[['adag_id', 'hutopanel_id', 'datumido', 'homerseklet']].values.tolist()

cursor.executemany('''
    INSERT INTO Homerseklet (adag_id, hutopanel_id, datumido, homerseklet) VALUES (?, ?, ?, ?)
''', homerseklet_data)
print(f"{len(homerseklet_data)} rekord lett beszúrva a 'homerseklet' táblába.")

# Változások mentése és kapcsolat lezárása
conn.commit()
conn.close()
