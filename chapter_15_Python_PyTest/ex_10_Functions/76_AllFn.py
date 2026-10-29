# build in functions
import math

# built in functions
result = max(12,23)
print(result)

# 1 . They can't return -> non return
# No Return Type and No Parameter / Argument - NRNP

def greet():
    print("Hello")

greet()

# 2 No Return type and With argument/param

print("No Return type and With argument/param")
def greet_by_name(name):
    print("Hello",name)

greet_by_name("Shankar")
# 3 No Return Type and with Default Argument( # Positional arguments)
def say_hello_default_arg(name ="shankar"):
    print("Hello",name.upper())

say_hello_default_arg("Cheerala")
say_hello_default_arg()

# Multiple argments
def multiple_args(name1="A", name2 = "B"):
    print("Mul --> ",name1,name2)

multiple_args()
multiple_args("Cheeras","Sharma")
multiple_args(name1="Cheeras")
multiple_args(name1="Sravya",name2="latha")
multiple_args(name2="Sumith")

# def test(name)
#  return name
# test("test")

# 4 Argument and return type

# Step 1 - Function defination
def sum_of_Two(a,b):
    return  a + b

# Step 2 - Function calling

result = sum_of_Two(4,56)
print(result)

def sum_of_two_number_with_default(num1=100, num2=200):
    print("I will sum the two numbers!")
    return num1 + num2

result = sum_of_two_number_with_default(num1=11, num2=22)
print(result)

result = sum_of_two_number_with_default()
print(result)