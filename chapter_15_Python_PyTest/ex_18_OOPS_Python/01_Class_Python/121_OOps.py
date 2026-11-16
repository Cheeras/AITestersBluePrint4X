class Person:
    # Attributes
    name = None
    id = None
    age = None
    email = None
    height = None
    gender = None
    phone_no = None
    address = None

    # Behaviours
    def talk(self):  # self will be first argument in every behaviour
        print("I can Talk")

    def sleep(self, name):  # Arg with No Return
        print(f"{name} is sleeping")

    def walk(self):
        print("I am walking")

    def method_walk_return(self):  # No Arg with Return
        return "I am walking"

    def function_outside(self):
        print("outside")


# Create instances — outside the class
geeta = Person()
amit = Person()
navita = Person()

# Test the methods
geeta.talk()
geeta.sleep("Geeta")
amit.walk()
print(amit.method_walk_return())
navita.function_outside()