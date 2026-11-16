def triple_number(num):
    return num * 3

print(triple_number(5))  # Output: 15

# Lambda function equivalent
triple = lambda x: x * 3
print(triple(5))  # Output: 15


# example 2

def double_number(num):
    return num * 2

result = lambda num: num * 2
print(result(10))  # Output: 20