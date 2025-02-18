# 리스트 끝에 요소를 추가하는 방법
numbers = [1, 2]
numbers.append(3)
print(numbers)  # [1, 2, 3]

# 리스트의 특정 위치에 요소를 추가하는 방법
my_list = [2, 3, 4]
my_list.insert(0, 1)  # 위치 0에 1을 삽입
print(my_list)  # [1, 2, 3, 4]

# 리스트 끝에 요소를 빼는 방법
numbers = [1, 2, 3]
pop_number = numbers.pop()
print(pop_number)  # 3
print(numbers)  # [1, 2]

# 리스트의 특정 위치의 요소를 제거하는 방법
numbers = [1, 2, 3]
pop_number = numbers.pop(0)  # 위치 0의 요소를 제거
print(pop_number)  # 1
print(numbers)  # [2, 3]

# 리스트의 특정 요소를 제거하는 방법
numbers = [1, 2, 3, 4, 5]
numbers.remove(4)
print(numbers)  # [1, 2, 3, 5]

# 리스트 이어붙이기
list1 = [1, 2, 3]
list2 = [4, 5, 6]
concatenated_list = list1 + list2
print(concatenated_list)  # [1, 2, 3, 4, 5, 6]

# 리스트의 모든 요소에 특정 작업을 하기
# for 반복문을 통해서 하는 방법
numbers = [1, 2, 3, 4, 5]
increased_numbers = []
for number in numbers:
    increased_numbers.append(number**2 + 2)
print(increased_numbers)  # [3, 6, 11, 18, 27]

# 리스트 컴프리헨션 방법
numbers = [1, 2, 3, 4, 5]
increased_numbers = [number**2 + 2 for number in numbers]
print(increased_numbers)  # [3, 6, 11, 18, 27]

# map 과 람다(lambda) 를 이용한 방법
numbers = [1, 2, 3, 4, 5]
squared_numbers = list(map(lambda x: x**2 + 2, numbers))
print(squared_numbers)  # [3, 6, 11, 18, 27]

# 리스트 정렬하기
unsorted_list = [5, 2, 9, 1, 5, 6]
sorted_list = sorted(unsorted_list)
print(sorted_list)  # [1, 2, 5, 5, 6, 9]

# 리스트에서 특정 조건의 요소를 남기기
# for 루프를 쓰는 방법
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even_numbers = []
for x in numbers:
    if x % 2 == 0:
        even_numbers.append(x)
print(even_numbers)  # [2, 4, 6, 8]

# 리스트 컴프리헨션 방법
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even_numbers = [x for x in numbers if x % 2 == 0]
print(even_numbers)  # [2, 4, 6, 8]

# filter 과 람다(lambda) 를 이용한 방법
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # [2, 4, 6, 8]

# 중첩된 2차원 리스트를 1차원 리스트로 만들기
nested_list = [[1, 2, 3], [4, 5], [6, 7, 8]]
flattened_list = sum(nested_list, [])
print(flattened_list)  # [1, 2, 3, 4, 5, 6, 7, 8]
