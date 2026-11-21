class Person:
    def say_name(self,name):
        print("Hi",name)

    def say_name(self,name,lastname="Cheerala"):
        print("Hi", name,lastname)

t = Person()
t.say_name("Cheerala")

t = Person()
t.say_name("Shankar","Cheerala")