import os

print("CWD:",os.getcwd())
print("OS:", os.name)

folder = os.path.join(os.getcwd(),"demo_output")
print(folder)

os.makedirs(folder, exist_ok=True)