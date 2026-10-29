# Step 1 - function defination
def display_information(name, role):
    print(f"Name: {name}, role is {role}")

# Step 2 - function calling
display_information(name="Shankar",role="QA")
display_information(role="QA Automation",name="Shankar")
"""
Keyword arguments are matched by parameter name, so order does not matter.
"""