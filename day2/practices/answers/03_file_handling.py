# numbers.txt에 있는 숫자 목록을 읽어들여
# 짝수의 갯수를 세고
# 그 결과를 result.txt에 써봅시다.
input_filename = "numbers.txt"
output_filename = "result.txt"

# numbers.txt 파일에서 숫자 목록을 읽어들이기
with open(input_filename, "r") as file:
    numbers = [
        int(line.strip()) for line in file.readlines()
    ]  # 각 줄의 숫자를 정수로 변환

# 짝수의 개수 세기
even_count = sum(1 for number in numbers if number % 2 == 0)

# result.txt 파일에 짝수의 개수를 기록하기
with open(output_filename, "w", encoding="utf-8") as file:
    file.write(f"짝수의 개수: {even_count}")
