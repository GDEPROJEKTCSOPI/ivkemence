import sqlite3
import pandas as pd

# 1. Csatlakozás a meglévő adatbázishoz
path_to_db_df = r'C:\\sql\hutopanelek_betoltes.db'
conn = sqlite3.connect(r'C:\\sql\hutopanelek_betoltes.db')
cursor = conn.cursor()

# 2. 'hutopanelek' tábla létrehozása, ha még nem létezik
cursor.execute('''
    CREATE TABLE IF NOT EXISTS hutopanelek (
    hutopanel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
    )
''')

# 3. Adatok létrehozása és betöltése a 'hutopanelek' táblába
# Panel neveinek generálása "Panel 1" - "Panel 15" formátumban
panel_data = pd.DataFrame({
    'name': [f'Hűtőpanel {i}' for i in range(1, 16)]
})

# Adatok beillesztése a 'hutopanelek' táblába
panel_data.to_sql('hutopanelek', conn, if_exists='append', index=False)

# 4. Kapcsolat lezárása
conn.close()
