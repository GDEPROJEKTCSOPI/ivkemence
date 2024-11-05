import pandas as pd
import sqlite3

db_path = r'output/ivkemence.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

kuszob = 70

cursor.execute('''
    SELECT DISTINCT hutopanel_id, adag_id 
    FROM homerseklet
''')
valid_combinations = cursor.fetchall()

log_file_path = "torolt_rekordok.txt"
with open(log_file_path, "w") as log_file:
    log_file.write("Törölt rekordok\n")
    log_file.write("=" * 40 + "\n")

for hutopanel_id, adag_id in valid_combinations:
    print(f'hutopanel : {hutopanel_id}, adag:  {adag_id}')

    cursor.execute('''
              SELECT homerseklet 
              FROM homerseklet
              WHERE adag_id = ? AND hutopanel_id = ?
          ''', (adag_id, hutopanel_id))

    # Collect the temperature values in a list
    homerseklet_list = [row[0] for row in cursor.fetchall()]

    df = pd.DataFrame(homerseklet_list,columns=['homerseklet'])
    avg = df['homerseklet'].mean()

    intervallum = avg * (kuszob/100)
    also_kuszob = avg - intervallum
    felso_kuszob = avg + intervallum


    cursor.execute('''
            SELECT * FROM homerseklet
            WHERE (homerseklet < ? OR homerseklet > ?)
            AND adag_id = ? AND hutopanel_id = ?;
        ''', (also_kuszob, felso_kuszob, adag_id, hutopanel_id))
    deleted_records = cursor.fetchall()

    with open(log_file_path, "a") as log_file:
        if deleted_records:
            with open(log_file_path, "a") as log_file:
                log_file.write(f"Deleted records for hutopanel_id {hutopanel_id}, adag_id {adag_id}:\n")
                log_file.write(f"Also küszöb: {also_kuszob:.2f}, Felso küszöb: {felso_kuszob:.2f}\n")
                for record in deleted_records:
                    log_file.write(f"{record}\n")
        else:
           continue

    cursor.execute('''
        DELETE FROM homerseklet
        WHERE (homerseklet < ? OR homerseklet > ?)
        AND adag_id = ? AND hutopanel_id = ?;
    ''', (also_kuszob, felso_kuszob, adag_id, hutopanel_id))

conn.commit()
conn.close()

