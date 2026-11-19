from dotenv import load_dotenv
import os
import platform
class VWOLoginPage:
    def __init__(self,email_arg,password_arg):
        self.email = email_arg
        self.password = password_arg

    def login_confirm(self):
        load_dotenv()
        if self.email == os.getenv("USERNAME") and self.password == os.getenv("PASSWORD"):
            print("Allowed, Login success")
        else:
            print("Login failed")

email = input("Enter the vwo login email")
password = input("Enter the Vwo login password")

vwo_obj_ref = VWOLoginPage(email,password)
vwo_obj_ref.login_confirm()

print(vwo_obj_ref.password)
print(os.name)
print(platform.system())
print(platform.release())
print(platform.version())