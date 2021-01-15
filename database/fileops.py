class FileOps:

    def filereader(self,filename):
        file1 = open(filename, "r")
        #add decryption
        f1 = file1.read()
        file1.close()
        return f1

    def filewriter(self,filename,content):
        file2 = open(filename, "w+")
        # add encryption
        file2.write(content)
        file2.close()

    def filewriterAppend(self,filename,content):
        file3 = open(filename, "a")
        file3.write(content)
        file3.close()
