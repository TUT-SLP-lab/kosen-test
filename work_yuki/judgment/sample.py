import numpy as np 

output = []
result = []
result_list = [0, 0, 0]

for i in range(10):
    num  = np.random.randint(1,4)
    result.append(num)
    result_list[num - 1] += 1
print(result)
print(result_list)
