import cmd

from src.classes import utils
from src.classes.database_instance import db
from src.classes.database_manipulation import insert_temperature_data, update_temperature_data, delete_temperature_data
from src.classes.database_query import query_temperature_data,query_portion_data,query_panel_data
from src.classes.database_process import show_panel,show_two_panel,show_all_panel,show_all_portion

class Menu(cmd.Cmd):
    intro   =   """
        IVKEMENCE adatbázis kezelő
        Kérlek válassz az elérhető parancsok közül
        ------------------------------------------
            > get_portion_data                                              |   Elérhető adag adatok listázása
            > get_panel_data                                                |   Elérhető hűtőpanel adatok listázása
            > get_temperature_data <panel_id> <adag_id>                     |   Elérhető hőmérséklet adatok listázása
            > insert_temp <panel_id> <adag_id> <homerseklet>                |   Hőmérsékleti adat beszúrása az adatbázisba 
            > update_temp <id> <uj_homerseklet>                             |   Hőmérsékleti adat módosítása az adatbázisban
            > delete_temp <id>                                              |   Hőmérsékleti adat törlése az adatbázisban
            > show_panel                                                    |   Egy panelhez és adaghoz tartozó hőmérsékletek megjelenítése grafikonon
            > show_panels                                                   |   Egy adaghoz tartozó két panel adatainak megjelenítése
            > show_all_panels                                               |   Egy adaghoz tartozó összes panel adatainak megjelenítése
            > show_all_portions                                             |   Egy panelhez tartozó összes adag adatainak megjelenítése
            > help <parancs>                                                |   Segítséget nyújt a parancsok használatához
            > exit                                                          |   Kilépés
        ------------------------------------------
        """
    prompt  = 'IVKEMENCE CLI > '

    def emptyline(self):
        pass

    # Adagok adatinak lekérdezése az adatbázisból.
    def do_get_portion_data(self, arg):
        query_portion_data()

    # Panelek adatainek lekérdezése
    def do_get_panel_data (self, arg):
        query_panel_data()

    # Hőmérsékletek lekérdezése panel és adag szerint
    def do_get_temperature_data(self, arg):

        args = arg.split()

        if len(args) != 2:
            print("Hiba: Kérjük, pontosan két argumentumot adjon meg: <panel_id> és <adag_id>.")
            cmd.Cmd.do_help(self, "get_temperature_data")
            return
        query_temperature_data(args[0], args[1])

    def do_insert_temp(self, arg):
        """
        Tetszőleges hőmérséklet érték beszúrása az adatbázisba.
        A parancs a jelenlegi dátumot és időt rendeli a bejegyzéshez.

        Szintaxis:
            panel_id: A hűtőpanel sorszáma, amihez a hőméréskleti adatok szeretnénk rendelni
            adag_id: Az adag azonosítója
            homerseklet: A hőmérsékleti érték

        Példa: insert_temp 5 32 44.3
        """

        args = arg.split()

        # Bemenet ellenőrzés
        # 3 paraméter megadása szükséges és adattípus ellenőrzés
        if (len(args) != 3) or (not utils.is_int(args[0]) or not utils.is_int(args[1]) or not utils.is_float(args[2])):
            cmd.Cmd.do_help(self,"insert_temp")
            return

        insert_temperature_data(args[0], args[1], args[2])

    def do_update_temp(self, arg):
        """
        Adatbázisban már meglévő hőmérsékleti adat módosítása.

        Szintaxis:
            id: A "homerseklet" táblában a rekordhoz tartozó id
            homerseklet: Az új hőmérsékleti érték

        Példa: update_temp 12331 64
        """

        args = arg.split()

        # Bemenet ellenőrzés
        # Legalább 2 paraméter megadása szükséges és adattípus ellenőrzés
        if (len(args) != 2) or (not utils.is_int(args[0]) or not utils.is_float(args[1])):
            cmd.Cmd.do_help(self,"update_temp")
            return

        update_temperature_data(args[0], args[1])

    def do_delete_temp(self, arg):
        """
        Egy hőmérsékleti adat törlése az adatbázisból.
        Szintaxis:
            id: A "homerseklet" táblában a rekordhoz tartozó id

        Példa: delete_temp 23134
        """
        args = arg.split()

        # Ellenőrizzük, hogy pontosan 1 argumentumot kaptunk
        if len(args) != 1:
            self.do_help("delete_temp")
            return

        # Ellenőrizzük, hogy az id egész szám-e
        if utils.is_int(args[0]):
            delete_temperature_data(args[0])  # Törlési funkció hívása csak id-vel
        else:
            print("Hibás bemeneti érték, győződj meg róla, hogy az azonosító szám.")

    def do_show_panel(self,arg):
        show_panel()
    def do_show_panels(self,arg):
        show_two_panel()

    def do_show_all_panels(self,arg):
        show_all_panel()

    def do_show_all_portions(self, arg):
        show_all_portion()

    def do_exit(self, arg=None):
        """
            Kilépés a programból
            Ez a parancs az adatbázist is lezárja
        """
        db.close()
        exit(0)