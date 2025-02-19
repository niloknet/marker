import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
import matplotlib.pyplot as plt
import time
from itertools import permutations
import os
os.environ['LOKY_MAX_CPU_COUNT'] = str(4)

# 임의의 도시 좌표 생성
np.random.seed(int(time.time()))
n_cities = 20
cities = np.random.rand(n_cities, 2) * 100

# Nearest Neighbor 알고리즘 구현
def nearest_neighbor(cities):
    n = len(cities)
    distances = pairwise_distances(cities)
    unvisited = set(range(1, n))
    path = [0]  # 첫 번째 도시에서 시작
    current = 0
    
    while unvisited:
        next_city = min(unvisited, key=lambda x: distances[current][x])
        path.append(next_city)
        unvisited.remove(next_city)
        current = next_city
        
    return path

# 2-opt 알고리즘 구현
def calculate_total_distance(path, distances):
    total_distance = 0
    for i in range(len(path)):
        total_distance += distances[path[i]][path[(i + 1) % len(path)]]
    return total_distance

def two_opt_swap(path, i, j):
    new_path = path.copy()
    new_path[i:j] = path[j-1:i-1:-1]
    return new_path

def two_opt(cities):
    distances = pairwise_distances(cities)
    current_path = list(range(len(cities)))
    
    improvement = True
    while improvement:
        improvement = False
        best_distance = calculate_total_distance(current_path, distances)
        
        for i in range(1, len(cities) - 1):
            for j in range(i + 1, len(cities)):
                new_path = two_opt_swap(current_path, i, j)
                new_distance = calculate_total_distance(new_path, distances)
                
                if new_distance < best_distance:
                    current_path = new_path
                    best_distance = new_distance
                    improvement = True
                    break
            if improvement:
                break
                
    return current_path

