# Problem - Find the Max amoung 3 numbers
# User inputs - num1, num2, num3 -> int
# output -> int or String with max number

num1 = int(input("Enter the num1\n"))
num2 = int(input("Enter the num2\n"))
num3 = int(input("Enter the num3\n"))

# result = max(num1,num2,num3);
# print(result)

if num1 >= num2 and num1 >= num3:
    print(f"num1 {num1} is greater")
elif num2 >= num3 and num2 >= num1:
    print(f"num2 {num2} is greater")
else:
    print(f"num3 {num3} is greater")