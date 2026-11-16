numbers = [1,2,3,4,5]
def sq(x):
    return x**2

# for n in numbers:
#     print(sq(n))

all_squared = list(map(sq,numbers))
# here map takes function to apply and data to process

print(all_squared)