
import networkx as nx
import heapq
import random
import time
import math 

# 힙을 사용하는 다익스트라 알고리즘
def dijkstra_with_heap(graph, start_node):
    shortest_paths = {node: float('inf') for node in graph.nodes}
    shortest_paths[start_node] = 0
    priority_queue = [(0, start_node)]
    visited = set()
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        for neighbor in graph.neighbors(current_node):
            if neighbor in visited:
                continue
                
            distance = current_distance + graph[current_node][neighbor]['weight']
            
            if distance < shortest_paths[neighbor]:
                shortest_paths[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return shortest_paths

def create_random_graph_with_coordinates(n_nodes, edge_density):
    G = nx.DiGraph()
    
    # 노드 추가 및 좌표 생성
    nodes = list(range(n_nodes))
    coordinates = {node: (random.uniform(0, 100), random.uniform(0, 100)) for node in nodes}
    G.add_nodes_from(nodes)
    
    # 엣지 추가
    for i in nodes:
        for j in nodes:
            if i != j and random.random() < edge_density:
                # 두 노드 간의 유클리드 거리 계산
                x1, y1 = coordinates[i]
                x2, y2 = coordinates[j]
                distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                G.add_edge(i, j, weight=distance)
    
    return G


def create_random_graph_with_coordinates(n_nodes, edge_density, start_node=0, end_node=None):
    if end_node is None:
        end_node = n_nodes - 1
        
    while True:  # 조건을 만족하는 그래프가 생성될 때까지 반복
        G = nx.DiGraph()
        
        # 노드 추가 및 좌표 생성
        nodes = list(range(n_nodes))
        coordinates = {node: (random.uniform(0, 100), random.uniform(0, 100)) for node in nodes}
        G.add_nodes_from(nodes)
        
        # 엣지 추가
        for i in nodes:
            for j in nodes:
                if i != j and random.random() < edge_density:
                    x1, y1 = coordinates[i]
                    x2, y2 = coordinates[j]
                    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    G.add_edge(i, j, weight=distance)
        
        # 시작 노드에서 종료 노드까지의 경로가 존재하는지 확인
        try:
            path_exists = nx.has_path(G, start_node, end_node)
        except nx.NetworkXError:
            path_exists = False
            
        # 경로가 존재하면 그래프 반환
        if path_exists:
            return G, coordinates


def euclidean_heuristic(current_coords, target_coords):
    x1, y1 = current_coords
    x2, y2 = target_coords
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def astar_with_heap(graph, coordinates, start_node, target_node):
    shortest_paths = {node: float('inf') for node in graph.nodes}
    shortest_paths[start_node] = 0
    priority_queue = [(0, start_node)]
    visited = set()
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        if current_node == target_node:
            break
            
        for neighbor in graph.neighbors(current_node):
            if neighbor in visited:
                continue
                
            # 실제 거리 계산
            distance = current_distance + graph[current_node][neighbor]['weight']
            
            if distance < shortest_paths[neighbor]:
                # 휴리스틱 값 계산
                h = euclidean_heuristic(coordinates[neighbor], coordinates[target_node])
                f = distance + h  # f = g + h
                shortest_paths[neighbor] = distance  # g값 저장
                heapq.heappush(priority_queue, (f, neighbor))
    
    return shortest_paths

def run_comparison_test(n_nodes, edge_density):
    # 랜덤 그래프 생성
    G, coordinates = create_random_graph_with_coordinates(n_nodes, edge_density)
    start_node = 0
    target_node = n_nodes - 1
    
    # 다익스트라 알고리즘 테스트
    start_time = time.perf_counter_ns()
    result_dijkstra = dijkstra_with_heap(G, start_node)
    end_time = time.perf_counter_ns()
    time_dijkstra = (end_time - start_time) / 1_000_000  # 나노초를 밀리초로 변환
    dijkstra_path_length = result_dijkstra[target_node]

    # A* 알고리즘 테스트
    start_time = time.perf_counter_ns()
    result_astar = astar_with_heap(G, coordinates, start_node, target_node)
    end_time = time.perf_counter_ns()
    time_astar = (end_time - start_time) / 1_000_000  # 나노초를 밀리초로 변환
    astar_path_length = result_astar[target_node]
    
    return {
        'nodes': n_nodes,
        'edges': G.number_of_edges(),
        'time_astar': time_astar,
        'time_dijkstra': time_dijkstra,
        'path_length_astar': astar_path_length,
        'path_length_dijkstra': dijkstra_path_length
    }

# 다양한 크기의 그래프에 대해 테스트 실행
test_cases = [
    (2000, 0.1),
    (5000, 0.1),
    (10000, 0.05),
    (20000, 0.05)
]

# 메인 실행 코드
for n_nodes, density in test_cases:
    result = run_comparison_test(n_nodes, density)
    print(f"\nTest with {result['nodes']} nodes and {result['edges']} edges:")
    print(f"Time with A*: {result['time_astar']:.4f} miliseconds")
    print(f"Time with Dijkstra: {result['time_dijkstra']:.4f} miliseconds")
    print(f"Time Speedup: {result['time_dijkstra']/result['time_astar']:.2f}x")
    print(f"A* Path Length: {result['path_length_astar']}")
    print(f"Dijkstra Path Length: {result['path_length_dijkstra']}")
    path_ratio = result['path_length_astar'] / result['path_length_dijkstra']
    print(f"Path Length Ratio (A*/Dijkstra): {path_ratio:.2f}x")
