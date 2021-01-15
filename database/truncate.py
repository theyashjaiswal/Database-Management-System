import re
import json

from database.lockstatus import LockStatus


class Truncate:
    def strip_text(self, text):
        return re.sub(' +', ' ', text.strip())

    def truncate_table(self, username, dbname, query, logger, fname):
        check_lock = LockStatus().checklock(username)
        # create db copy
        src_fname = dbname + "_Tables.txt"
        dest_dname = dbname + "_Tables_copy.txt"
        if fname is None:
            filename = src_fname
            dtname = dbname + "_Tables_Datatypes.txt"
            status = False
        else:
            filename = dest_dname
            dtname = dbname + "_Tables_Datatypes_copy.txt"
            status = True
        file1 = open(filename, "r")
        f1 = file1.read()
        file1.close()
        update_set_dict = {}
        dict_obj = json.loads(f1)
        is_truncate_query = False
        # query = "TRUNCATE table player;"
        if re.split(" ", query)[0].lower() == "truncate":
            is_truncate_query = True
        file1 = open(filename, "r")
        f1 = file1.read()
        file1.close()
        update_set_dict = {}
        dict_obj = json.loads(f1)
        if (is_truncate_query):
            table_name = self.strip_text(re.findall(r'table(.*?);', query.lower())[0].strip())
            #print(table_name)
            tables_info = dict_obj['Tables']
            #print(tables_info)
            for values in tables_info:
                if values.get("Table_name") == table_name:
                    #print("found")
                    values_info = values['Table_columns']
                    #print(values_info)
                    del values_info[:1]
                    #print(values_info)
                    for column_values in values_info:
                        for columns in column_values:
                            column_values[columns] = 'defnull'
                        #print(column_values)
            #print(tables_info)
            #print(dict_obj)
            file1 = open(filename, "w+")
            f1 = file1.write(json.dumps(dict_obj))
            file1.close()

        return status
