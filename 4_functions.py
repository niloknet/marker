from dynamic_gridworld import DynamicGridWorldEnv

# 환경 생성
env = DynamicGridWorldEnv(size=5)

# 지정한 횟수 만큼 박스를 두고 오른쪽으로 한 칸 이동하는 이동하는 함수
def place_and_move_right(x):
    for _ in range(x):
        env.place()
        env.move_right()

env.move_down()
place_and_move_right(3)

env.keep_window_open()
