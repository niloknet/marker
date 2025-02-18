def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1) # 재귀적으로 함수를 호출 (자기 자신을 호출)

print(factorial(5))  # 120