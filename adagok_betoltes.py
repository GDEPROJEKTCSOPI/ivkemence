import sqlite3
import pandas as pd

# 1. Adatbázis létrehozása és csatlakozás
# Új adatbázis fájl létrehozása
path_to_db_df = r'C:\\sql\adagok_beemelese.db'
conn = sqlite3.connect(r'C:\\sql\adagok_beemelese.db')
cursor = conn.cursor()

# 2. Táblák létrehozása az ER diagram alapján
cursor.execute('''
    CREATE TABLE IF NOT EXISTS adagok (
    adag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_datetime DATE NOT NULL,
    end_datetime DATE NOT NULL,
    koztes_ido INTEGER,
    idotartam INTEGER NOT NULL
    )
''')

# Index létrehozása a keresési teljesítmény növelése érdekében
cursor.execute('CREATE INDEX IF NOT EXISTS idx_adagok_start_datetime ON adagok(start_datetime);')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_adagok_adag_id ON adagok(adag_id);')

# 3. Adatok betöltése az 'adagok_atalakitott.csv' fájlból
# CSV betöltése és oszlopok átnevezése a tábla struktúrájának megfelelően
adagok_df = pd.read_csv(r'C:\Users\VG\Desktop\adatbeemeles/adagok_atalakitott.csv', delimiter=';')
adagok_df = adagok_df.rename(columns={
    'start_datetime': 'start_datetime',
    'end_datetime': 'end_datetime',
    'ADAGKOZI IDO': 'koztes_ido',
    'ADAGIDO': 'idotartam'
})
adagok_data = adagok_df[['start_datetime', 'end_datetime', 'koztes_ido', 'idotartam']]

# 4. Adatok beillesztése az 'adagok' táblába (adag_id nélkül, mivel az automatikus)
adagok_data.to_sql('adagok', conn, if_exists='append', index=False)

# 5. Kapcsolat lezárása
conn.close()
