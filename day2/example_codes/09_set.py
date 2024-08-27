# 집합 생성
fruits = {"apple", "banana", "cherry"}

# 요소 추가
fruits.add("orange")

# 요소 제거
fruits.remove("banana")

# 집합 연산
other_fruits = {"cherry", "mango"}
union_set = fruits.union(other_fruits)
intersection_set = fruits.intersection(other_fruits)

print(union_set)  # 출력: {'cherry', 'mango', 'orange', 'apple'}
print(intersection_set)  # 출력: {'cherry'}
