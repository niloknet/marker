from dynamic_gridworld import DynamicGridWorldEnv

# 환경 초기화 및 깨진 다리 로드
env = DynamicGridWorldEnv(size=9)
env.reset()
env.load_broken_bridge()

# 다리 수리 함수 정의
def fix_pole():
    ############ 여기 아래에서 코드를 작성해주세요 ############












    ########################################################

# 전체 다리 수리
for _ in range(9):  # 8칸 이동하며 수리
    y = env.agent_pos[1]  # 현재 y 좌표 저장
    # 현재 위치의 y좌표가 홀수일 때만 수리 진행
    if y % 2 == 0:
        fix_pole()
    env.move_right()
    
env.keep_window_open()
