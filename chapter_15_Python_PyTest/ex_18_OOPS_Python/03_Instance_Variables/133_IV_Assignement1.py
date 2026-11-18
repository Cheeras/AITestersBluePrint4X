#Assignment 1: 
#Employee Salary Calculator (Real-world HR scenario)
"""
Create a class `Employee` with:
- A **global variable** `company_name = "TechCorp"`
- An **instance variable** `salary` set via constructor
- A **local variable** `bonus` inside a method that calculates total pay
"""
companyName = "TechCorp"
class Employee:
    def __init__(self,name,salary):
        self.name = name
        self.salary = salary

    def calculate_total_Pay(self):
        bonus = 5000
        totalSalary = self.salary + bonus
        print(f"{self.name} at {companyName}")
        print(f"Base Salary {self.salary} Bonus {bonus} and Total salary is {totalSalary}")

emp1 = Employee("Suresh",100000)
emp2 = Employee("Ramesh",220000)
emp1.calculate_total_Pay()
emp2.calculate_total_Pay()