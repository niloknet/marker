from dynamic_gridworld import DynamicGridWorldEnv
import time

def print_adjacency_list(adj_list):
    """
    인접 리스트를 보기 좋게 출력합니다.
    """
    print("graph_list = {")
    for node, neighbors in adj_list.items():
        # 마지막 항목이 아닐 경우 쉼표 추가
        if node != list(adj_list.keys())[-1]:
            print(f"    {node}: {neighbors},")
        else:
            print(f"    {node}: {neighbors}")
    print("}")

def find_path_dfs(adj_list, start=(0,0), goal=None):
    """
    DFS로 시작점에서 목표점까지의 경로를 찾습니다.
    
    Args:
        adj_list: 그래프의 인접 리스트
        start: 시작 좌표 튜플 (x,y)
        goal: 목표 좌표 튜플 (x,y)
    
    Returns:
        list: 경로를 이루는 좌표 튜플들의 리스트, 경로가 없으면 None
    """
    if goal is None:
        print("도착점을 지정해주세요")
        return None

    visited = []  # 방문한 노드를 추적하기 위한 리스트 
    stack = [(start, [start])]  # (현재 위치, 현재까지의 경로)

    while stack:
        current, path = stack.pop()
        ############ 여기 아래에서 코드를 작성해주세요 ############













        ########################################################

    return None  # 경로를 찾지 못한 경우

# 환경 초기화
env = DynamicGridWorldEnv(size=4)
env.create_maze()

# 인접 리스트 가져오기
adj_list = env.get_adjacency_list()
print("\n인접 리스트 표현:")
print_adjacency_list(adj_list)

# 경로 찾기
goal_pos = (env.size-1, env.size-1)
path = find_path_dfs(adj_list, start=(0,0), goal=goal_pos)

if path:
    print(f"\n찾은 경로: {path}")
    # 찾은 경로대로 이동
    env.follow_path(path)
else:
    print("경로를 찾지 못했습니다.")

# PyGame 창 유지
env.keep_window_open()
