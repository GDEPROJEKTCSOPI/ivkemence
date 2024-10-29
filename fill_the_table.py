import sqlite3
import pandas as pd
from datetime import datetime

# Adatbázis létrehozása és csatlakozás
path_to_db = r'ivkemence.db'
conn = sqlite3.connect(r'ivkemence.db')
cursor = conn.cursor()

# 'Hutopanelek' tábla létrehozása és feltöltése
cursor.execute('''
    CREATE TABLE IF NOT EXISTS hutopanelek (
    hutopanel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
    )
''')

# Panel neveinek generálása "Hűtőpanel 1" - "Hűtőpanel 15" formátumban
panel_data = pd.DataFrame({
    'name': [f'Hűtőpanel {i}' for i in range(1, 16)]
})
panel_data.to_sql('hutopanelek', conn, if_exists='append', index=False)

# 'Homerseklet' tábla létrehozása
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Homerseklet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hutopanel_id INTEGER NOT NULL,
    adag_id INTEGER NOT NULL,
    datumido TEXT NOT NULL,
    homerseklet REAL,
    FOREIGN KEY (hutopanel_id) REFERENCES Hutopanelek(hutopanel_id),
    FOREIGN KEY (adag_id) REFERENCES adagok(adag_id)
    )
''')

# hutopanelek_atalakitott.csv fájl betöltése
homerseklet_df = pd.read_csv(r'hutopanelek_atalakitott.csv', delimiter=';')

# Adatok feldolgozása: minden panel oszlopának hozzáadása a megfelelő formátumban
combined_data = []
for panel_id in range(1, 16):  # 1-től 15-ig minden panelre
    time_column = f'Panel hőfok {panel_id} [°C] Time'       # Idő oszlop neve
    value_column = f'Panel hőfok {panel_id} [°C] ValueY'    # Hőmérséklet érték oszlop neve
    if time_column in homerseklet_df.columns and value_column in homerseklet_df.columns:
        temp_data = homerseklet_df[['Adagszam', time_column, value_column]].copy()
        temp_data.columns = ['adag_id', 'datumido', 'homerseklet']  # Oszlopok átnevezése az adatbázis számára
        temp_data['hutopanel_id'] = panel_id  # Minden panelhez a megfelelő ID hozzárendelése
        # a hibás adatokat amik , -vel vannak átalakítjuk hogy ne legyen type hiba
        temp_data['homerseklet'] = temp_data['homerseklet'].str.replace(',', '.').astype(float)
        temp_data['datumido'] = pd.to_datetime(temp_data['datumido'], errors='coerce')
        # Szöveg formátumba alakítás a másodpercek megőrzéséhezS
        temp_data['datumido'] = temp_data['datumido'].dt.strftime('%Y-%m-%d %H:%M:%S')
        combined_data.append(temp_data)

# Az összesített adatokat egy DataFrame-be konvertáljuk
final_data = pd.concat(combined_data, ignore_index=True)
homerseklet_data = final_data[['adag_id', 'hutopanel_id', 'datumido', 'homerseklet']].values.tolist()

# Adatok beszúrása az adatbázisba
cursor.executemany('''
    INSERT INTO Homerseklet (adag_id, hutopanel_id, datumido, homerseklet) VALUES (?, ?, ?, ?)
''', homerseklet_data)

# 'Adagok' tábla létrehozása és feltöltése a CSV fájlból
cursor.execute('''
    CREATE TABLE IF NOT EXISTS adagok (
    adag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_datetime DATE NOT NULL,
    end_datetime DATE NOT NULL,
    koztes_ido INTEGER,
    idotartam INTEGER NOT NULL
    )
''')

# Indexek létrehozása a 'adagok' táblához
cursor.execute('CREATE INDEX IF NOT EXISTS idx_adagok_start_datetime ON adagok(start_datetime);')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_adagok_adag_id ON adagok(adag_id);')

# adagok_atalakitott.csv fájl betöltése és oszlopok átnevezése
adagok_df = pd.read_csv(r'adagok_atalakitott.csv', delimiter=';')
adagok_df = adagok_df.rename(columns={
    'start_datetime': 'start_datetime',
    'end_datetime': 'end_datetime',
    'ADAGKOZI IDO': 'koztes_ido',
    'ADAGIDO': 'idotartam'
})
adagok_data = adagok_df[['start_datetime', 'end_datetime', 'koztes_ido', 'idotartam']]
adagok_data.to_sql('adagok', conn, if_exists='append', index=False)

# Változások mentése és kapcsolat lezárása
conn.commit()
conn.close()
print("Adatok sikeresen betöltve mindhárom táblába, a 'datumido' egységes formátumban került az adatbázisba.")
