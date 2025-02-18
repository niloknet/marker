import time
from collections import deque

# BFS 함수 (인접 행렬 기반)
def bfs_matrix(graph, start):
    visited = []  # 방문한 노드 리스트
    queue = deque([start])  # 시작 노드를 큐에 추가
    n = len(graph)  # 그래프의 크기 (노드 개수)

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)  # 방문 처리
            print(f"{node+1} 노드를 방문했습니다.")
            time.sleep(1)

            # 현재 노드와 연결된 모든 노드 탐색
            for i in range(n):
                if graph[node][i] == 1 and i not in visited:  # 연결되어 있고 방문하지 않은 경우
                    queue.append(i)

    return visited

# 예제 그래프
"""
       1
      / \
     2   3
    / \    \
   4   5    6
"""

graph_matrix = [
    [0, 1, 1, 0, 0, 0],
    [1, 0, 0, 1, 1, 0],
    [1, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0]
]

# BFS 실행
print("BFS는 다음과 같은 순서로 탐색을 합니다.")
bfs_matrix(graph_matrix, start=0)   # 시작 노드를 인덱스 기준으로 전달 (노드1)

print("\nBFS는 다음과 같은 순서로 탐색을 합니다.")
bfs_matrix(graph_matrix, start=4)   # 시작 노드를 인덱스 기준으로 전달 (노드5)
