from src.classes.database_instance import db
from src.classes.database_manipulation import *
from src.classes.menu import Menu

# Főprogram indítás

Menu().cmdloop()

#insert_example()

#df = db.query("SELECT * FROM homerseklet WHERE datumido LIKE date() || '%';")

#print(df)

#db.close()