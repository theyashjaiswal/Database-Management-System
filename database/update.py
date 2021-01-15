import re
import json

from database.lockstatus import LockStatus


class Update:

    def strip_text(self,text):
        return re.sub(' +', ' ', text.strip())

    def update_row(self, username,dbname,query,logger,fname):
        check_lock = LockStatus().checklock(username)
        # create db copy
        src_fname = dbname + "_Tables.txt"
        dest_dname = dbname + "_Tables_copy.txt"
        if fname is None:
            filename = src_fname
            status = False
        else:
            filename = dest_dname
            status = True
        file1 = open(filename, "r")
        f1 = file1.read()
        file1.close()
        update_set_dict = {}
        dict_obj = json.loads(f1)
        is_update_query = False
        # query = "UPDATE Player SET player_name = 'ABC', position = 'forward' WHERE team_id = '1';"
        if re.split(" ", query)[0].lower() == "update":
            is_update_query = True

        if is_update_query:
            # do operation
            update_query_set_values = re.split(",",
                                               re.sub("[^A-Za-z0-9=,_]", " ",
                                                      re.findall(r'set(.*?)where', query.lower())[0]))
            update_query_condition = re.split(",", re.sub("[^A-Za-z0-9=,_]", " ", re.split('where', query.lower())[1]))
            table_name = self.strip_text(re.findall(r'update(.*?)set', query.lower())[0].strip())

            for y in update_query_condition:
                list_condition_update = re.split("= |< |> |<= |>= ", y)
                key_to_search_for_update_condition = self.strip_text(list_condition_update[0])
                value_update_condition = self.strip_text(list_condition_update[1])

            for x in update_query_set_values:
                list_key_value_update = re.split("=", x)
                key_to_search = self.strip_text(list_key_value_update[0])
                value_to_update = self.strip_text(list_key_value_update[1])
                update_set_dict[key_to_search] = value_to_update
                # search in dict for condition and perform updates

            print("Update Query Operation")
            #print(update_set_dict)
            tables_info = dict_obj['Tables']
            #print(tables_info)
            for values in tables_info:
                if values.get("Table_name") == table_name:
                    print("found")
                    values_info = values['Table_columns']
                    for inside_list_value in values_info:
                        if inside_list_value.get(key_to_search_for_update_condition) == value_update_condition:
                            #print(inside_list_value)
                            inside_list_value.update(update_set_dict)

            #print(dict_obj)
            #print(values)
            #print('check')
            file1 = open(filename, "w+")
            f1 = file1.write(json.dumps(dict_obj))
            file1.close()
            return status