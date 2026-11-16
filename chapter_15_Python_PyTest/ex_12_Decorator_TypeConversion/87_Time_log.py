import time

def time_decorator(func):
    def wrapper():
        start_time = time.time()
        print("start time: ", start_time)
        func()
        end_time = time.time()
        print("end time: ", end_time)
        print("Total time taken by the function: ", end_time - start_time)
    return wrapper

def print_logs(func):
    def wrapper():
        print("Start the logs")
        func()
        print("End the logs")
    return wrapper

@time_decorator
@print_logs
def test_ui_1():
    print("Add a fuction, time taken by this funciton 1")
    time.sleep(2)

def test_ui_2():
    print("Add a function, time taken by this function 2")
    time.sleep(5)

print("-----------------")

#with decorator
test_ui_1()

#without decorator
test_ui_2()