numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 첫 번째 요소만 출력
print(numbers[0])  # 1

# 마지막 요소만 출력
print(numbers[-1])  # 10

# 두 번째 요소만 출력
print(numbers[1])  # 2

# 뒤에서 두 번째 요소만 출력
print(numbers[-2])  # 9

# 3번째부터 7번째까지 반복
for num in numbers[2:7]:
    print(num)  # 3, 4, 5, 6, 7

# 2번째마다 반복
for num in numbers[::2]:
    print(num)  # 1, 3, 5, 7, 9

# 역순으로 반복
for num in numbers[::-1]:
    print(num)  # 10, 9, 8, 7, 6, 5, 4, 3, 2, 1

# 7번째부터 3번째까지 역순으로 반복
for num in numbers[2:7][::-1]:
    print(num)  # 7, 6, 5, 4, 3

# 뒤에서 5번째부터 뒤에서 8번째까지 반복
for num in numbers[-5:-9:-1]:
    print(num)  # 6, 5, 4, 3

# 2번째마다 역순으로 반복
for num in numbers[::-2]:
    print(num)  # 10, 8, 6, 4, 2
