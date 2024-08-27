def divide(a, b):
    try:
        return a / b
    except:
        raise


result = None
try:
    result = divide(10, 0)
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다.")

print(result)  # None
