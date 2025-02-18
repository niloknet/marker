from dynamic_gridworld import DynamicGridWorldEnv
from collections import deque
import time

def print_adjacency_matrix(adj_matrix, size):
    """
    인접 행렬을 보기 좋게 출력합니다.
    
    Args:
        adj_matrix: 인접 행렬
        size: 그리드 월드의 크기
    """
    n = size * size
    print("\n인접 행렬:")
    print("   ", end="")
    for i in range(n):
        print(f"({i//size},{i%size})", end=" ")
    print("\n" + "-" * (n * 7 + 4))
    
    for i in range(n):
        print(f"({i//size},{i%size})", end=" ")
        for j in range(n):
            print(f"{adj_matrix[i][j]:^5}", end=" ")
        print()

def find_path_bfs(adj_matrix, size, start=(0,0), goal=None):
    """
    BFS로 시작점에서 목표점까지의 최단 경로를 찾습니다.
    
    Args:
        adj_matrix: 인접 행렬
        size: 그리드 월드의 크기
        start: 시작 좌표 튜플 (x,y)
        goal: 목표 좌표 튜플 (x,y)
    
    Returns:
        list: 최단 경로를 이루는 좌표 튜플들의 리스트, 경로가 없으면 None
    """
    if goal is None:
        print("도착점을 지정해주세요")
        return None
        
    size = int(len(adj_matrix) ** 0.5)  # 그리드 크기 계산
    start_idx = start[0] * size + start[1]
    goal_idx = goal[0] * size + goal[1]
    
    visited = []
    parent = [-1] * len(adj_matrix)  # 각 노드의 부모 노드를 저장
    queue = deque([start_idx])
    
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            print(f"({node//size},{node%size}) 좌표를 방문했습니다.")
            time.sleep(0.5)
            
            if node == goal_idx:
                # 경로 재구성
                path = []
                current = node
                while current != -1:
                    path.append((current//size, current%size))
                    current = parent[current]
                return path[::-1]
            
            for i in range(len(adj_matrix)):
                if adj_matrix[node][i] == 1 and i not in visited:
                    queue.append(i)
                    if parent[i] == -1:  # 아직 부모가 설정되지 않은 경우에만
                        parent[i] = node
    
    return None

# 환경 초기화
env = DynamicGridWorldEnv(size=4)
env.create_maze()

# 인접 행렬 가져오기
adj_matrix = env.get_adjacency_matrix()
print_adjacency_matrix(adj_matrix, env.size)

# 경로 찾기
goal_pos = (env.size-1, env.size-1)
path = find_path_bfs(adj_matrix, env.size, start=(0,0), goal=goal_pos)

if path:
    print(f"\n찾은 경로: {path}")
    # 찾은 경로대로 이동
    env.follow_path(path)
else:
    print("경로를 찾지 못했습니다.")

# PyGame 창 유지
env.keep_window_open()
