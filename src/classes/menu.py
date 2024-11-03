import cmd

from src.classes import utils
from src.classes.database_instance import db
from src.classes.database_manipulation import delete_temperature_data
from src.classes.database_manipulation import insert_temperature_data


class Menu(cmd.Cmd):
    intro   =   """
        IVKEMENCE adatbázis kezelő
        Kérlek válassz az elérhető parancsok közül
        ------------------------------------------
            > insert_temp <panel_id> <adag_id> <homerseklet>                |   Hőmérsékleti adat beszúrása az adatbázisba 
            
            > delete_temp <panel_id> <adag_id>                              |   Adat törlése adag és panel id alapján
            > help <parancs>                                                |   Segítséget nyújt a parancsok használatához
            > exit                                                          |   Kilépés
        ------------------------------------------
        """
    prompt  = 'IVKEMENCE CLI > '

    def do_insert_temp(self, arg):
        """
        Tetszőleges hőmérséklet adat beszúrása az adatbázisba.
        A parancs a jelenlegi dátumot és időt rendeli a bejegyzéshez.

        Szintaxis:
            panel_id: A hűtőpanel sorszáma, amihez a hőméréskleti adatok szeretnénk rendelni
            adag_id: Az adag azonosítója
            homerseklet: A hőmérsékleti érték

        Példa: insert_data 5 32 44.3
        """

        args = arg.split()

        # Bemenet ellenőrzés
        # Legalább 3 paraméter megadása szükséges és adattípus ellenőrzés
        if (len(args) < 3) or (not utils.is_int(args[0]) or not utils.is_int(args[1]) or not utils.is_float(args[2])):
            cmd.Cmd.do_help(self,"insert_temp")
            return

        insert_temperature_data(args[0], args[1], args[2])

    def do_delete_temp(self, arg):
        """
        Hőmérsékleti adat törlése az adatbázisból.
        Szintaxis:
            delete_temp <panel_id> <adag_id> - konkrét adat törlése id alapján
        """
        args = arg.split()

        # Ellenőrizzük, hogy pontosan 2 argumentumot kaptunk
        if len(args) != 2:
            self.do_help("delete_temp")
            return

        if utils.is_int(args[0]) and utils.is_int(args[1]):
             delete_temperature_data(args[0], args[1])  # Törlési funkció
        else:
            print("Hibás bemeneti értékek, győződj meg róla, hogy az azonosítók számok.")


    def do_exit(self, arg=None):
        """
            Kilépés a programból
            Ez a parancs az adatbázist is lezárja
        """
        db.close()
        exit(0)