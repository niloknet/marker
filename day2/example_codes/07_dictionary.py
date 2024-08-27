# 딕셔너리 생성
student = {"name": "Alice", "age": 25, "courses": ["Math", "Science"]}

# 값 조회
print(student["name"])  # 출력: Alice

# 값 추가 및 수정
student["age"] = 26
student["grade"] = "A"

# 값 삭제
del student["courses"]

print(student)  # 출력: {'name': 'Alice', 'age': 26, 'grade': 'A'}
