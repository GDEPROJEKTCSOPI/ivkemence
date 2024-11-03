import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Panel:
    # SET
    def __init__(self, mini, maxi, avg, med, mod):
        self.mini = float(mini.replace(',', '.') if isinstance(mini, str) else mini)      
        self.maxi = float(maxi.replace(',', '.') if isinstance(maxi, str) else maxi)       
        self.avg = float(avg.replace(',', '.') if isinstance(avg, str) else avg)  
        self.med = float(med.replace(',', '.') if isinstance(med, str) else med)
        self.mod = float(mod.replace(',', '.') if isinstance(mod, str) else mod)
    
    # GET
    def get_min(self):  return self.mini 
    def get_max(self):  return self.maxi
    def get_avg(self):  return self.avg
    def get_med(self):  return self.med
    def get_mod(self):  return self.mod

eleresiut = r'db_creator/output/ivkemence.db'
conn = sqlite3.connect(eleresiut)

lekerdezes1 = '''
    WITH OrderedValues AS (
        SELECT "Panel hőfok 1 [°C] ValueY",
               ROW_NUMBER() OVER (ORDER BY CAST("Panel hőfok 1 [°C] ValueY" AS REAL)) AS rn,
               COUNT(*) OVER () AS total_count
        FROM hutopanelek
    )
    SELECT 
        MIN(CAST("Panel hőfok 1 [°C] ValueY" AS REAL)) AS min1,
        MAX(CAST("Panel hőfok 1 [°C] ValueY" AS REAL)) AS max1,
        AVG(CAST("Panel hőfok 1 [°C] ValueY" AS REAL)) AS avg1,
        (SELECT AVG("Panel hőfok 1 [°C] ValueY") FROM OrderedValues WHERE rn IN ((total_count + 1) / 2, (total_count + 2) / 2)) AS median,
        (SELECT "Panel hőfok 1 [°C] ValueY" FROM hutopanelek GROUP BY "Panel hőfok 1 [°C] ValueY" ORDER BY COUNT(*) DESC LIMIT 1) AS mode
    FROM hutopanelek;
'''

cursor = conn.cursor()
cursor.execute(lekerdezes1)
eredmeny1 = cursor.fetchone()
panel1 = Panel(eredmeny1[0], eredmeny1[1], eredmeny1[2], eredmeny1[3], eredmeny1[4])

lekerdezes2 = '''
    WITH OrderedValues AS (
        SELECT "Panel hőfok 2 [°C] ValueY",
               ROW_NUMBER() OVER (ORDER BY CAST("Panel hőfok 2 [°C] ValueY" AS REAL)) AS rn,
               COUNT(*) OVER () AS total_count
        FROM hutopanelek
    )
    SELECT 
        MIN(CAST("Panel hőfok 2 [°C] ValueY" AS REAL)) AS min1,
        MAX(CAST("Panel hőfok 2 [°C] ValueY" AS REAL)) AS max1,
        AVG(CAST("Panel hőfok 2 [°C] ValueY" AS REAL)) AS avg1,
        (SELECT AVG("Panel hőfok 2 [°C] ValueY") FROM OrderedValues WHERE rn IN ((total_count + 1) / 2, (total_count + 2) / 2)) AS median,
        (SELECT "Panel hőfok 2 [°C] ValueY" FROM hutopanelek GROUP BY "Panel hőfok 2 [°C] ValueY" ORDER BY COUNT(*) DESC LIMIT 1) AS mode
    FROM hutopanelek;
'''

cursor.execute(lekerdezes2)
eredmeny2 = cursor.fetchone()
panel2 = Panel(eredmeny2[0], eredmeny2[1], eredmeny2[2], eredmeny2[3], eredmeny2[4])

lekerdezes_data1 = 'SELECT CAST("Panel hőfok 1 [°C] ValueY" AS REAL) AS hofok1 FROM hutopanelek;'
data1 = pd.read_sql_query(lekerdezes_data1, conn)

lekerdezes_data2 = 'SELECT CAST("Panel hőfok 2 [°C] ValueY" AS REAL) AS hofok2 FROM hutopanelek;'
data2 = pd.read_sql_query(lekerdezes_data2, conn)

conn.close()

# Panel 1 hőfokok statisztika 
ypoints = np.array(data1['hofok1'])

ypoints = np.array(data1['hofok1']) 

plt.plot(ypoints, color='r', label='Panel 1 Hőfok')

plt.title("Panel1 Hőfokok változásának ábrázolása")
plt.xlabel("Mérések száma")
plt.ylabel("Hőfok (°C)")

plt.legend()
plt.grid(True)
plt.show()

# Panel 2 hőfokok statisztika 
ypoints = np.array(data2['hofok2'])

ypoints = np.array(data2['hofok2']) 

plt.plot(ypoints, color='r', label='Panel 2 Hőfok')

plt.title("Panel2 Hőfokok változásának ábrázolása")
plt.xlabel("Mérések száma")
plt.ylabel("Hőfok (°C)")

plt.legend()
plt.grid(True)
plt.show()

# Panel 1 és Panel 2 összehasonlítása
ypoints1 = np.array(data1['hofok1'])
ypoints2 = np.array(data2['hofok2'])

plt.plot(ypoints1, color='r', label='Panel 1 Hőfok')
plt.plot(ypoints2, color='b', label='Panel 2 Hőfok')  

plt.axhline(y=panel1.get_min(), color='r', linestyle='--', label='Panel 1 minimum hőfoka')
plt.axhline(y=panel1.get_max(), color='r', linestyle='--', label='Panel 1 maximális hőfoka')
plt.axhline(y=panel1.get_avg(), color='r', linestyle='--', label='Panel 1 átlagos hőfoka')
plt.axhline(y=panel1.get_med(), color='r', linestyle=':', label='Panel 1 hőfokának mediánja')
plt.axhline(y=panel1.get_mod(), color='r', linestyle='-.', label='Panel 1 hőfokának módusza')

plt.axhline(y=panel2.get_min(), color='b', linestyle='--', label='Panel 2 Minimum hőfoka')
plt.axhline(y=panel2.get_max(), color='b', linestyle='--', label='Panel 2 maximális hőfoka')
plt.axhline(y=panel2.get_avg(), color='b', linestyle='--', label='Panel 2 átlagos hőfoka')
plt.axhline(y=panel2.get_med(), color='b', linestyle=':', label='Panel 2 hőfokának mediánja')
plt.axhline(y=panel2.get_mod(), color='b', linestyle='-.', label='Panel 2 hőfokának módusza')

plt.title("Panel1 és Panel2 Hőfokok változásának összehasonlítása")
plt.xlabel("Mérések száma")
plt.ylabel("Hőfok (°C)")

plt.legend()
plt.grid(True)
plt.show()

# Tesztelés: 
#print("Panel 1 Statisztikák:")
#print(f"Min: {panel1.get_min():.2f} °C, Max: {panel1.get_max():.2f} °C, Avg: {panel1.get_avg():.2f} °C, Median: {panel1.get_med():.2f} °C, Mode: {panel1.get_mod():.2f} °C")
#print("\nPanel 2 Statisztikák:")
#print(f"Min: {panel2.get_min():.2f} °C, Max: {panel2.get_max():.2f} °C, Avg: {panel2.get_avg():.2f} °C, Median: {panel2.get_med():.2f} °C, Mode: {panel2.get_mod():.2f} °C")
#print("\nDATA1 kiiratása:")
#print(data1)
#print("\nDATA2 kiiratása:")
#print(data2)