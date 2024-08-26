numbers = [1, 2, 3]

for i in range(len(numbers)):
    print(f"i: {i}, numbers: {numbers}")
    if numbers[i] % 2 == 0:
        del numbers[i]
print(numbers)
