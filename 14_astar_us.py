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

def heuristic(node1, node2, pos):
    # 두 도시 간의 직선 거리를 계산
    x1, y1 = pos[node1]
    x2, y2 = pos[node2]
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)**3

def astar_visualization(G, start, end, pos):
    g_score = {node: float('infinity') for node in G.nodes()}
    g_score[start] = 0
    
    f_score = {node: float('infinity') for node in G.nodes()}
    f_score[start] = heuristic(start, end, pos)
    
    previous = {node: None for node in G.nodes()}
    open_list = {start}
    closed_list = set()
    all_steps = []

    # 그래프 크기와 여백 조정
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)
    plt.margins(0.2)  # 여백 추가
    
    # tight_layout 설정
    plt.tight_layout()

    while open_list:
        current = min(open_list, key=lambda x: f_score[x])
        current_cost = g_score[current]
        
        current_path = []
        temp = current
        while temp is not None:
            current_path.insert(0, temp)
            temp = previous[temp]
            
        step_info = {
            'current_node': current,
            'g_score': g_score.copy(),
            'f_score': f_score.copy(),
            'open_list': open_list.copy(),
            'closed_list': closed_list.copy(),
            'path': current_path.copy(),
            'is_final': current == end
        }
        all_steps.append(step_info)
        
        if current == end:
            break
            
        open_list.remove(current)
        closed_list.add(current)
        
        for neighbor in G.neighbors(current):
            if neighbor in closed_list:
                continue
                
            tentative_g_score = g_score[current] + G[current][neighbor]['weight']
            
            if tentative_g_score < g_score[neighbor]:
                previous[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end, pos)
                open_list.add(neighbor)
    
    def update(frame):
        ax.clear()
        step = all_steps[frame]

        for text in fig.texts:
          text.remove()
          
        # 그래프 영역 최대화
        ax.set_position([0.1, 0.1, 0.8, 0.8])  # [left, bottom, width, height]
        
        if step['is_final']:
            node_colors = ["yellow" if node in step['path'] else "lightblue" 
                         for node in G.nodes()]
            edge_colors = ["yellow" if (u in step['path'] and v in step['path'] and 
                          abs(step['path'].index(u) - step['path'].index(v)) == 1)
                          else "gray" for u, v in G.edges()]
            nx.draw(G, pos=pos, node_color=node_colors, edge_color=edge_colors,
                   node_size=700, ax=ax)
        else:
            nx.draw_networkx_nodes(G, pos=pos, node_color='lightblue', 
                                 node_size=700, ax=ax)
            nx.draw_networkx_edges(G, pos=pos, edge_color='gray', ax=ax)
            
            if step['path']:
                path_edges = list(zip(step['path'][:-1], step['path'][1:]))
                nx.draw_networkx_edges(G, pos=pos, edgelist=path_edges, 
                                     edge_color='blue', width=2, ax=ax)
            
            nx.draw_networkx_nodes(G, pos=pos, nodelist=[step['current_node']], 
                                 node_color='red', node_size=700, ax=ax)
        
        labels = {node: f"{node}" for node in G.nodes()}
        nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=10)
        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        edge_labels = {k: f'{v:.1f}' for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, 
                                   font_size=8)
        
        title = f"Step {frame + 1}: Current Node = {step['current_node']}"
        if step['is_final']:
            title = f"Final Path | Total Cost: {step['g_score'][end]:.1f}"
        ax.set_title(title)
        ax.axis('off')
        
        # 상태 정보 표시
        current_node = step['current_node']
        open_list_with_f = [f"{node}(f={step['f_score'][node]:.1f})" for node in step['open_list']]
        status_text = [
            f"Current Node: {current_node}",
            f"g({current_node}) = {step['g_score'][current_node]:.1f}, h({current_node}) = {step['f_score'][current_node] - step['g_score'][current_node]:.1f}",
            f"Open List with f(n): {sorted(open_list_with_f, key=lambda x: float(x.split('=')[1][:-1]))}",
            f"Closed List: {step['closed_list']}",
            f"Current Path: {' -> '.join(step['path'])}"
        ]
        
        # 상태 정보를 그래프 아래에 표시
        plt.figtext(0.1, 0.02, '\n'.join(status_text), fontsize=10,
                  bbox=dict(facecolor='white', alpha=0.8))
    
    current_frame = [0]
    
    def on_key(event):
        if event.key == 'right' and current_frame[0] < len(all_steps) - 1:
            current_frame[0] += 1
        elif event.key == 'left' and current_frame[0] > 0:
            current_frame[0] -= 1
        update(current_frame[0])
        plt.draw()
    
    fig.canvas.mpl_connect('key_press_event', on_key)
    update(0)
    plt.show()
    
    return step_info['path'], step_info['g_score'][end]

# 그래프 생성 및 실행
G = nx.from_numpy_array(weighted_adjacency_matrix)
mapping = {i: name for i, name in enumerate(city_names)}
G = nx.relabel_nodes(G, mapping)

# A* 알고리즘 실행
shortest_path, total_distance = astar_visualization(G, 'San Francisco', 'New York', pos)

