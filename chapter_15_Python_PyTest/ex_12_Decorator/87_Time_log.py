import time

def time_decorator(func):
    def wrapper():
        func()
        return wrapper

@time_decorator
def test_ui_1():
    print("Add a function, time taken by this function")
    time.sleep(2)


def test_ui_2():
    print("Add a function, time taken by this function")
    time.sleep(2)

    