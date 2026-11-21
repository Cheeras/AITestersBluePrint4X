from abc import ABC,abstractmethod
class Father(ABC):
    def __init__(self,name):
        self.name = name

    @abstractmethod
    def loan(self):
        pass

class Shankar(Father):
    def loan(self):
        print("Giving the 50K loan")

sc = Shankar("Shankar Cheerala")
sc.loan()