# 클러스터링 기반 해법
def cluster_cities(cities, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(cities)
    centers = kmeans.cluster_centers_
    return clusters, centers

def optimize_cluster_path(cities, cluster_id, cluster_indices):
    cluster_cities = cities[cluster_indices]
    n = len(cluster_cities)
    distances = pairwise_distances(cluster_cities)
    
    current_city = 0
    path = [current_city]
    unvisited = set(range(1, n))
    
    while unvisited:
        next_city = min(unvisited, 
                       key=lambda x: distances[current_city][x])
        path.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city
        
    return cluster_indices[path]

def optimize_cluster_path_bf_limited(cities, cluster_id, cluster_indices):
    if len(cluster_indices) > 10:  # 도시가 10개 초과면 NN 알고리즘 사용
        return optimize_cluster_path(cities, cluster_id, cluster_indices)
    
    cluster_cities = cities[cluster_indices]
    n = len(cluster_cities)
    distances = pairwise_distances(cluster_cities)
    
    min_distance = float('inf')
    best_path = None
    
    for path in permutations(range(n)):
        current_distance = sum(distances[path[i]][path[(i + 1) % n]] 
                             for i in range(n))
        if current_distance < min_distance:
            min_distance = current_distance
            best_path = path
    
    return cluster_indices[list(best_path)]

def optimize_cluster_connections(cities, clusters, n_clusters):
    # 각 클러스터의 경로 계산
    cluster_paths = []
    for i in range(n_clusters):
        cluster_indices = np.where(clusters == i)[0]
        if len(cluster_indices) > 0:
            cluster_path = optimize_cluster_path_bf_limited(cities, i, cluster_indices)
            cluster_paths.append(cluster_path)
    
    # 클러스터 순서 최적화
    best_order = None
    min_total_distance = float('inf')
    distances = pairwise_distances(cities)
    
    # 클러스터 순서의 모든 순열 시도
    for cluster_order in permutations(range(len(cluster_paths))):
        total_distance = 0
        current_path = []
        
        # 주어진 순서대로 클러스터 연결
        for i in range(len(cluster_order)):
            current_cluster = cluster_paths[cluster_order[i]]
            
            if current_path:  # 이전 클러스터와 현재 클러스터 사이의 거리 추가
                total_distance += distances[current_path[-1]][current_cluster[0]]
            
            # 클러스터 내부 경로의 거리 추가
            for j in range(len(current_cluster)-1):
                total_distance += distances[current_cluster[j]][current_cluster[j+1]]
            
            current_path.extend(current_cluster)
        
        # 마지막 도시에서 첫 도시로의 거리 추가
        total_distance += distances[current_path[-1]][current_path[0]]
        
        if total_distance < min_total_distance:
            min_total_distance = total_distance
            best_order = current_path
    
    return best_order

def plot_solutions(cities, cluster_path, two_opt_path, nn_path):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # 클러스터링 결과 플롯
    ax1.scatter(cities[:, 0], cities[:, 1], c='red', s=100)
    for i in range(len(cluster_path)):
        start = cities[cluster_path[i]]
        end = cities[cluster_path[(i + 1) % len(cluster_path)]]
        ax1.plot([start[0], end[0]], [start[1], end[1]], 'b-')
    ax1.set_title('Clustering Method')

    # 2-opt 결과 플롯
    ax2.scatter(cities[:, 0], cities[:, 1], c='red', s=100)
    for i in range(len(two_opt_path)):
        start = cities[two_opt_path[i]]
        end = cities[two_opt_path[(i + 1) % len(two_opt_path)]]
        ax2.plot([start[0], end[0]], [start[1], end[1]], 'g-')
    ax2.set_title('2-opt Method')
    
    # NN 결과 플롯
    ax3.scatter(cities[:, 0], cities[:, 1], c='red', s=100)
    for i in range(len(nn_path)):
        start = cities[nn_path[i]]
        end = cities[nn_path[(i + 1) % len(nn_path)]]
        ax3.plot([start[0], end[0]], [start[1], end[1]], 'y-')
    ax3.set_title('Nearest Neighbor Method')

    plt.show()

def plot_combined_solutions(cities, cluster_path, two_opt_path):
    plt.figure(figsize=(10, 10))
    plt.scatter(cities[:, 0], cities[:, 1], c='red', s=100, label='Cities')
    
    # 클러스터링 경로 그리기
    for i in range(len(cluster_path)):
        start = cities[cluster_path[i]]
        end = cities[cluster_path[(i + 1) % len(cluster_path)]]
        plt.plot([start[0], end[0]], [start[1], end[1]], 'b-', alpha=0.5, label='Clustering' if i == 0 else "")
    
    # 2-opt 경로 그리기
    for i in range(len(two_opt_path)):
        start = cities[two_opt_path[i]]
        end = cities[two_opt_path[(i + 1) % len(two_opt_path)]]
        plt.plot([start[0], end[0]], [start[1], end[1]], 'g-', alpha=0.5, label='2-opt' if i == 0 else "")
    
    plt.legend()
    plt.show()

# 두 방법으로 해법 찾기
# 1. 클러스터링 기반 해법
clusters, centers = cluster_cities(cities)
cluster_final_path = optimized_path = optimize_cluster_connections(cities, clusters, 5)

# 2. 2-opt 해법
two_opt_final_path = two_opt(cities)

# 3. Nearest Neighbor 해법
nn_path = nearest_neighbor(cities)

# 결과 비교를 위한 총 거리 계산
distances = pairwise_distances(cities)
cluster_distance = calculate_total_distance(cluster_final_path, distances)
two_opt_distance = calculate_total_distance(two_opt_final_path, distances)
nn_distance = calculate_total_distance(nn_path, distances)

clusters, centers = cluster_cities(cities, n_clusters=5)
optimized_path = optimize_cluster_connections(cities, clusters, 5)


print(f"클러스터링 기반 해법의 총 거리: {cluster_distance:.2f}")
print(f"2-opt 해법의 총 거리: {two_opt_distance:.2f}")
print(f"Nearest Neighbor 해법의 총 거리: {nn_distance:.2f}")

# 시각화 함수 호출
plot_solutions(cities, cluster_final_path, two_opt_final_path, nn_path)
