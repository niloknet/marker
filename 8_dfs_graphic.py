import networkx as nx
import matplotlib.pyplot as plt
from time import sleep

def dfs_visualize_with_info(graph, start, pos):
    visited = set()
    stack = [start]
    all_steps = []
    
    # 각 단계의 상태를 저장
    while stack:
        current = stack[-1]  # 스택의 top 확인
        
        if current not in visited:
            visited.add(current)
            neighbors = list(graph.neighbors(current))
            unvisited_neighbors = [n for n in neighbors if n not in visited]
            
            # 현재 상태 저장
            step_info = {
                'current': current,
                'stack': stack.copy(),
                'visited': visited.copy(),
                'neighbors': neighbors,
                'unvisited_neighbors': unvisited_neighbors
            }
            all_steps.append(step_info)
            
            # 방문하지 않은 이웃 노드들을 스택에 추가
            for neighbor in reversed(unvisited_neighbors):
                stack.append(neighbor)
        else:
            stack.pop()  # 이미 방문한 노드는 스택에서 제거
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), height_ratios=[3, 1])
    plt.subplots_adjust(hspace=0.3)
    
    def update(frame):
        ax1.clear()
        ax2.clear()
        
        step = all_steps[frame]
        current = step['current']
        stack = step['stack']
        visited_nodes = step['visited']
        
        # 노드 색상 설정
        node_colors = []
        for node in graph.nodes():
            if node == current:
                node_colors.append('red')  # 현재 노드
            elif node in stack:
                node_colors.append('yellow')  # 스택에 있는 노드
            elif node in visited_nodes:
                node_colors.append('lightgreen')  # 방문한 노드
            elif node in step['unvisited_neighbors']:
                node_colors.append('lightblue')  # 방문하지 않은 이웃 노드
            else:
                node_colors.append('white')  # 기타 노드
        
        # 엣지 색상 설정
        edge_colors = []
        for (u, v) in graph.edges():
            if u == current and v in step['unvisited_neighbors']:
                edge_colors.append('blue')  # 현재 탐색 중인 엣지
            elif u in visited_nodes and v in visited_nodes:
                edge_colors.append('green')  # 이미 탐색한 엣지
            else:
                edge_colors.append('gray')  # 미탐색 엣지
        
        # 그래프 그리기
        nx.draw(graph, pos, ax=ax1, with_labels=True,
                node_color=node_colors,
                edge_color=edge_colors,
                node_size=800, font_size=10)
        ax1.set_title(f"DFS Step {frame + 1}")
        
        # 상태 정보 표시
        status_text = [
            f"Current Node: {current}",
            f"Stack: {stack}",
            f"Visited: {visited_nodes}",
            f"Unvisited Neighbors: {step['unvisited_neighbors']}"
        ]
        
        ax2.text(0.1, 0.5, '\n'.join(status_text), fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8))
        ax2.axis('off')
    
    # 키보드 이벤트 핸들러
    current_frame = [0]
    
    def on_key(event):
        if event.key == 'right' and current_frame[0] < len(all_steps) - 1:
            current_frame[0] += 1
        elif event.key == 'left' and current_frame[0] > 0:
            current_frame[0] -= 1
        update(current_frame[0])
        plt.draw()
    
    fig.canvas.mpl_connect('key_press_event', on_key)
    
    # 초기 프레임 표시
    update(0)
    plt.show()

# 그래프 생성
G = nx.DiGraph()
edges = [
    ("A", "B"), ("A", "C"),
    ("B", "D"), ("B", "E"),
    ("C", "F"), ("C", "G"),
    ("E", "H"), ("E", "I")
]
G.add_edges_from(edges)

# 노드 위치 설정
pos = {
    "A": (0, 0),
    "B": (-1, -1),
    "C": (1, -1),
    "D": (-1.5, -2),
    "E": (-0.5, -2),
    "F": (0.5, -2),
    "G": (1.5, -2),
    "H": (-0.75, -3),
    "I": (-0.25, -3)
}

# DFS 실행 및 시각화
print("DFS Visualization (Use left/right arrow keys to navigate):")
dfs_visualize_with_info(G, "A", pos)
