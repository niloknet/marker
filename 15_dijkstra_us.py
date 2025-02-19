import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

weighted_adjacency_matrix = np.array([
    [ 0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
      1.38705624,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        , 16.18166969,  3.37551848,  0.        ,  0.        ,
      0.        ,  0.        ,  9.18249476,  0.        ,  0.        ],
    [ 0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        ,  1.7199689 ,  0.        ,  5.59394852,
      0.        ,  0.        ,  0.        ,  0.        ,  3.75719377,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ],
    [ 0.        ,  0.        ,  0.        , 14.37892639,  0.        ,
      0.        ,  0.        ,  0.        , 12.91892519,  0.        ,
     35.17254886,  0.        ,  0.        ,  0.        ,  0.        ,
     17.49227378,  2.57214716,  4.6063288 ,  0.        ,  0.        ],
    [ 0.        ,  0.        , 14.37892639,  0.        ,  0.        ,
      0.        ,  3.14400573,  0.        ,  3.33698067,  0.        ,
      0.        , 15.69597671,  0.        , 20.48284926,  0.        ,
      0.        , 13.60156553,  0.        , 14.04326828,  0.        ],
    [ 0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        , 14.16269102,  5.1395387 ,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  4.09854438,
      9.47416155,  0.        ,  0.        ,  0.        ,  0.        ],
    [ 1.38705624,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        ,  2.14892764,  0.        ,
      0.        ,  0.        ,  8.23128429,  0.        ,  0.        ],
    [ 0.        ,  0.        ,  0.        ,  3.14400573, 14.16269102,
      0.        ,  0.        ,  0.        ,  3.75754015,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
     12.18951394,  0.        ,  0.        ,  0.        ,  0.        ],
    [ 0.        ,  1.7199689 ,  0.        ,  0.        ,  5.1395387 ,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  4.00232432,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ],
    [ 0.        ,  0.        , 12.91892519,  3.33698067,  0.        ,
      0.        ,  3.75754015,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
     10.75214481,  0.        ,  0.        ,  0.        ,  0.        ],
    [ 0.        ,  5.59394852,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  7.45482562,
      0.        ,  0.        ,  0.        ,  0.        ,  7.7532606 ],
    [ 0.        ,  0.        , 35.17254886,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
     19.0429686 ,  0.        ,  0.        ,  0.        ,  2.11121411],
    [16.18166969,  0.        ,  0.        , 15.69597671,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        , 13.50762677,  0.        ,
      0.        ,  0.        ,  0.        ,  3.02044252,  0.        ],
    [ 3.37551848,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        , 11.98603508,  0.        ,  0.        ],
    [ 0.        ,  0.        ,  0.        , 20.48284926,  0.        ,
      2.14892764,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        , 13.50762677,  0.        ,  0.        ,  0.        ,
      0.        ,  9.16367901,  6.92200672, 11.23072117,  0.        ],
    [ 0.        ,  3.75719377,  0.        ,  0.        ,  4.09854438,
      0.        ,  0.        ,  4.00232432,  0.        ,  7.45482562,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
     10.75858267,  0.        ,  0.        ,  0.        , 12.01264688],
    [ 0.        ,  0.        , 17.49227378,  0.        ,  9.47416155,
      0.        , 12.18951394,  0.        , 10.75214481,  0.        ,
     19.0429686 ,  0.        ,  0.        ,  0.        , 10.75858267,
      0.        ,  0.        ,  0.        ,  0.        , 18.60777397],
    [ 0.        ,  0.        ,  2.57214716, 13.60156553,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        ,  9.16367901,  0.        ,
      0.        ,  0.        ,  4.03233654,  0.        ,  0.        ],
    [ 9.18249476,  0.        ,  4.6063288 ,  0.        ,  0.        ,
      8.23128429,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        , 11.98603508,  6.92200672,  0.        ,
      0.        ,  4.03233654,  0.        ,  0.        ,  0.        ],
    [ 0.        ,  0.        ,  0.        , 14.04326828,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  3.02044252,  0.        , 11.23072117,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  0.        ],
    [ 0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
      0.        ,  0.        ,  0.        ,  0.        ,  7.7532606 ,
      2.11121411,  0.        ,  0.        ,  0.        , 12.01264688,
     18.60777397,  0.        ,  0.        ,  0.        ,  0.        ]
])

city_names = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
              'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Francisco',
              'Seattle', 'Miami', 'Boston', 'Washington DC', 'Las Vegas',
              'Denver', 'Indianapolis', 'Detroit', 'Orlando', 'Portland']

# 도시 좌표 정의
cities = np.array([
    [-74.006, 40.714],  # New York
    [-118.243, 34.052],  # Los Angeles
    [-87.629, 41.878],  # Chicago
    [-95.369, 29.760],  # Houston
    [-112.074, 33.448],  # Phoenix
    [-75.165, 39.952],  # Philadelphia
    [-98.495, 29.424],  # San Antonio
    [-117.161, 32.715],  # San Diego
    [-96.797, 32.776],  # Dallas
    [-122.419, 37.774],  # San Francisco
    [-122.332, 47.606],  # Seattle
    [-80.191, 25.761],  # Miami
    [-71.059, 42.360],  # Boston
    [-77.036, 38.895],  # Washington DC
    [-115.139, 36.169],  # Las Vegas
    [-104.990, 39.739],  # Denver
    [-86.158, 39.768],  # Indianapolis
    [-83.045, 42.331],  # Detroit
    [-81.379, 28.538],  # Orlando
    [-122.676, 45.523]   # Portland
])

