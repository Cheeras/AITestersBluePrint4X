class BaseTest:
    def __init__(self,browser):
        self.browser = browser

    def setup(self):
        print(f"Launching {self.browser}")

class LoginTest(BaseTest):
    def run_test(self):
        self.setup()
        print("Running login Test.....")

class singupTest(BaseTest):
    def run_test(self):
        self.setup()
        print("Running the signup Test....")

t = LoginTest("Chrome")
t.run_test()

t1 = singupTest("firefox")
t1.run_test()