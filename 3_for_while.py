from dynamic_gridworld import DynamicGridWorldEnv

env = DynamicGridWorldEnv(size=5)

print("지그재그 패턴을 그립니다.")

while True:
    # 오른쪽으로 이동하면서 물체 배치
    for i in range(env.size - 1):  # 오른쪽 끝까지 이동
        env.place()
        env.move_right()
    env.place()  # 오른쪽 끝에서 물체 배치

    if not env.sense_down_wall():  # 아래쪽에 벽이 없으면 이동
        env.move_down()
    else:  # 아래쪽에 벽이 있으면 루프 종료
        print("아래쪽에 벽이 있습니다. 루프를 종료합니다.")
        break

    # 왼쪽으로 이동하면서 물체 배치
    for i in range(env.size - 1):  # 왼쪽 끝까지 이동
        env.place()
        env.move_left()
    env.place()  # 왼쪽 끝에서 물체 배치

    if not env.sense_down_wall():  # 아래쪽에 벽이 없으면 이동
        env.move_down()
    else:  # 아래쪽에 벽이 있으면 루프 종료
        print("아래쪽에 벽이 있습니다. 루프를 종료합니다.")
        break

env.keep_window_open()

