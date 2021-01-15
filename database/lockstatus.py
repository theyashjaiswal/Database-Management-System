import json
import sys

class LockStatus():
    def checklock(self,username):
        with open("lock_details.json") as lock_details:
            data = json.load(lock_details)
            lock = data['Lock_Details']        
            if lock['lock_acquired'] == True and lock['username'] != username:
                print("other user is already accessing the database")
                sys.exit()
            else:
                return