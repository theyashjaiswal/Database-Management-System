from database.authenticate import Login
from database.signup import Signup
from database.logger import ConfigureLogs

class MainUi():

    def ask_user(self):
        print("Enter 0 to Login\nEnter 1 to SignUp")
        option = input("your option: ")
        if option == '0':
            #redirect to login
            logger = ConfigureLogs().configure_log("Eventlogs","Event")
            Login().user_login(logger)
        elif option == '1':
            #redirect to signup
            logger = ConfigureLogs().configure_log("Eventlogs","Event")
            Signup().signup_user(logger)
            self.ask_user()
        else:
            print('enter correct option')

if __name__=="__main__":
    MainUi().ask_user()
