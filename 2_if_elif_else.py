from dynamic_gridworld import DynamicGridWorldEnv

# 환경 초기화
env = DynamicGridWorldEnv(size=5)

# 실행 흐름
env.reset()  # 환경 초기화

# 여러 위치에서 물체 배치 및 확인
env.move_right()  # 오른쪽으로 이동
env.place()       # 현재 위치에 물체 배치
env.move_left()   # 왼쪽으로 이동

# 주변 확인 및 행동 수행
senses = env.sense_all()  # 네 방향 감지 결과 가져오기

if senses["right"]["box"]:  # 오른쪽에 물체가 있는 경우
    print("오른쪽에 물체가 있습니다!")
    env.move_down()
elif senses["left"]["box"]:  # 왼쪽에 물체가 있는 경우
    print("왼쪽에 물체가 있습니다!")
    env.move_up()
elif senses["up"]["box"]:  # 위쪽에 물체가 있는 경우
    print("위쪽에 물체가 있습니다!")
    env.move_down()
elif senses["down"]["box"]:  # 아랫쪽에 물체가 있는 경우
    print("아랫쪽에 물체가 있습니다!")
    env.move_up()
else:  # 주변에 물체가 없는 경우
    print("주변에 물체가 없습니다. 현재 위치에 물체를 배치합니다.")
    env.place()

env.keep_window_open()
