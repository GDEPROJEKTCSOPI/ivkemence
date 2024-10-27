#datumido tizedes javítás
#1 python
import sqlite3

path_to_db = r'output/ivkemence.db'
conn = sqlite3.connect(path_to_db)
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
