import networkx as nx
import heapq
import matplotlib.pyplot as plt
import random
import time

# 그래프 시각화 함수
def visualize_graph(graph, pos, shortest_paths, previous_nodes, current_node, step):
    plt.clf()  # 이전 플롯 지우기
    
    # 모든 엣지를 기본 색으로 그리기
    nx.draw(graph, pos=pos, with_labels=False,
            node_color="lightblue", edge_color="gray", node_size=3000,
            font_size=10)
    
    # 현재까지 방문한 경로 강조 표시
    for node in graph.nodes:
        if previous_nodes[node] is not None:
            nx.draw_networkx_edges(
                graph,
                pos,
                edgelist=[(previous_nodes[node], node)],
                edge_color="blue",
                width=2.5,
            )
    
    # 현재 노드 강조 표시
    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=[current_node],
        node_color="red",
        node_size=3000,
    )
    

    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph,
                                 pos,
                                 edge_labels=edge_labels,
                                 font_size=10)
    # 최단 거리 정보 표시
    labels = {node: f"{node}\n({shortest_paths[node]})" for node in graph.nodes}
    nx.draw_networkx_labels(graph, pos=pos, labels=labels)
    
    plt.title(f"Step {step}: Current Node = {current_node}")
def dijkstra_with_visualization(graph, start_node, end_node):
    # 초기화
    shortest_paths = {node: float('inf') for node in graph.nodes}
    shortest_paths[start_node] = 0
    previous_nodes = {node: None for node in graph.nodes}
    priority_queue = [(0, start_node)]
    visited = set()
    
    # 모든 단계를 저장할 리스트
    all_steps = []
    
    # 각 단계의 상태 저장
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        # 현재 상태 저장
        step_info = {
            'current_node': current_node,
            'shortest_paths': shortest_paths.copy(),
            'previous_nodes': previous_nodes.copy(),
            'visited': visited.copy()
        }
        all_steps.append(step_info)
        
        if current_node == end_node:
            break
            
        for neighbor in graph.neighbors(current_node):
            if neighbor in visited:
                continue
                
            edge_weight = graph[current_node][neighbor]['weight']
            new_distance = shortest_paths[current_node] + edge_weight
            
            if new_distance < shortest_paths[neighbor]:
                shortest_paths[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))
    
    # 최종 경로 상태 추가
    final_path = reconstruct_path(previous_nodes, start_node, end_node)
    final_step = {
        'current_node': 'final',
        'shortest_paths': shortest_paths,
        'previous_nodes': previous_nodes,
        'visited': visited,
        'final_path': final_path
    }
    all_steps.append(final_step)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), height_ratios=[3, 1])
    plt.subplots_adjust(hspace=0.3)
    
    def update(frame):
        ax1.clear()
        ax2.clear()
        
        step = all_steps[frame]
        current_node = step['current_node']
        shortest_paths = step['shortest_paths']
        previous_nodes = step['previous_nodes']
        
        if current_node == 'final':
            # 최종 경로 표시
            final_path = step['final_path']
            node_colors = ["yellow" if node in final_path else "lightblue" for node in G.nodes]
            edge_colors = [
                "yellow" if (u in final_path and v in final_path and 
                            abs(final_path.index(u) - final_path.index(v)) == 1)
                else "gray" for u, v in G.edges()
            ]
            title = f"Final Shortest Path | Total Cost: {shortest_paths[end_node]}"
        else:
            # 진행 중인 상태 표시
            node_colors = ["red" if node == current_node 
                         else "lightgreen" if shortest_paths[node] < float('inf')
                         else "lightblue" for node in G.nodes]
            edge_colors = ["blue" if previous_nodes[v] == u else "gray" 
                         for u, v in G.edges()]
            title = f"Step {frame + 1}: Current Node = {current_node}"
        
        # 그래프 그리기
        nx.draw(G, pos=pos, ax=ax1,
                with_labels=False,
                node_color=node_colors,
                edge_color=edge_colors,
                node_size=3000,
                font_size=10)
        
        # 엣지 가중치 표시
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax1)
        
        # 노드 레이블 표시
        labels = {node: f"{node}\n({shortest_paths[node]})" for node in graph.nodes}
        nx.draw_networkx_labels(graph, pos=pos, labels=labels, ax=ax1)
        
        ax1.set_title(title)
        
        # 상태 정보 표시
        if current_node == 'final':
            status_text = [
                "Search Complete!",
                f"Shortest Path: {' -> '.join(step['final_path'])}",
                f"Total Cost: {shortest_paths[end_node]}"
            ]
        else:
            status_text = [
                f"Current Node: {current_node}",
                f"Visited Nodes: {step['visited']}",
                f"Current Shortest Paths: {dict(shortest_paths)}"
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
    
    return final_path, shortest_paths[end_node]

def reconstruct_path(previous_nodes, start_node, end_node):
    path = []
    current_node = end_node
    
    while current_node is not None:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]
        
    return path

# 메인 코드 실행
if __name__ == "__main__":
    start_node = "Start"
    middle_node = "Middle"
    end_node = "End"
    nodes = ['Start', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'Middle', 'D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'End']  # B3, D4 제거

    adj_matrix = [
        [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Start
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A1
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # A2
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # B1
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # B2 (Middle로 연결)
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # C1
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # C2
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],  # Middle
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # D1
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # D2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # D3 (End로 연결)
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # E1
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # E2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # E3
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # End
    ]

    # 가중치가 있는 인접 행렬 생성 (0은 연결되지 않음, 양수는 가중치)
    weighted_matrix = []
    for row in adj_matrix:
        weighted_row = []
        for cell in row:
            if cell == 1:
                # 1-10 사이의 랜덤 가중치 부여
                weighted_row.append(random.randint(1, 10))
            else:
                weighted_row.append(0)
        weighted_matrix.append(weighted_row)

    # NetworkX 그래프 생성
    G = nx.DiGraph()

    # 노드 추가
    for node in nodes:
        G.add_node(node)

    # 엣지 추가 (가중치 포함)
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if weighted_matrix[i][j] > 0:
                G.add_edge(nodes[i], nodes[j], weight=weighted_matrix[i][j])

    # 노드 위치 설정 (가로 배치)
    # 노드 위치 설정 (가로 배치)
    pos = {
        # Start 노드
        start_node: (0, 1),
        
        # Start -> Middle 경로
        "A1": (1, 2), "A2": (2, 2),
        "B1": (1, 1), "B2": (2, 1), 
        "C1": (1, 0), "C2": (2, 0),
        
        # Middle 노드
        middle_node: (4, 1),
        
        # Middle -> End 경로
        "D1": (5, 2), "D2": (6, 2), "D3": (7, 2),
        "E1": (5, 0), "E2": (6, 0), "E3": (7, 0),
        
        # End 노드
        end_node: (9, 1)
    }

    # 다익스트라 알고리즘 실행
    shortest_path, total_distance = dijkstra_with_visualization(G, start_node, end_node)

    # 최종 결과 출력
    print("Shortest Path:", shortest_path)
    print("Total Distance:", total_distance)
    
    plt.show()
