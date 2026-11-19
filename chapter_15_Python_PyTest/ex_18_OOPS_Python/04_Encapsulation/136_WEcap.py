class VWOLoginPage:
    def __init__(self,email_arg,password_arg):
        self.email = email_arg
        self.password = password_arg

    def login_confirm(self):
        if self.email == "student@example.com" and self.password == "demo123":
            print("Login is Allowed")
        else:
            print("Login failed")

email = input("Enter the vwo login email")
password = input("Enter the Vwo login password")

vwo_obj_ref = VWOLoginPage(email,password)
vwo_obj_ref.login_confirm()
    