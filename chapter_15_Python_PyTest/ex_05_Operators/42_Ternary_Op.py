user_age = int(input("Enter your age \n"))

if user_age >= 18:
    print("Yes You are eligilble for vote")
else: 
    print("No You are not eligible for vote")

print("Yes You are eligible for vote - P" if user_age >= 18 else "You are not eligible to cast vote - P")

# Open the termminal and run the following command
# python "d:\Workspace\AITestersBluePrint4X\chapter_15_Python_PyTest\ex_05_Operators\42_Ternary_Op.py"