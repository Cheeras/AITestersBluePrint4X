"""
static belongs to class
it will be same for all objects ref
whatever is common between all objects ref
it become static
"""

class AITB:
    statcourseName = "AITB"
    mentor = "ShankarCheerala"

    def __init__(self,name):
        self.name = name

    def display(self):
        print("HI ,",self.name,"Your Mentor is "+ AITB.mentor)

    @staticmethod
    def display2():
        print("Static method")

s1 = AITB("Amit")
s2 = AITB("Luckky")
s1.display()
s2.display()

AITB.display2()