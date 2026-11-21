class BaseTest:
    def run(self):
        print("Running the Base Test")

class LoginTest(BaseTest):
    def run(self):
        print("Running the Login Test")


t = BaseTest()
t.run()
