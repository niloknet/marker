from dynamic_gridworld import DynamicGridWorldEnv

env = DynamicGridWorldEnv(size=5)

print("체크무늬 패턴을 그립니다.")

# 체크무늬 패턴 생성
for row in range(env.size):
    for col in range(env.size):
        # 짝수 행-짝수 열 또는 홀수 행-홀수 열에 물체 배치
        if (row + col) % 2 == 0:
            env.place()
        # 오른쪽으로 이동 (마지막 열에서는 이동하지 않음)
        if col < env.size - 1:
            env.move_right()
    
    # 다음 행으로 이동
    if row < env.size - 1:
        env.move_down()
        # 항상 왼쪽 끝으로 이동
        for _ in range(env.size - 1):
            env.move_left()

env.keep_window_open()
