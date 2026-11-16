test_results = ["PASS","FAIL","PASS","SKIP","FAIL"]

pass_give = list(filter(lambda x: x == "FAIL", test_results))
print(pass_give)