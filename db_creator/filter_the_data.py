import pandas as pd
import sqlite3
from src.classes.queries import temp_query, existing_panels_and_portions_query, temp_between_query
from src.classes.mutations import delete_temp_between

db_path = r'output/ivkemence.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute(existing_panels_and_portions_query)
valid_combinations = cursor.fetchall()

log_file_path = "output/torolt_rekordok.txt"
with open(log_file_path, "w") as log_file:
    log_file.write("Törölt rekordok\n")
    log_file.write("=" * 40 + "\n")

for hutopanel_id, adag_id in valid_combinations:
    print(f'hutopanel : {hutopanel_id}, adag:  {adag_id}')

    cursor.execute(temp_query, (hutopanel_id,adag_id))

    homerseklet_list = [row[0] for row in cursor.fetchall()]

    df = pd.DataFrame(homerseklet_list,columns=['homerseklet'])

    also_kuszob = 0
    felso_kuszob = 100

    adag_id_and_panel_id_not_for_valid_datas =[]

    cursor.execute(temp_between_query, (also_kuszob, felso_kuszob, adag_id, hutopanel_id))
    deleted_records = cursor.fetchall()

    with open(log_file_path, "a") as log_file:
        if deleted_records:
            with open(log_file_path, "a") as log_file:
                log_file.write(f"Deleted records for hutopanel_id {hutopanel_id}, adag_id {adag_id}:\n")
                log_file.write(f"Also küszöb: {also_kuszob:.2f}, Felso küszöb: {felso_kuszob:.2f}\n")
                for record in deleted_records:
                    log_file.write(f"{record}\n")

            if (hutopanel_id, adag_id) not in adag_id_and_panel_id_not_for_valid_datas:
                adag_id_and_panel_id_not_for_valid_datas.append((hutopanel_id, adag_id))

    for hutopanel_id, adag_id in adag_id_and_panel_id_not_for_valid_datas:
        cursor.execute(delete_temp_between, (adag_id, hutopanel_id))

conn.commit()
conn.close()

