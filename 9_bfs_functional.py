from collections import deque
import time

def bfs_matrix_functional(graph, start):
    def bfs_recursive(queue, visited):
        if not queue:  # 큐가 비어있으면 종료
            return visited
        
        node = queue.popleft()
        if node not in visited:
            print(f"{node+1} 노드를 방문했습니다.")
            time.sleep(1)
            # 현재 노드와 연결된 노드 중 방문하지 않은 노드를 큐에 추가
            neighbors = [i for i in range(len(graph[node])) if graph[node][i] == 1 and i not in visited]
            return bfs_recursive(queue + deque(neighbors), visited + [node])
        return bfs_recursive(queue, visited)
    
    return bfs_recursive(deque([start]), [])

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

visited_bfs = bfs_matrix_functional(graph_matrix, 0)
print("BFS 방문 순서:", visited_bfs)
