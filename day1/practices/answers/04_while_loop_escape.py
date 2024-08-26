import random

# 1-100 사이의 숫자를 랜덤으로 정하기
random_number = random.randint(1, 100)

# 맞출 때까지 반복하기
while True:
    # 사용자로부터 입력 받기
    guess = int(input("1-100 사이의 숫자를 맞춰보세요: "))

    # 입력이 랜덤 숫자보다 낮은 경우
    if guess < random_number:
        print("너무 낮습니다.")
    # 입력이 랜덤 숫자보다 높은 경우
    elif guess > random_number:
        print("너무 높습니다.")
    # 입력이 랜덤 숫자와 일치하는 경우
    else:
        print("정답입니다!")
        break
