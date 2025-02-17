from dynamic_gridworld import DynamicGridWorldEnv

# 환경 초기화
env = DynamicGridWorldEnv(size=5)

# 패턴을 위한 좌표 정의
pattern_coordinates = [
    (0, 1), (0, 3),
    (1, 0), (1, 2), (1, 4),
    (2, 0), (2, 4),
    (3, 1), (3, 3),
    (4, 2)
]

# 에이전트를 특정 좌표로 이동시키는 함수
def move_to(env, target):
    while tuple(env.agent_pos) != target:
        if env.agent_pos[0] < target[0]:   # 아래로 이동
            env.move_down()
        elif env.agent_pos[0] > target[0]: # 위로 이동
            env.move_up()
        elif env.agent_pos[1] < target[1]: # 오른쪽으로 이동
            env.move_right()
        elif env.agent_pos[1] > target[1]: # 왼쪽으로 이동
            env.move_left()

# 지정된 좌표에 객체를 배치하여 패턴 그리기
for coord in pattern_coordinates:
    move_to(env, coord)  # 에이전트를 해당 좌표로 이동
    env.place()          # 객체 배치

# 관찰을 위해 창을 열어둠
env.keep_window_open()
