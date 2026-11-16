student_infor1 = {
    "name": "Vinod",
    "age": 76,
    "address": {
        "home_address":"AP",
        "office_address":"TS"
    }
}

student_infor2 = {
    "name": "Venky",
    "age": 45,
    "address": {
        "home_address":"GOA",
        "office_address":"KA"
    }
}

student_list = [student_infor1,student_infor2]

print(student_list)
print(student_list[0])
print(student_list[0]["name"])
print(student_list[1]["age"])
print(student_list[0]["address"]["office_address"])

