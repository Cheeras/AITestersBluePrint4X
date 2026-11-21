class TestSuite:
    def info(self):
        print("Test suite information")

class BaseTest(TestSuite):
    def setup(self):
        print("Base setup")

    def run(self):
        print("Base Test execution")

class LoginTest(BaseTest):
    def run(sef): # Overriding
        print("Login Test execution")

class APITest(BaseTest):
    def run(self): # Overriding
        print("API Test execution")

t1 = LoginTest()
t2 = APITest()
t3 = BaseTest()
t1.run()
