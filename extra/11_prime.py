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


if is_prime(16):
    print("16은 소수입니다.")
else:
    print("16은 소수가 아닙니다.")
# 16은 소수가 아닙니다.

if is_prime(17):
    print("17은 소수입니다.")
else:
    print("17은 소수가 아닙니다.")
# 17은 소수입니다.
