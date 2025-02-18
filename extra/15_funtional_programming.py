# 순수 함수 (Pure Function)
# 순수 함수는 입력값에 의해서만 출력값이 결정되며, 외부 상태를 변경하지 않습니다.
add_2 = lambda x: x + 2  # 입력 x에 2를 더한 값을 반환하는 순수 함수

# 불변성 (Immutability)
# 기존 데이터를 변경하는 대신 새로운 데이터 구조를 생성합니다.
numbers = [1, 10, 3, 5, 7, 29, 14]  # 원본 리스트

# 내림차순으로 정렬된 새로운 리스트 생성
descending_order_sorted_numbers = sorted(numbers, reverse=True)
print(numbers)  # 원본 리스트는 변경되지 않음
# 출력: [1, 10, 3, 5, 7, 29, 14]
print(descending_order_sorted_numbers)  # 정렬된 새로운 리스트 출력
# 출력: [29, 14, 10, 7, 5, 3, 1]

# 불변성 (Immutability)
# 고차 함수 (Higher-Order Function)
# 고차 함수는 다른 함수를 인자로 받거나 함수를 반환할 수 있는 함수입니다.
added_numbers = list(
    map(add_2, numbers)
)  # 각 요소에 add_2 함수를 적용하여 새로운 리스트 생성
print(numbers)  # 원본 리스트는 변경되지 않음
# 출력: [1, 10, 3, 5, 7, 29, 14]
print(added_numbers)  # 각 요소에 2가 더해진 새로운 리스트 출력
# 출력: [3, 12, 5, 7, 9, 31, 16]


# 지연 평가 (Lazy Evaluation)
# 지연 평가는 표현식의 평가를 필요할 때까지 미루는 전략입니다.
# 파이썬에서는 제너레이터를 사용하여 지연 평가를 구현할 수 있습니다.
def lazy_add_2(numbers):
    for number in numbers:
        yield number + 2  # 각 요소에 2를 더한 값을 생성하고, 함수 실행을 일시 중지


# 사용 예시
lazy_added_numbers = lazy_add_2(numbers)  # 제너레이터 객체 생성
print(next(lazy_added_numbers))  # 첫 번째 값 출력: 3
print(next(lazy_added_numbers))  # 두 번째 값 출력: 12

# 필요시 제너레이터를 리스트로 변환
lazy_added_numbers_list = list(lazy_add_2(numbers))
print(lazy_added_numbers_list)  # 모든 요소에 2가 더해진 리스트 출력
# 출력: [3, 12, 5, 7, 9, 31, 16]
