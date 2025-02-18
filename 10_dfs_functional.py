import time

def dfs_list_functional(graph, node, visited=None):
    if visited is None:
        visited = []  # 초기화: 방문한 노드 리스트

    if node in visited:
        return visited  # 이미 방문한 노드는 그대로 반환

    # 현재 노드를 방문 처리
    visited = visited + [node]
    print(f"{node+1} 노드를 방문했습니다.")
    time.sleep(1)

    # 이웃 노드들을 재귀적으로 탐색
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited = dfs_list_functional(graph, neighbor, visited)

    return visited
    
# 예제 그래프
"""
       1
      / \
     2   3
    / \    \
   4   5    6
"""
# Example graph (adjacency list)
graph_list = {
    0: [1, 2],       # Node 1 is connected to Node 2 and Node 3
    1: [0, 3, 4],    # Node 2 is connected to Node 1, Node 4, and Node 5
    2: [0, 5],       # Node 3 is connected to Node 1 and Node 6
    3: [1],          # Node 4 is connected to Node 2
    4: [1],          # Node 5 is connected to Node 2
    5: [2]           # Node 6 is connected to Node 3
}

visited_dfs = dfs_list_functional(graph_list, 0)
print("DFS 방문 순서:", visited_dfs)
