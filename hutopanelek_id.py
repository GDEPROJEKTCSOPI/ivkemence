import pandas as pd

# Az adagok CSV fájl betöltése
file_path_adagok = r'C:\Users\VG\Desktop\projektfeladat\adagok.csv'
adagok_df = pd.read_csv(file_path_adagok, encoding='ISO-8859-1', sep=';')

# Új oszlop létrehozása - Kezdeti dátum és idő
adagok_df['Kezdeti dátum és idő'] = pd.to_datetime(
    adagok_df['Kezdeti dátum'] + ' ' + adagok_df['Kezdet idõ'], errors='coerce'
)

# Új oszlop létrehozása - Vége dátum és idő
adagok_df['Vége dátum és idő'] = pd.to_datetime(
    adagok_df['Vége dátum'] + ' ' + adagok_df['Vége idõ'], errors='coerce'
)

# A DataFrame exportálása új CSV fájlba UTF-8 kódolással és pontosvesszővel elválasztva
output_path_adagok = r'C:\Users\VG\Desktop\projektfeladat\adagok_atalakitott.csv'
adagok_df.to_csv(output_path_adagok, sep=';', encoding='utf-8', index=False)

print(f"CSV fájl elmentve ide: {output_path_adagok}")

# Hutopanelek csv betöltés
file_path_hutopanelek = r'C:\Users\VG\Desktop\projektfeladat\Hutopanelek.csv'

# csv-k betöltése pontosvesszővel elválasztva, utf-8 kódolással
hutopanelek_df = pd.read_csv(file_path_hutopanelek, sep=';', encoding='utf-8')
adagok_atalakitott_df = pd.read_csv(output_path_adagok, sep=';', encoding='utf-8')

# Az idők átalakítása datetime formátumra a hutopanelek fájlban
hutopanelek_df['Panel hőfok 1 [°C] Time'] = pd.to_datetime(hutopanelek_df['Panel hőfok 1 [°C] Time'], errors='coerce', format='%Y.%m.%d %H:%M')

# Az adagok H és I oszlopának (kezdeti és vége dátum/idő) átalakítása datetime formátumra
start_times = pd.to_datetime(adagok_atalakitott_df['Kezdeti dátum és idő'], errors='coerce')
end_times = pd.to_datetime(adagok_atalakitott_df['Vége dátum és idő'], errors='coerce')

# Függvény az adagszám megkeresésére az idő alapján
def find_adagszam_for_time(time, start_times, end_times, adagszam):
    for start_time, end_time, adagszam_value in zip(start_times, end_times, adagszam):
        if start_time <= time <= end_time:
            return adagszam_value
    return None

# Az adagszám hozzárendelése közvetlenül az 'id' oszlopba (A oszlop)
hutopanelek_df['id'] = hutopanelek_df['Panel hőfok 1 [°C] Time'].apply(
    lambda x: find_adagszam_for_time(x, start_times, end_times, adagok_atalakitott_df['Adagszám'])
)

# Az eredmény exportálása UTF-8 kódolással, pontosvessző elválasztóval
output_path_hutopanelek = r'C:\Users\VG\Desktop\projektfeladat\Hutopanelek_id_3.csv'
hutopanelek_df.to_csv(output_path_hutopanelek, sep=';', encoding='utf-8', index=False)

print(f"Az átalakított fájl mentve: {output_path_hutopanelek}")
