import pandas as pd
import os
from tabulate import tabulate
from database.fileops import FileOps

class Display:

    # add methods as required seperately donot modify these
    def print_tables(self,dict_object):
        # add methods as required seperately donot modify these
        print("\n======Tables=======")
        for i in dict_object['Tables']:
            print("\n")
            print("Table Name: " + i['Table_name'].capitalize())
            tables_headers = list(i['Table_columns'][0].keys())
            val = i['Table_columns']
            print(tabulate(pd.DataFrame(val, columns=tables_headers),
                           headers='keys', tablefmt='psql'))
            print("\n")

    def print_datadictionary(self,file_name,datatype_dict_object):
        fileopobj = FileOps()
        # add methods as required seperately donot modify these
        #print("\n======Data Dictionary=======")
        save_path = "/Users/yash/database_5408_project_integration/output"
        full_name = os.path.join(save_path, file_name)
        fileopobj.filewriter(full_name, "\n===========Data Dictionary============\n")
        for i in datatype_dict_object['Tables']:
            #print("\n")
            #print("Table Name: " + i['Table_name'].capitalize())
            fileopobj.filewriterAppend(full_name, "\nTable Name: " + i['Table_name'].capitalize()+"\n")
            tables_headers = list(i['Table_columns'][0].keys())
            tables_headers.remove("Relationship")
            val = i['Table_columns'][0]
            #print(tabulate(pd.DataFrame(val, columns=tables_headers),headers='keys', tablefmt='psql'))
            fileopobj.filewriterAppend(full_name,tabulate(pd.DataFrame(val, columns=tables_headers),
                           headers='keys', tablefmt='psql'))
            #print("\n")

    def print_relationships(self,file_name,datatype_dict_object):
        fileopobj = FileOps()
        # add methods as required seperately donot modify these
        #print("\n======Relationships between Tables=======")
        save_path = "/Users/yash/database_5408_project_integration/output"
        full_name = os.path.join(save_path, file_name)
        fileopobj.filewriter(full_name, "\n=========ER Diagram==========\n")
        fileopobj.filewriterAppend(full_name, "\nRelationships between Tables\n")
        for i in datatype_dict_object['Tables']:
            #print("\n")
            #print("Table Name: " + i['Table_name'].capitalize())
            fileopobj.filewriterAppend(full_name, "\nTable Name: " + i['Table_name'].capitalize()+"\n")
            tables_headers = ["Relationship"]
            val = i['Table_columns'][0]
            #print(tabulate(pd.DataFrame(val, columns=tables_headers),headers='keys', tablefmt='psql'))
            fileopobj.filewriterAppend(full_name,tabulate(pd.DataFrame(val, columns=tables_headers),headers='keys', tablefmt='psql'))
            #print("\n")

# #call from different method where queries are parsed
# fileopobj = FileOps()
# f1 = fileopobj.filereader("5408_group2_Tables.txt")
# f2 = fileopobj.filereader("5408_group2_Tables_Datatypes.txt")
# usertable_dict_obj = json.loads(f1)
# usertable_datatype_dict_obj = json.loads(f2)
#
# # print(json.dumps(usertable_dict_obj, indent = 1))
# # print(json.dumps(usertable_datatype_dict_obj, indent = 1))
#
# displayObj=Display()
#
# displayObj.print_tables(usertable_dict_obj)
#
# displayObj.print_datadictionary(usertable_datatype_dict_obj)
#
# displayObj.print_relationships(usertable_datatype_dict_obj)
