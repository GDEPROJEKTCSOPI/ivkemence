# modulok, könyvtárak,keretrendszerek beolvasása
import pandas as pd

# A hűtőpanelek CSV fájl betöltése
file_path_hutopanelek = r'csv/hutopanelek.csv'
hutopanelek_df = pd.read_csv(file_path_hutopanelek, sep=';', encoding='utf-8')

# Az adagok CSV fájl betöltése
file_path_adagok = r'csv/adagok.csv'
adagok_df = pd.read_csv(file_path_adagok, encoding='utf-8', sep=';')

# 'Panel hőfok 1 [°C] Time' átalakítása
hutopanelek_df['Panel hőfok 1 [°C] Time'] = pd.to_datetime(
    hutopanelek_df['Panel hőfok 1 [°C] Time'], format='%Y.%m.%d %H:%M', errors='coerce'
)

# Új oszlop létrehozása - Kezdeti dátum és idő
# Új oszlop létrehozása - Vége dátum és idő
adagok_df['start_datetime'] = pd.to_datetime(adagok_df['Kezdeti datum'] + ' ' + adagok_df['Kezdet ido'], errors='coerce')
adagok_df['end_datetime'] = pd.to_datetime(adagok_df['Vege datum'] + ' ' + adagok_df['Vege ido'], errors='coerce')

# A DataFrame exportálása új CSV fájlba UTF-8 kódolással és pontosvesszővel elválasztva
output_path_adagok = r'csv/adagok_atalakitott.csv'
adagok_df.to_csv(output_path_adagok, sep=';', encoding='utf-8', index=False)

print(f"CSV fájl elmentve ide: {output_path_adagok}")

# Az átalakított file beolvasása
adagok_atalakitott_df = pd.read_csv(output_path_adagok, sep=';', encoding='utf-8')

#  Az idők átalakítása datetime formátumra az adagok fájlban
adagok_atalakitott_df['start_datetime'] = pd.to_datetime(adagok_atalakitott_df['start_datetime'].str.strip().str.replace('\xa0', ''), errors='coerce')
adagok_atalakitott_df['end_datetime'] = pd.to_datetime(adagok_atalakitott_df['end_datetime'].str.strip().str.replace('\xa0', ''), errors='coerce')

# Az idők átalakítása datetime formátumra a hutopanelek fájlban
hutopanelek_df['Panel hőfok 1 [°C] Time'] = pd.to_datetime(
    hutopanelek_df['Panel hőfok 1 [°C] Time'], errors='coerce', infer_datetime_format=True
)

# A nem idő vagyis type hibás adatokat töröljük
hutopanelek_df.dropna(subset=['Panel hőfok 1 [°C] Time'], inplace=True)

# IntervalIndex létrehozása
intervals = pd.IntervalIndex.from_arrays(adagok_atalakitott_df['start_datetime'],
                                         adagok_atalakitott_df['end_datetime'],
                                         closed='both')

# Függvény az adagszám megkeresésére az idő alapján
def find_adagszam(time):
    match = adagok_atalakitott_df.loc[intervals.contains(time), 'Adagszam']
    if not match.empty:
        return match.values[0]  # Return the first match
    return None  # Return None if no match is found

# Az adagszám hozzárendelése közvetlenül az 'id' oszlopba (A oszlop)
hutopanelek_df['id'] = hutopanelek_df['Panel hőfok 1 [°C] Time'].apply(find_adagszam)

# Id oszlop előre hozása és átnevezése
cols = hutopanelek_df.columns.tolist()
cols.insert(0, cols.pop(cols.index('id')))  # Move 'id' to the first position
hutopanelek_df = hutopanelek_df[cols]
hutopanelek_df.rename(columns={'id': 'Adagszam'}, inplace=True)

# A DataFrame exportálása új CSV fájlba UTF-8 kódolással és pontosvesszővel elválasztva
output_path_hutopanelek = r'csv/hutopanelek_atalakitott.csv'
hutopanelek_df.to_csv(output_path_hutopanelek, sep=';', encoding='utf-8', index=False)

print(f"CSV fájl elmentve ide: {output_path_hutopanelek}")
