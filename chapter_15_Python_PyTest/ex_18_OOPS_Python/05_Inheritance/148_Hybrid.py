#Hybrid Inheritance
# A mix of multiple and multilevel inheritance
class Base:
    def base_method(self):
        print("Base Method")

class A(Base):
    def a_method(self):
        print("A Method")

class B(Base):
    def b_method(self):
        print("B Method")

class C(A,B):
    def c_method(self):
        print("C method")

obj_ref = C()
obj_ref.base_method()
obj_ref.a_method()
obj_ref.b_method()
obj_ref.c_method()