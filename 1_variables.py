from dynamic_gridworld import DynamicGridWorldEnv

# 환경 생성
env = DynamicGridWorldEnv(size=5)

# 변수에 현재 위치 저장
saved_pos_x = env.agent_pos[0]
saved_pos_y = env.agent_pos[1]

print(f"저장된 X 좌표: {saved_pos_x}, 저장된 Y 좌표: {saved_pos_y}")
print(f"저장된 좌표: ({saved_pos_x}, {saved_pos_y})")

# 아래로 이동
env.move_down()

print(f"저장된 좌표: ({saved_pos_x}, {saved_pos_y})")
print(f"현재 좌표: ({env.agent_pos[0]}, {env.agent_pos[1]})")

# 현재 위치와 이전 위치 비교하여 차이를 변수에 저장
difference_x = env.agent_pos[0] - saved_pos_x
difference_y = env.agent_pos[1] - saved_pos_y

print(f"지금과 이전의 좌표 차이 ({difference_x}, {difference_y})")

env.keep_window_open()
