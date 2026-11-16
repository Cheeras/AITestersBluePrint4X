response_time_ms = [1500,300,1600]

def mil_sec(milliseconds):
    return milliseconds / 1000
response_time_sec = list(map(mil_sec, response_time_ms))
# print(response_time_sec)

response_time_ms_list  =  list(map(lambda ms: ms/1000, response_time_ms))
print(response_time_ms_list)