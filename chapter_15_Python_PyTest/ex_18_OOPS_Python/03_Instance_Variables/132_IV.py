g = 10 # Global variable

class Person:
    i = 11 # Instance, class, Attribute, property

    def print_infor(self):
        l = 20 # local l variable
        print(l)

    def talk(self):
        print(self.i)
        print(g)

personObjRef = Person()
personObjRef.print_infor()
personObjRef.talk()