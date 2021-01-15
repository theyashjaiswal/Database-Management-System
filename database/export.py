import os.path
from database.fileops import FileOps

class Export_SQLDUMP:
    def export_sql_dump(self,db_name,query):
        fileOpsObj = FileOps()
        #export_location = re.findall(r"\'(.*?)\'", query)[0]
        #save_path = export_location
        save_path = "/Users/yash/database_5408_project_integration/output"
        full_name = os.path.join(save_path,db_name+"_SQLDUMP.sql")
        f1 = fileOpsObj.filereader(db_name+"_SQLDUMP.sql")
        fileOpsObj.filewriter(full_name,f1)
        #copyfile("/Users/yash/database_5408_project_create_insert/"+db_name+"_SQLDUMP.sql", export_location + db_name+"_SQLDUMP.sql")

# sqldumpObj = Export_SQLDUMP()
# query = "export sql dump;"
# sqldumpObj.export_sql_dump("5408",query)