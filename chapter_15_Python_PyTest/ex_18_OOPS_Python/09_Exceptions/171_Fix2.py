try:
    a = int(input("Enter num 1"))
    b = int(input("Enter num 2"))
    c = a / b
    print(c)
except (ZeroDivisionError, ValueError, TypeError, NameError):
    print("Error due to ZDE or value")
