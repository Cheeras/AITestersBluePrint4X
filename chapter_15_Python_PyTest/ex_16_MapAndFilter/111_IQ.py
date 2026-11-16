name = ["John", "Alice", "Bob", "Eve"]

def uppercase_names(names):
    return names.upper()

up_list = list(map(uppercase_names, name))

print(up_list)