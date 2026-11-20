class TestExample:
    def __init__(self):
        self.driver = "Chrome"
        self._config = "STAG"
        self.__api__key = "ABC12345"

    def show(self):
        print(f"Driver: {self.driver}")
        print(f"Config: {self._config}")
        print(f"API key: {self.__api__key}")

    def __private_method1(self):
        pass

    def __private_method2(self):
        pass

    def work(self):
        self.__private_method1()
        self.__private_method2()


obj_ref = TestExample()
obj_ref.show()
obj_ref.work()

# Access Levels:

print(obj_ref.driver)
print(obj_ref._config)
#print(obj_ref.__api__key)