class Bomb:
    def __init__(self, counter):
        self._counter = counter  # 보호된 카운터로 설정 (관례적으로 보호)

    def tick(self):
        print(f"카운터: {self._counter}")
        self._counter -= 1
        if self._counter <= 0:
            print(f"카운터: {self._counter}")
            print("폭탄이 터졌습니다!")


bomb = Bomb(10)  # 10초뒤에 터지는 폭탄을 설치

# 5초가 지나고...
for _ in range(5):
    bomb.tick()

# 폭탄을 발견했습니다!
# 폭탄의 카운터를 직접 조작해서
# 폭탄 처리반이 도착할 때까지 폭탄이 터지지 않게 해봅시다.
print("--- 카운터를 해킹합니다 ---")


# 카운트다운 계속
for _ in range(5):
    bomb.tick()
