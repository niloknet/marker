import networkx as nx
import heapq
import random
import time

# 힙을 사용하지 않는 다익스트라 알고리즘
def dijkstra_without_heap(graph, start_node):
    shortest_paths = {node: float('inf') for node in graph.nodes}
    shortest_paths[start_node] = 0
    unvisited_nodes = set(graph.nodes)
    
    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda node: shortest_paths[node])
        
        if shortest_paths[current_node] == float('inf'):
            break
            
        for neighbor in graph.neighbors(current_node):
            distance = shortest_paths[current_node] + graph[current_node][neighbor]['weight']
            if distance < shortest_paths[neighbor]:
                shortest_paths[neighbor] = distance
                
        unvisited_nodes.remove(current_node)
    
    return shortest_paths

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

# 랜덤 그래프 생성 함수
def create_random_graph(n_nodes, edge_density):
    G = nx.DiGraph()
    
    # 노드 추가
    nodes = list(range(n_nodes))
    G.add_nodes_from(nodes)
    
    # 엣지 추가
    for i in nodes:
        for j in nodes:
            if i != j and random.random() < edge_density:
                G.add_edge(i, j, weight=random.randint(1, 100))
    
    return G

# 테스트 실행
def run_comparison_test(n_nodes, edge_density):
    # 랜덤 그래프 생성
    G = create_random_graph(n_nodes, edge_density)
    start_node = 0
    
    # 힙을 사용하지 않는 버전 테스트
    start_time = time.time()
    result1 = dijkstra_without_heap(G, start_node)
    time1 = time.time() - start_time
    
    # 힙을 사용하는 버전 테스트
    start_time = time.time()
    result2 = dijkstra_with_heap(G, start_node)
    time2 = time.time() - start_time
    
    return {
        'nodes': n_nodes,
        'edges': G.number_of_edges(),
        'time_without_heap': time1,
        'time_with_heap': time2
    }

# 다양한 크기의 그래프에 대해 테스트 실행
test_cases = [
    (500, 0.1),
    (1000, 0.1),
    (5000, 0.1),
    (10000, 0.1),
    (20000, 0.05),
    (5000, 0.01),
    (5000, 0.1),
    (5000, 0.6)
]

for n_nodes, density in test_cases:
    result = run_comparison_test(n_nodes, density)
    print(f"\nTest with {result['nodes']} nodes and {result['edges']} edges:")
    print(f"Time without heap: {result['time_without_heap']:.4f} seconds")
    print(f"Time with heap: {result['time_with_heap']:.4f} seconds")
    print(f"Speedup: {result['time_without_heap']/result['time_with_heap']:.2f}x")
