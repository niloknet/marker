from dynamic_gridworld import DynamicGridWorldEnv

# 환경 초기화 및 깨진 다리 로드
env = DynamicGridWorldEnv(size=9)
env.reset()
env.load_broken_bridge()

# 다리 수리 함수 정의
def fix_pole():
    # 현재 위치에서 아래로 이동하면서 기둥 수리
    for _ in range(5):  # 5번 반복
        # 아래쪽이 비어있는지 확인
        if not env.sense_down()["box"]:
            env.move_down()  # 아래로 이동
            env.place()  # 현재 위치에 기둥 설치
        else:
            env.move_down()  # 아래로 이동
        
    # 원래 높이로 돌아가기
    for _ in range(5):
        env.move_up()
            
    # 다음 위치로 이동

# 전체 다리 수리
for _ in range(9):  # 8칸 이동하며 수리
    y = env.agent_pos[1]  # 현재 y 좌표 저장
    # 현재 위치의 y좌표가 홀수일 때만 수리 진행
    if y % 2 == 0:
        fix_pole()
    env.move_right()
    
env.keep_window_open()
