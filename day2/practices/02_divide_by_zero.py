def divide(a, b):
    # ZeroDivisionError 에러가 났을 때 오류 메세지를 출력하고 None을 반환합니다.
    return a / b


# 테스트
result1 = divide(10, 0)  # 0으로 나눌 때 예외 처리
result2 = divide(10, 2)  # 정상적인 나누기
print(result1)  # 출력: None
print(result2)  # 출력: 5.0
