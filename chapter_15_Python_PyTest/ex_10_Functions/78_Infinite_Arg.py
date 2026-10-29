# step 1 - function definition

def print_mul_arg(*list_args):
    # arg - List
    for i in list_args:
        print(i)


# function calling
print_mul_arg("Shankar")
print_mul_arg(2,3,4,5,6,7,9,0)
print_mul_arg("Shankar","Cheerala")
print_mul_arg("Shankar","Cheerala","First")
print_mul_arg("Shankar","Cheerala","First",4.12)
print_mul_arg("Shankar","Cheerala","First",4.12,True)
