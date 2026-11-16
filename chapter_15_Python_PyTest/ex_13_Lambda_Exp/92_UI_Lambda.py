user_input = int(input("Enter the number"))
check_even_odd_function = lambda num: "Even" if num % 2 == 0 else "Odd"
result = check_even_odd_function(user_input)
print(f"The number {user_input} is {result}.")

# Alternate in one line
print((lambda num: "Even" if num % 2 == 0 else "Odd")(int(input("Enter Number: "))))

import math
op2 = lambda: math.pow(int(input("Enter the number")),2)

print(f"The square of the number is {op2()}.")