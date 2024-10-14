# modulok, könyvtárak,keretrendszerek beolvasása
import sqlite3

# új adatbázis file létrehozása
conn = sqlite3.connect('ivkemence.db')
cursor = conn.cursor()

# táblák hozzáadása az er diagram alapján
cursor.execute('''
    CREATE TABLE adagok (
    adag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    datumido_kezdet DATE NOT NULL,
    datumido_veg DATE NOT NULL,
    koztes_ido INTEGER,
    idotartam INTEGER NOT NULL
    )
''')


cursor.execute('''
    CREATE TABLE hutopanelek (
    hutopanel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE homerseklet (
    homerseklet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    adag_id INTEGER NOT NULL,
    hutopanel_id INTEGER NOT NULL,
    datumido DATE NOT NULL,
    FOREIGN KEY (adag_id) REFERENCES adagok(adag_id),
    FOREIGN KEY (hutopanel_id) REFERENCES hutopanelek(hutopanel_id)
    )
''')

# adatok feltöltése
# bevitt értékek ellenőrzése
# műveletek feldolgása
# adatok feldolgása

# lezárás
conn.commit()

conn.close()