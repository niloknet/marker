def fibonacci_lazy_evaluation(n):
    def fib():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    f = fib()
    for _ in range(n):
        next(f)
    return next(f)

print(fibonacci_lazy_evaluation(10))  # 55
print(fibonacci_lazy_evaluation(20))  # 6765
print(fibonacci_lazy_evaluation(1000))  # 스택 오버플로우가 발생할까요??