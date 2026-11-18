class Calc:
    a = None
    b = None

    def __init__(self):
        print("Default constructor")

    def sum(self,a,b):
        return a+b

    def sub(self, a,b):
        return a - b

    def mul(self,a,b):
        return a*b

    def div(self,a,b):
            return a/b

a = float(input("Enter the value of a"))
b = float(input("Enter the value of b"))

objref = Calc()

output_sum = objref.sum(a,b)
output_sub = objref.sub(a,b)
output_mul = objref.mul(a,b)
output_div = objref.div(a,b)


print(output_sum,output_sub,output_mul,output_div)