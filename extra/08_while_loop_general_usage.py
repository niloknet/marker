# 사용자로부터 입력을 받고, 입력이 "quit"이면 반복을 종료
while True:
    user_input = input("입력하세요: ")
    if user_input == "quit":
        break
    print(user_input)
