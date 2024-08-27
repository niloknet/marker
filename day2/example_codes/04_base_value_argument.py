def base_convert(number, base=10):
    if base < 2:
        return "Base must be >= 2"
    if number == 0:
        return "0"

    digits = []
    is_negative = number < 0
    number = abs(number)

    while number:
        digits.append(str(number % base))
        number //= base

    if is_negative:
        return "-" + "".join(reversed(digits))

    return "".join(reversed(digits))


decimal_str = base_convert(100)  # 기본값인 10진법으로 변환
binary_str = base_convert(100, 2)  # 2진법으로 변환
hexadecimal_str = base_convert(100, 16)  # 16진법으로 변환
octal_str = base_convert(100, 8)  # 8진법으로 변환

print(f"100은 10진법으로 {decimal_str} 입니다.")  # 100
print(f"100은 2진법으로 {binary_str} 입니다.")  # 1100100
print(f"100은 16진법으로 {hexadecimal_str} 입니다.")  # 64
print(f"100은 8진법으로 {octal_str} 입니다.")  # 144
