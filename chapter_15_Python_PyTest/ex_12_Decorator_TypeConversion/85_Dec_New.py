def before_after_ui_test(func):
    def wrapper():
        print("1.Before the TC code executed")
        func()
        print("2.After the TC code executed")
    return wrapper

# func == test_ui
@before_after_ui_test
def test_ui():
    print("Hi, I am testing a UI Test")

# function calling
test_ui()

"""
Bottom line: In Python, indentation is not a style choice — 
it's part of the language grammar. One extra space or a 
misplaced dedent changes the meaning (or breaks) your program.
"""
# In Python, indentaion is not a style choice 
# it's part of the language grammar