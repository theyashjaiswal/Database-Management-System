import os
from database.default_database import CreateDefault

class UseDb():
    def use_database(self,dbname):
        file_exists = os.path.isfile(dbname+"_Tables.txt")
        if file_exists:
            return True
        else:
            return False
    def create_database(self,dbname):
        file_exists = os.path.isfile(dbname+"_Tables.txt")
        if file_exists:
            print("db already exists")
            return False
        else:
            CreateDefault().database(dbname)
            return True
