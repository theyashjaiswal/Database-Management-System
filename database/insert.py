import re
import json
from database.fileops import FileOps
from database.lockstatus import LockStatus


class InsertQuery:

    def __init__(self):
        self.fileObj = FileOps()

    def strip_text(self, text):
        return re.sub(' +', ' ', text.strip())

    def insert_row(self,username,dbname,query,logger,fname):
        check_lock = LockStatus().checklock(username)
        #create db copy
        src_fname = dbname+"_Tables.txt"
        dest_dname = dbname+"_Tables_copy.txt"
        if fname == None:            
            filename = src_fname
            dtname = dbname+"_Tables_Datatypes.txt"
            status = False
        else:
            filename = dest_dname
            dtname = dbname+"_Tables_Datatypes_copy.txt"
            status = True

        table_name = re.split(" ", self.strip_text(re.findall(r'into(.*?)\(', query.lower())[0]))[0]

        query_tablelevel = re.findall(r'\((.*?)\)', query.lower())

        if (len(query_tablelevel) == 1):
            table_columns_values_list = re.split(",",re.sub("[^A-Za-z0-9_, ]", "", self.strip_text(query_tablelevel[0])))
        else:
            table_columns_headers_list = re.split(",",re.sub("[^A-Za-z0-9_, ]", "", self.strip_text(query_tablelevel[0])))
            table_columns_values_list = re.split(",",re.sub("[^A-Za-z0-9_, ]", "", self.strip_text(query_tablelevel[1])))


        if len(re.findall(r'\((.*?)\)', query.lower())) == 1:

            # DIRECT INSERT with out columns indication
            print("Inserted rows in Table")
            f1 = json.loads(self.fileObj.filereader(filename))
            f2 = json.loads(self.fileObj.filereader(dtname))

            auto_increment_list = []
            original_table_col_list = []

            for i in f2['Tables']:
                if (i['Table_name'] == table_name):
                    auto_increment_list = i['Table_columns'][0]['Auto Increment']
                    original_table_col_list = i['Table_columns'][0]['Name']
                    nullable_original_list = i['Table_columns'][0]['Nullable']

            null_check_list = []
            for z in range(0, len(original_table_col_list)):
                if (nullable_original_list[z] == "No" and auto_increment_list[z] != "Yes"):
                    null_check_list.append(original_table_col_list[z])

            is_null_error = False
            for x in range(0,len(table_columns_values_list)):
                if(nullable_original_list[x] == "Yes" and "null" in table_columns_values_list):
                    is_null_error = True

            if(not(is_null_error)):
                is_this_table_flag = False
                for k, v in f1.items():
                    if (k == "Tables"):
                        for t in v:
                            for k1, v1 in t.items():
                                if (k1 == "Table_name" and v1 == table_name):
                                    is_this_table_flag = True
                                    continue
                                if (is_this_table_flag):
                                    # reset flag once entered
                                    is_this_table_flag = False
                                    # change default values first i.e first row
                                    if (len(v1) == 1 and "defnull" in v1[0].values()):
                                        if (len(v1[0]) == len(table_columns_values_list)):
                                            i = 0
                                            for v1 in v1:
                                                for k2, v2 in v1.items():
                                                    if (i < len(table_columns_values_list)):
                                                        v1[k2] = table_columns_values_list[i].capitalize()
                                                        i += 1
                                    else:
                                        temp_obj = v1[len(v1) - 1].copy()
                                        v1.append(temp_obj)
                                        i = 0
                                        for k2, v2 in v1[len(v1) - 1].items():
                                            if (i < len(table_columns_values_list)):
                                                v1[len(v1) - 1][k2] = table_columns_values_list[i].capitalize()
                                                i += 1
                self.fileObj.filewriter(filename, json.dumps(f1))

            else:
                print("Null values not allowed for the columns: "+str(null_check_list) +" in Table: "+table_name.capitalize())
                print("Please re-enter your query.")

        elif len(re.findall(r'\((.*?)\)', query.lower())) == 2:
            # insert values in specific columns
            print("Inserted rows in Table")
            f1 = json.loads(self.fileObj.filereader(filename))
            f2 = json.loads(self.fileObj.filereader(dtname))

            is_this_table_flag = False
            auto_increment_list = []
            original_table_col_list = []

            for i in f2['Tables']:
                if(i['Table_name']==table_name):
                    auto_increment_list= i['Table_columns'][0]['Auto Increment']
                    original_table_col_list = i['Table_columns'][0]['Name']
                    nullable_original_list = i['Table_columns'][0]['Nullable']

            null_check_list = []
            for z in range(0,len(original_table_col_list)):
                if(nullable_original_list[z]=="No" and auto_increment_list[z]!="Yes"):
                    null_check_list.append(original_table_col_list[z])

            is_null_error = False
            for y in null_check_list:
                if y not in table_columns_headers_list:
                    is_null_error = True

            if(not(is_null_error)):
                for k, v in f1.items():
                    if (k == "Tables"):
                        for t in v:
                            for k1, v1 in t.items():
                                if (k1 == "Table_name" and v1 == table_name):
                                    is_this_table_flag = True
                                    continue
                                if (is_this_table_flag):
                                    # reset flag once entered
                                    is_this_table_flag = False
                                    # change default values first i.e first row
                                    if (len(v1) == 1 and "defnull" in v1[0].values()):
                                        i = 0
                                        for v1 in v1:
                                            for k2, v2 in v1.items():
                                                if (i < len(table_columns_values_list)):
                                                    if (k2 == table_columns_headers_list[i]):
                                                        v1[k2] = table_columns_values_list[i].capitalize()
                                                        i += 1
                                                        continue
                                                if(v2 == "1"):
                                                    continue
                                                else:
                                                    v1[k2] = "null"
                                    else:
                                        temp_obj = v1[len(v1) - 1].copy()
                                        v1.append(temp_obj)
                                        i = 0
                                        j = 0
                                        for k2, v2 in v1[len(v1) - 1].items():
                                            if (i < len(table_columns_headers_list)):
                                                if (k2 == table_columns_headers_list[i]):
                                                    v1[len(v1) - 1][k2] = table_columns_values_list[i].capitalize()
                                                    i += 1
                                                    continue
                                            if(k2 == original_table_col_list[j] and auto_increment_list[j]=="Yes"):
                                                v1[len(v1) - 1][k2] = int(v1[len(v1) - 2][k2])+1
                                                j += 1
                                            else:
                                                v1[len(v1) - 1][k2] = "null"
                                                j += 1

                self.fileObj.filewriter(filename, json.dumps(f1))
            else:
                print("Null values not allowed for the columns: "+str(null_check_list) +" in Table: "+table_name.capitalize())
                print("Please re-enter your query.")
        else:
            print("ERROR IN INSERT QUERY!!!")
            print("Please re-enter your query.")
        return status

# # call from different method where queries are parsed
# insertObj = InsertQuery()
#
# # query = "INSERT INTO Player(player_id,team_id,league_id,player_name,position,age) VALUES(2,2,1,'Robinder Dhillon','Goalie',22);"
# #query = "INSERT INTO Player VALUES(24,1,2,'Sam','Forward',27);"
# #query = "INSERT INTO Team(league_id) VALUES(7);"
#query = "INSERT INTO Team(team_id,team_name,league_id) VALUES(1,'Robinder ki Team Lelo BHai',7);"
# query = "INSERT INTO Player(league_id,player_name,position,age) VALUES(1,'Kethan','Forward',22);"
# #query = "INSERT INTO Player(player_name) VALUES('Jordan');"
#
# insertObj.insert_row(query)
# is_insert_query = False
# if re.split(" ", query)[0].lower() == "insert":
#     is_insert_query = True
