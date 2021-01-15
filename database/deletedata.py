import re
import json
from database.lockstatus import LockStatus

class DeleteOp():        

    def delete_data(self,username,dbname,table_name,condition=None,logger=None,fname=None):
        check_lock = LockStatus().checklock(username)
        #create db copy
        src_fname = dbname+"_Tables.txt"
        dest_dname = dbname+"_Tables_copy.txt"
        if fname == None:            
            filename = src_fname
            status = False
        else:
            filename = dest_dname
            status = True
        with open(filename,'r') as user_tables:
            jdata = json.load(user_tables)
            tables = jdata['Tables']
            for table in tables:
                if table['Table_name'] == table_name.lstrip():
                    global table_data
                    table_data = table['Table_columns']
                    if condition == None:
                        del table_data[1:]
                        for data in table_data:
                            for key in data:
                                data[key] = 'null'
                        logger.info("data is deleted from the table {}".format(table_name))                        
                    else:
                        row_num=0
                        row_to_delete=[]
                        num_of_rows_table = len(table_data)
                        flag = True
                        for data in table_data:
                            g_op = re.search(">",condition)
                            l_op = re.search("<",condition)
                            e_op = re.search("=",condition)
                            if g_op:
                                lst = condition.split('>')
                                if data[lst[0].lower().strip()] != 'null' and int(data[lst[0].lower().strip()]) > int(lst[1].lower().strip()):
                                    row_to_delete.append(row_num)
                                    for key in data:
                                        if(num_of_rows_table==1):
                                            flag=False
                                            data[key] = 'null'
                                        else:
                                            continue
                                    logger.info("data is deleted from the table {}".format(table_name))
                                    
                            elif l_op:
                                lst = condition.split('<')
                                if data[lst[0].lower().strip()] != 'null' and int(data[lst[0].lower().strip()]) < int(lst[1].lower().strip()):
                                    row_to_delete.append(row_num)
                                    for key in data:
                                        if (num_of_rows_table == 1):
                                            flag = False
                                            data[key] = 'null'
                                        else:
                                            continue
                                    logger.info("data is deleted from the table {}".format(table_name))
                                    
                            elif e_op:
                                lst = condition.split('=')
                                res = isinstance(data[lst[0].lower().strip()],int)
                                if res:
                                    given = int(lst[1].lower().strip())
                                else:
                                    given = lst[1].lower().strip()                                
                                if data[lst[0].lower().strip()] == given :
                                    row_to_delete.append(row_num)
                                    for key in data:
                                        if (num_of_rows_table == 1):
                                            flag = False
                                            data[key] = 'null'
                                        else:
                                            continue
                                    logger.info("data is deleted from the table {}".format(table_name))
                                    print("data is deleted from the table {}".format(table_name))
                            row_num += 1
                        new_list=[]
                        final_list=[]
                        if(flag):
                            for x in row_to_delete:
                                new_list.append(table_data[x])
                            for x in table_data:
                                if (x in new_list):
                                    continue
                                else:
                                    final_list.append(x)
                        else:
                            final_list=table_data

                    table['Table_columns'] = final_list
            
            with open(filename,'w') as usr_details:
                json.dump(jdata,usr_details,indent=4) 
            usr_details.close()
        user_tables.close()
        return status


