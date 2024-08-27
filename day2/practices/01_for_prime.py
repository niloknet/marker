def is_prime(number):
    """주어진 숫자가 소수인지 여부를 판별하는 함수"""
    if number <= 1:
        return False
    if number <= 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False

    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6

    return True


# 1에서 100까지 숫자를 돌면서 소수인지 아닌지 출력해봅시다
