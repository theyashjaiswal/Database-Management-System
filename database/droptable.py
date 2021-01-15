import json
from database.lockstatus import LockStatus
import re

class DropOp():
    def remove_tables(self,files,table_name):
        for filename in files:
            with open(filename) as user_tables:
                data = json.load(user_tables)
                tables = data['Tables']
                for table in tables:
                    if table['Table_name'] == table_name.lstrip():
                        #drop table
                        index = tables.index(table)
                        del tables[index]
                        break       
                with open(filename,'w') as usr_details:
                    json.dump(data,usr_details,indent=4)  
                usr_details.close()
            user_tables.close()

    def remove_dump(self,dumpname,table_name):
        with open(dumpname,'r') as dump_data:
            dump = dump_data.readlines()
            for que in dump:
                table = re.findall(r'table(.*?)\(', que.lower())
                if table[0].strip() == table_name.lstrip():
                    dump.remove(que)
                    break
            with open(dumpname,'w') as changed_data:
                changed_data.write(str(dump).lstrip("['").rstrip("']"))
            changed_data.close()
        dump_data.close()

    def drop_table(self,username,dbname,table_name,logger,fname):
        check_lock = LockStatus().checklock(username)
        src_fname = dbname+"_Tables.txt"
        dest_dname = dbname+"_Tables_copy.txt"
        if fname == None:            
            filename = src_fname
            dumpname = dbname + "_SQLDUMP.sql"
            dtname = dbname + "_Tables_Datatypes.txt"
            status = False
        else:
            filename = dest_dname
            dumpname = dbname + "_SQLDUMP_copy.sql"
            dtname = dbname + "_Tables_Datatypes_copy.txt"
            status = True
        delete_tables = []
        delete_tables.append(filename)
        delete_tables.append(dtname)
        self.remove_tables(delete_tables,table_name)
        # remove from dump
        self.remove_dump(dumpname,table_name)           
        return status
