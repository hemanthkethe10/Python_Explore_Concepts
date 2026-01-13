arr = [2, 3, -8, 7, -1, 2, 3]

# Naive approach O(n^2)

# max_sum = arr[0]
# for i in range(len(arr)):
#     curr_sum = 0
#     for j in range(i, len(arr)):
#         curr_sum += arr[j]
#         max_sum = max(max_sum, curr_sum)
# print(max_sum)

#Efficient approach O(n)

max_sum = arr[0]
curr_sum = arr[0]
for i in range(1, len(arr)):
    curr_sum = max(arr[i], curr_sum + arr[i])
    max_sum = max(max_sum, curr_sum)
print(max_sum)