# Find the Given positive number is even or odd

num = int(input("Enter a number").strip())

if num >= 0:
    if num%2 == 0:
        print(f"Given number {num} is Even")
    else:
        print(f"Given number {num} is odd")
else:
    print("Negative number")