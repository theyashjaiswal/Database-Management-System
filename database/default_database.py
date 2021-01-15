class CreateDefault():

    def database(self,dbname):
        if len(dbname)== 0 :
            dbname = "assignment_5408"
        else:
            self.dbname = dbname

        flower_bracket_start = '{'
        flower_bracket_end = '}'

        #default structure for dict
        default_json_string = flower_bracket_start+'"Database_name":"'+dbname+'","Tables":[]'+flower_bracket_end
        default_data_type_json_string = flower_bracket_start+'"Database_name":"'+dbname+'","Tables":[]'+flower_bracket_end

        print("Creating new DATABSASE: "+dbname)
        file1 = open(dbname+"_Tables.txt", "w+")
        file1.write(default_json_string)
        file1.close()
        file2 = open(dbname+"_Tables_Datatypes.txt", "w+")
        file2.write(default_data_type_json_string)
        file2.close()