#datumido tizedes javítás
#1 python
import sqlite3

db_path = r'C:\\sql\betoltes_egyben2.db'
conn = sqlite3.connect(r'C:\\sql\betoltes_egyben2.db')
cursor = conn.cursor()

cursor.execute('''
    UPDATE Homerseklet
    SET homerseklet = ROUND(homerseklet, 1)
''')

conn.commit()
conn.close()

#sql
UPDATE Homerseklet
SET homerseklet = ROUND(homerseklet, 1);

#0-90 fok
#keresés
SELECT id, homerseklet
FROM Homerseklet
WHERE homerseklet < 0 OR homerseklet > 90;

#módosítás
UPDATE Homerseklet
SET homerseklet = 0
WHERE homerseklet < 0 OR homerseklet > 90;

#törlés
DELETE FROM Homerseklet
WHERE homerseklet < 0 OR homerseklet > 90;
