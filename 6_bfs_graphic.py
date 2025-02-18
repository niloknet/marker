import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges for paths from start to middle
start_node = "Start"
middle_node = "Middle"
end_node = "End"

# Path 1: Start -> A1 -> A2 -> Middle
G.add_edge(start_node, "A1")
G.add_edge("A1", "A2")
G.add_edge("A2", middle_node)

# Path 2: Start -> B1 -> B2 -> B3 -> Middle
G.add_edge(start_node, "B1")
G.add_edge("B1", "B2")
G.add_edge("B2", "B3")
G.add_edge("B3", middle_node)

# Path 3: Start -> C1 -> C2 -> Middle
G.add_edge(start_node, "C1")
G.add_edge("C1", "C2")
G.add_edge("C2", middle_node)

# Add nodes and edges for paths from middle to end
# Path 4: Middle -> D1 -> D2 -> D3 -> D4 -> End
G.add_edge(middle_node, "D1")
G.add_edge("D1", "D2")
G.add_edge("D2", "D3")
G.add_edge("D3", "D4")
G.add_edge("D4", end_node)

# Path 5: Middle -> E1 -> E2 -> E3 -> End
G.add_edge(middle_node, "E1")
G.add_edge("E1", "E2")
G.add_edge("E2", "E3")
G.add_edge("E3", end_node)

# 노드 위치 설정 (가로 배치)
pos = {
    # Start 노드
    start_node: (0, 1),
    
    # Start -> Middle 경로
    "A1": (1, 2), "A2": (2, 2),
    "B1": (1, 1), "B2": (2, 1), "B3": (3, 1),
    "C1": (1, 0), "C2": (2, 0),
    
    # Middle 노드
    middle_node: (4, 1),
    
    # Middle -> End 경로
    "D1": (5, 2), "D2": (6, 2), "D3": (7, 2), "D4": (8, 2),
    "E1": (5, 0), "E2": (6, 0), "E3": (7, 0),
    
    # End 노드
    end_node: (9, 1)
}

def bfs_visualize_with_path(graph, start, target, pos):
    visited = set()
    queue = deque([(start, [start])])
    shortest_path = None
    all_steps = []
    
    # BFS 각 단계의 상태를 저장
    while queue and not shortest_path:
        current_queue = list(queue)
        current, path = queue.popleft()
        
        if current not in visited:
            neighbors = list(graph.neighbors(current))
            unvisited_neighbors = [n for n in neighbors if n not in visited]
            
            # 현재 상태 저장
            step_info = {
                'current': current,
                'queue': current_queue,
                'visited': visited.copy(),
                'neighbors': neighbors,
                'unvisited_neighbors': unvisited_neighbors,
                'path': path
            }
            all_steps.append(step_info)
            
            visited.add(current)
            
            if current == target:
                shortest_path = path
                break
                
            for neighbor in unvisited_neighbors:
                queue.append((neighbor, path + [neighbor]))
    
    # 최종 경로 상태 추가
    if shortest_path:
        final_step = {
            'current': 'final',
            'queue': [],
            'visited': visited,
            'neighbors': [],
            'unvisited_neighbors': [],
            'path': shortest_path
        }
        all_steps.append(final_step)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), height_ratios=[3, 1])
    plt.subplots_adjust(hspace=0.3)
    
    def update(frame):
        ax1.clear()
        ax2.clear()
        
        step = all_steps[frame]
        current = step['current']
        queue = step['queue']
        visited_nodes = step['visited']
        path = step['path']
        
        if current == 'final':
            # 최종 경로 표시
            node_colors = ["yellow" if node in path else "lightblue" for node in graph.nodes()]
            edge_colors = [
                "yellow" if (u in path and v in path and 
                            abs(path.index(u) - path.index(v)) == 1) 
                else "gray" for u, v in graph.edges()
            ]
            title = f"Final Shortest Path Found!"
        else:
            # BFS 진행 과정 표시
            node_colors = []
            for node in graph.nodes():
                if node == current:
                    node_colors.append('red')
                elif node in [q[0] for q in queue]:
                    node_colors.append('yellow')
                elif node in visited_nodes:
                    node_colors.append('lightgreen')
                elif node in step['unvisited_neighbors']:
                    node_colors.append('lightblue')
                else:
                    node_colors.append('white')
            
            edge_colors = []
            for (u, v) in graph.edges():
                if u == current and v in step['unvisited_neighbors']:
                    edge_colors.append('blue')
                elif u in visited_nodes and v in visited_nodes:
                    edge_colors.append('green')
                else:
                    edge_colors.append('gray')
            
            title = f"BFS Step {frame + 1}"
        
        # 그래프 그리기
        nx.draw(graph, pos, ax=ax1, with_labels=True,
                node_color=node_colors,
                edge_color=edge_colors,
                node_size=800, font_size=10)
        ax1.set_title(title)
        
        # 상태 정보 표시
        if current == 'final':
            status_text = [
                "Search Complete!",
                f"Shortest Path: {' -> '.join(path)}",
                f"Path Length: {len(path)} nodes"
            ]
        else:
            status_text = [
                f"Current Node: {current}",
                f"Queue: {[q[0] for q in queue]}",
                f"Visited: {visited_nodes}",
                f"Current Path: {' -> '.join(path)}",
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

# BFS 실행 및 시각화
bfs_visualize_with_path(G, "Start", "End", pos)