import re
from database.fetchdata import FindData
from database.deletedata import DeleteOp
from database.droptable import DropOp
from database.usedb import UseDb
from database.create import CreatQuery
from database.insert import InsertQuery
from database.update import Update
from database.truncate import Truncate
from database.display import Display
from database.fileops import FileOps
from database.export import Export_SQLDUMP
import json
import os
from tabulate import tabulate
import pandas as pd
import shutil
import time
from database.logger import ConfigureLogs


class ParseQuery():
    def logrecords(self,dbname,total_time):
        eventlogger = ConfigureLogs().configure_log("GeneralLogs","General")
        eventlogger.info("Query execution time: {}".format(total_time))
        with open(dbname+"_Tables.txt") as user_tables:
            data = json.load(user_tables)
            tables = data['Tables']
            eventlogger.info("Number of tables in the database, {} is {}".format(dbname,len(tables)))
            for table in tables:
                rows = table['Table_columns']
                eventlogger.info("Number of rows in the table, {} : {}".format(table['Table_name'],len(rows)))

    def login_status(self,username,dbname,logger,start_time):
        end_time = time.time()
        total_time = end_time-start_time
        self.logrecords(dbname,total_time)
        ask_usr = input("Enter 0 if you want to continue or type exit to exit: ")

        if ask_usr == 'exit':
            SystemExit
        else:
            query = input("enter query in SQL to process: ")
            words = query.lower().split(' ')
            if words[0] == 'begin':
                self.parse_transactions(username, dbname, logger)
            else:
                self.parse_query(username, dbname, query, logger)

    def check_permissions(self,username):
        with open("user_details.json") as user_details:
            data = json.load(user_details)
            usrs = data['User_Details']
            flag = 0
            for usr in usrs:
                if usr['username'] == username:
                    permissions = usr['granted_privileges']
                    return permissions

    def showdb(self,username,logger):
        files = os.listdir()
        print("-------------------List Of Databases----------------------")
        db_dict = {}
        lst_db = []
        for file in files:
            if file.endswith('_Tables.txt'):                
                lst_db.append(file[0:-11])
                db_dict['databases'] = lst_db
        databases = db_dict['databases']
        print(tabulate(pd.DataFrame(databases, columns=db_dict.keys()),headers = 'keys', tablefmt = 'psql'))
        query= input("use already created database or create a new one using sql query only: ")
        format = query.lower().split(' ')
        if len(format) == 2 and (format[0] == 'use' or format[0] == 'create'):
            self.create_use(username,query,logger)

    def create_use(self,username,query,logger):
        query = query.lower()
        words = query.split(' ')
        dbname = ''
        if words[0].lower() == 'create':
            dbname = words[1].strip(';')
            self.parse_createdb(username,dbname,logger)
        elif words[0].lower() == 'use':
            dbname = words[1].strip(';')
            self.parse_use(username,dbname,logger)
        logger.info("User {} has selected {} database".format(username,dbname))

    def parse_query(self,username,dbname,query,logger,fname=None):
        logger.info("Query sent by the user {}, is {}".format(username,query))
        start_time = time.time()
        query = query.lower()
        words = query.split(' ')
        check_permissions = self.check_permissions(username)
        if words[0] in check_permissions:
            if words[0].lower() == 'select':
                #select parsing
                try:
                    self.parse_select(username,dbname,query,logger,fname,start_time)
                except:
                    print("Error in your Select query!!! Please check syntax!!")
                    logger.error("Error in your Select query!!! Please check syntax!!")
                    self.login_status(username, dbname, logger, start_time)
            elif words[0].lower() == 'delete':
                #delete parsing
                try:
                    self.parse_delete(username,dbname,query,logger,fname,start_time)
                except:
                    print("Error in your Delete query!!! Please check syntax!!")
                    logger.error("Error in your Delete query!!! Please check syntax!!")
                    self.login_status(username, dbname, logger, start_time)
            elif words[0].lower() == 'drop':
                #drop table
                try:
                    self.parse_drop(username,dbname,query,logger,fname,start_time)
                except:
                    print("Error in your drop query!!! Please check syntax!!")
                    logger.error("Error in your drop query!!! Please check syntax!!")
                    self.login_status(username, dbname, logger, start_time)
            elif words[0].lower() == 'create':
                crtObj = CreatQuery()
                try:
                    status = crtObj.create_table(username,dbname,query,logger,fname)
                    if status:
                        return
                    else:
                        self.login_status(username,dbname,logger,start_time)
                except:
                    print("Error in your Create query!!! Please check syntax!!")
                    logger.error("Error in your drop query!!! Please check syntax!!")
                    self.login_status(username, dbname, logger, start_time)
            elif words[0].lower() == 'insert':
                insertObj = InsertQuery()
                try:
                    status = insertObj.insert_row(username,dbname,query,logger,fname)
                    if status:
                        return
                    else:
                        self.login_status(username,dbname,logger,start_time)
                except:
                    print("Error in your Insert query!!! Please check syntax!!")
                    logger.error("Error in your Insert query!!! Please check syntax!!")
                    self.login_status(username, dbname, logger, start_time)
            elif words[0].lower() == 'update':
                updateObj = Update()
                try:
                    status = updateObj.update_row(username, dbname, query, logger, fname)
                    if status:
                        return
                    else:
                        self.login_status(username, dbname, logger, start_time)
                except:
                    print("Error in your update query!!! Please check syntax!!")
                    logger.error("Error in your update query!!! Please check syntax!!")
                    self.login_status(username, dbname, logger, start_time)
            elif words[0].lower() == 'truncate':
                truncateObj = Truncate()
                try:
                    status = truncateObj.truncate_table(username, dbname, query, logger, fname)
                    if status:
                        return
                    else:
                        self.login_status(username, dbname, logger, start_time)
                except:
                    print("Error in your truncate query!!! Please check syntax!!")
                    logger.error("Error in your truncate query!!! Please check syntax!!")
                    self.login_status(username, dbname, logger, start_time)
            elif words[0].lower() == 'show':
                try:
                    displayObj = Display()
                    fileopobj = FileOps()
                    f1 = fileopobj.filereader(dbname+"_Tables.txt")
                    usertable_dict_obj = json.loads(f1)
                    status = displayObj.print_tables(usertable_dict_obj)
                    if status:
                        return
                    else:
                        self.login_status(username,dbname,logger,start_time)
                except:
                    print("Error in your query!!! Please check syntax!! Show Tables;")
                    logger.error("Error in your query!!! Please check syntax!! Show Tables;")
                    self.login_status(username, dbname, logger, start_time)
            elif (words[0].lower() == 'export' and words[1].lower() == 'data') and (words[2].lower() == 'dictionary' or words[2].lower() == 'dictionary;'):
                try:
                    displayObj = Display()
                    fileopobj = FileOps()
                    f1 = fileopobj.filereader(dbname+"_Tables_Datatypes.txt")
                    usertable_datatype_dict_obj = json.loads(f1)
                    status = displayObj.print_datadictionary("DataDictionary.txt",usertable_datatype_dict_obj)
                    print("Data Dictionary exported. Check your output folder.")
                    logger.info("Data Dictionary exported. Check your output folder.")
                    if status:
                        return
                    else:
                        self.login_status(username,dbname,logger,start_time)
                except:
                    print("Error in your query!!! Please check syntax!! export data dictionary;")
                    logger.error("Error in your query!!! Please check syntax!! export data dictionary;")
                    self.login_status(username, dbname, logger, start_time)
            elif (words[0].lower() == 'export') and (words[1].lower() == 'erd' or words[1].lower() == 'erd;'):
                try:
                    displayObj = Display()
                    fileopobj = FileOps()
                    f1 = fileopobj.filereader(dbname+"_Tables_Datatypes.txt")
                    usertable_datatype_dict_obj = json.loads(f1)
                    status = displayObj.print_relationships("ERD.txt",usertable_datatype_dict_obj)
                    print("ERD exported. Check your output folder.")
                    logger.info("ERD exported. Check your output folder.")
                    if status:
                        return
                    else:
                        self.login_status(username,dbname,logger,start_time)
                except:
                    print("Error in your query!!! Please check syntax!! export erd;")
                    logger.error("Error in your query!!! Please check syntax!! export erd;")
                    self.login_status(username, dbname, logger, start_time)
            elif (words[0].lower() == 'export' and words[1].lower() == 'sql') and (words[2].lower() == 'dump' or words[2].lower() == 'dump;'):
                try:
                    sqldumpObj = Export_SQLDUMP()
                    status = sqldumpObj.export_sql_dump(dbname,query)
                    print("SQL Dump exported. Check your output folder.")
                    logger.info("SQL Dump exported. Check your output folder.")
                    if status:
                        return
                    else:
                        self.login_status(username,dbname,logger,start_time)
                except:
                    print("Error in your query!!! Please check syntax!! export sql dump;")
                    logger.error("Error in your query!!! Please check syntax!! export sql dump;")
                    self.login_status(username, dbname, logger, start_time)
            else:
                print("Invalid query!!! Please check syntax!!")
                logger.error("Invalid query!!! Please check syntax!!")
                self.login_status(username, dbname, logger, start_time)
        else:
            print("no permissions granted")
            self.login_status(username, dbname, logger, start_time)

    def parse_transactions(self,username,db_name,logger):
        try:
            start_time = time.time()
            query_list =[]
            file_exists = os.path.isfile("lock_details.json")
            if file_exists:
                with open("lock_details.json") as lock_details:
                    data = json.load(lock_details)
                    lock = data['Lock_Details']
                
                    if lock['lock_acquired'] == True:
                        print("other user is already accessing the database")
                        logger.info("other user is already accessing the database")
                        return
                    else:
                        detail_dict = {'lock_acquired': True,'username':username}
                        data['Lock_Details'] = detail_dict
                        with open("lock_details.json", 'w') as lck_details:
                            json.dump(data,lck_details,indent=4) 
                        lck_details.close()  
                        src_fname = db_name+"_Tables.txt"
                        dest_dname = db_name+"_Tables_copy.txt"     
                        shutil.copy(src_fname,dest_dname) 
                        src_dtname = db_name+"_Tables_Datatypes.txt"
                        dest_dtname = db_name+"_Tables_Datatypes_copy.txt"     
                        shutil.copy(src_dtname,dest_dtname)
                        src_dumpname = db_name+"_SQLDUMP.sql"
                        dest_dumpname = db_name+"_SQLDUMP_copy.sql"
                        shutil.copy(src_dumpname,dest_dumpname)
                lock_details.close()
            
            else:
                lock_dict = {} 
                details = []
                detail_dict = {'lock_acquired': True,'username':username}
                lock_dict['Lock_Details'] = detail_dict
                with open("lock_details.json", 'a') as lock_details:
                    json.dump(lock_dict,lock_details,indent=4)
                    src_fname = db_name+"_Tables.txt"
                    dest_dname = db_name+"_Tables_copy.txt"     
                    shutil.copy(src_fname,dest_dname)  
                    src_dtname = db_name+"_Tables_Datatypes.txt"
                    dest_dtname = db_name+"_Tables_Datatypes_copy.txt"     
                    shutil.copy(src_dtname,dest_dtname)
                    src_dumpname = db_name+"_SQLDUMP.sql"
                    dest_dumpname = db_name+"_SQLDUMP_copy.sql"
                    shutil.copy(src_dumpname,dest_dumpname) 
                lock_details.close()

            for que in range(1,3):
                query = input("enter the {} query in the transaction".format(que))
                query_list.append(query)
            status = input("do you want to commit this transaction?type commit; ")
            for query in query_list:
                self.parse_query(username,db_name,query,logger,fname=db_name+"_Tables_copy.txt")
            if 'commit' in status.lower():
                shutil.copy(db_name+"_Tables_copy.txt",db_name+"_Tables.txt")  
                shutil.copy(db_name + "_Tables_Datatypes_copy.txt",db_name + "_Tables_Datatypes.txt") 
                file_exists = os.path.isfile(db_name + "_SQLDUMP_copy.sql")
                if file_exists:
                    shutil.copy(db_name + "_SQLDUMP_copy.sql",db_name + "_SQLDUMP.sql")

            os.remove(db_name+"_Tables_copy.txt")
            os.remove(db_name+"_Tables_Datatypes_copy.txt")
            if file_exists: 
                os.remove(db_name+"_SQLDUMP_copy.sql")
            
            with open("lock_details.json") as lock_details:
                data = json.load(lock_details)
                lock = data['Lock_Details']               
                if lock['lock_acquired'] == True:
                    lock['lock_acquired'] = False
                    with open("lock_details.json", 'w') as lck_details:
                        json.dump(data,lck_details,indent=4)
                    lck_details.close()
            lock_details.close()
            self.login_status(username,db_name,logger,start_time)
        except:
            logger.error("an error occurred while performing transactions")

    def parse_createdb(self,username,db_name,logger):
        status = UseDb().create_database(db_name)
        if status:
            query= input("enter query in SQL to process: ")
            words = query.lower().split(' ')
            if words[0] == 'begin':
                self.parse_transactions(username,db_name,logger)
            else:
                self.parse_query(username,db_name,query,logger)
        else:
            query = input("give new db name with create")
            format = query.lower().split(' ')
            if len(format) == 2 and format[0] == 'create':
                self.create_use(username,query,logger)

    def parse_use(self,username,db_name,logger):
        status = UseDb().use_database(db_name)
        if status:
            query= input("enter query in SQL to process: ")
            words = query.lower().split(' ')
            if words[0] == 'begin':
                self.parse_transactions(username,db_name,logger)
            else:
                self.parse_query(username,db_name,query,logger)
        else:
            query = input("create a new db with create: ")
            format = query.lower().split(' ')
            if len(format) == 2 and format[0] == 'create':
                self.create_use(username,query,logger)

    def parse_select(self,username,dbname,query,logger,fname,start_time):
        query = query.lower()
        logger.info("parsing select query, {}".format(query))
        col = re.search('select(.+?)from',query).group(1)
        columns = col.strip().split(',')
        find = re.search('from(.+?)where',query)
        if find:
            table_name = find.group(1).strip().split(' ')
            pattern = re.compile('where(.*)')
            condition = pattern.findall(query)
            status = FindData().fetch_data(dbname,table_name[0],columns,condition[0].strip(';'),logger,fname)
            if status:
                return
            else:
                self.login_status(username,dbname,logger,start_time)
        else:
            pattern = re.compile('from(.*)')
            table_name = pattern.findall(query)
            status = FindData().fetch_data(dbname,table_name[0].strip(';'),columns,logger=logger,fname=fname)
            if status:
                return
            else:
                self.login_status(username,dbname,logger,start_time)
    
    def parse_delete(self,username,dbname,query,logger,fname,start_time):
        query = query.lower()
        logger.info("parsing delete query, {}".format(query))
        find = re.search('from(.+?)where',query)
        if find:
            table_name = find.group(1).strip().split(' ')
            pattern = re.compile('where(.*)')
            condition = pattern.findall(query)
            status = DeleteOp().delete_data(username,dbname,table_name[0],condition[0].strip(';'),logger,fname)
            if status:
                return
            else:
                self.login_status(username,dbname,logger,start_time)

        else:
            pattern = re.compile('from(.*)')
            table_name = pattern.findall(query)
            status = DeleteOp().delete_data(username,dbname,table_name[0].strip(';'),logger=logger,fname=fname)
            if status:
                return
            else:
                self.login_status(username,dbname,logger,start_time)
            
    def parse_drop(self,username,dbname,query,logger,fname,start_time):
        query = query.lower()
        logger.info("parsing drop query, {}".format(query))
        pattern = re.compile('table(.*)')
        table_name = pattern.findall(query)
        status = DropOp().drop_table(username,dbname,table_name[0].strip(';'),logger,fname)
        if status:
            return
        else:
            self.login_status(username,dbname,logger,start_time)
