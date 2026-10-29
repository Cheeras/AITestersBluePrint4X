# Step 1 - function defination

def sum_three(a=1,b=1,c=1):
    return a + b + c

result1 = sum_three()
print(result1)

result2 = sum_three(10,20)
print(result1)

result3 = sum_three(10,20,30)
print(result3)

result4 = sum_three(b=22, a=10, c= 45)
print(result4)

result5 = sum_three(b=67,a=10,c=20)
print(result5)

result6 = sum_three(a=10, b=30, c=49)
print(result6)