pos = {}
for i, name in enumerate(city_names):
    pos[name] = cities[i]

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def visualize_dijkstra_step(G, pos, distances, current_node, path, step, current_cost):
    plt.clf()
    
    # 기본 노드와 엣지 그리기
    nx.draw_networkx_nodes(G, pos=pos, node_color='lightblue', node_size=700)
    nx.draw_networkx_edges(G, pos=pos, edge_color='gray')
    
    # 현재까지의 경로 강조
    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos=pos, edgelist=path_edges, edge_color='blue', width=2)
    
    # 현재 노드 강조
    nx.draw_networkx_nodes(G, pos=pos, nodelist=[current_node], node_color='red', node_size=700)
    
    # 레이블 표시
    labels = {node: f"{node}\n({distances[node]:.1f})" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=8)
    
    # 엣지 가중치 표시
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f'{v:.1f}' for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, font_size=7)
    
    plt.title(f"Step {step}: Current Node = {current_node}, Current Cost = {current_cost:.1f}")
    plt.axis('off')
    plt.pause(2)
    
def dijkstra_visualization(G, start, end, pos):
    distances = {node: float('infinity') for node in G.nodes()}
    distances[start] = 0
    previous = {node: None for node in G.nodes()}
    unvisited = set(G.nodes())
    
    all_steps = []
    
    while unvisited:
        current = min(unvisited, key=lambda x: distances[x])
        current_cost = distances[current]
        
        if current == end:
            break
            
        current_path = []
        temp = current
        while temp is not None:
            current_path.insert(0, temp)
            temp = previous[temp]
        
        step_info = {
            'current_node': current,
            'distances': distances.copy(),
            'previous': previous.copy(),
            'current_path': current_path,
            'current_cost': current_cost,
            'is_final': False
        }
        all_steps.append(step_info)
        
        for neighbor in G.neighbors(current):
            if neighbor in unvisited:
                new_distance = distances[current] + G[current][neighbor]['weight']
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
        
        unvisited.remove(current)
    
    # 최종 경로 재구성
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous[current]
        
    # 최종 단계 추가
    final_step = {
        'current_node': end,
        'distances': distances,
        'previous': previous,
        'current_path': path,
        'current_cost': distances[end],
        'is_final': True
    }
    all_steps.append(final_step)
    
    fig, ax = plt.subplots(figsize=(15, 10))
    
    def update(step):
        ax.clear()
        
        if step['is_final']:
            # 최종 경로일 때 노드와 엣지를 노란색으로 강조
            node_colors = ["yellow" if node in step['current_path'] else "lightblue" 
                         for node in G.nodes()]
            edge_colors = ["yellow" if (u in step['current_path'] and v in step['current_path'] and 
                          abs(step['current_path'].index(u) - step['current_path'].index(v)) == 1)
                          else "gray" for u, v in G.edges()]
            nx.draw_networkx_nodes(G, pos=pos, node_color=node_colors, node_size=700)
            nx.draw_networkx_edges(G, pos=pos, edge_color=edge_colors)
        else:
            # 진행 중인 상태
            nx.draw_networkx_nodes(G, pos=pos, node_color='lightblue', node_size=700)
            nx.draw_networkx_edges(G, pos=pos, edge_color='gray')
            
            if step['current_path']:
                path_edges = list(zip(step['current_path'][:-1], step['current_path'][1:]))
                nx.draw_networkx_edges(G, pos=pos, edgelist=path_edges, edge_color='blue', width=2)
            
            nx.draw_networkx_nodes(G, pos=pos, nodelist=[step['current_node']], 
                                 node_color='red', node_size=700)
        
        # 레이블 표시
        labels = {node: f"{node}\n({step['distances'][node]:.1f})" for node in G.nodes()}
        nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=8)
        
        # 엣지 가중치 표시
        edge_labels = nx.get_edge_attributes(G, 'weight')
        edge_labels = {k: f'{v:.1f}' for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, font_size=7)
        
        if step['is_final']:
            title = f"Shortest Path from {start} to {end}\nTotal Distance: {step['current_cost']:.1f}"
        else:
            title = f"Step: Current Node = {step['current_node']}, Current Cost = {step['current_cost']:.1f}"
        
        ax.set_title(title)
        ax.axis('off')
    
    current_frame = [0]
    
    def on_key(event):
        if event.key == 'right' and current_frame[0] < len(all_steps) - 1:
            current_frame[0] += 1
        elif event.key == 'left' and current_frame[0] > 0:
            current_frame[0] -= 1
        update(all_steps[current_frame[0]])
        plt.draw()
    
    fig.canvas.mpl_connect('key_press_event', on_key)
    update(all_steps[0])
    plt.show()
    
    return path, distances[end]

# 그래프 생성 및 실행 코드는 그대로 유지
G = nx.from_numpy_array(weighted_adjacency_matrix)
mapping = {i: name for i, name in enumerate(city_names)}
G = nx.relabel_nodes(G, mapping)

# 다익스트라 알고리즘 실행
shortest_path, total_distance = dijkstra_visualization(G, 'San Francisco', 'New York', pos)
