import time

def dfs_list(graph, start):
    visited = []  # 방문한 노드를 추적하기 위한 리스트
    stack = [start]  # 시작 노드로 초기화된 스택

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)  # 노드를 방문했다고 표시
            print(f"{node+1} 노드를 방문했습니다.")
            time.sleep(1)

            # 올바른 순회를 위해 연결된 노드들을 역순으로 스택에 추가
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)

    return visited

# 예제 그래프
"""
       1
      / \
     2   3
    / \    \
   4   5    6
"""

# 예제 그래프 (인접 리스트)
graph_list = {
    0: [1, 2],       
    1: [0, 3, 4],    
    2: [0, 5],       
    3: [1],         
    4: [1],         
    5: [2]           
}

# 인점 리스트를 이용해 DFS 실행
print("DFS는 다음과 같은 순서로 탐색을 합니다.")
dfs_list(graph_list, start=0)   # 시작 노드를 인덱스 기준으로 전달 (노드1)

print("\nDFS는 다음과 같은 순서로 탐색을 합니다.")
dfs_list(graph_list, start=4)   # 시작 노드를 인덱스 기준으로 전달 (노드5)
