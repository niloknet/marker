import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time

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

import numpy as np
from itertools import permutations
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def create_distance_matrix(cities):
    n = len(cities)
    matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = haversine_distance(
                    cities[i][1], cities[i][0],  # lat, lon for city i
                    cities[j][1], cities[j][0]   # lat, lon for city j
                )
    return matrix

def nearest_neighbor_tsp(distance_matrix, city_names):
    n = len(city_names)
    unvisited = set(range(n))
    current = 0
    path = [current]
    total_distance = 0
    unvisited.remove(current)
    
    while unvisited:
        next_city = min(unvisited, key=lambda x: distance_matrix[current][x])
        total_distance += distance_matrix[current][next_city]
        current = next_city
        path.append(current)
        unvisited.remove(current)
    
    # Return to start
    total_distance += distance_matrix[path[-1]][path[0]]
    path.append(path[0])
    
    return [city_names[i] for i in path], total_distance

from itertools import permutations

def brute_force_tsp(distance_matrix, city_names):
    n = len(city_names)
    min_distance = float('inf')
    best_path = None
    
    for perm in permutations(range(n)):
        distance = 0
        valid_path = True
        
        for i in range(n-1):
            if distance_matrix[perm[i]][perm[i+1]] > 0:
                distance += distance_matrix[perm[i]][perm[i+1]]
            else:
                valid_path = False
                break
                
        if valid_path and distance_matrix[perm[-1]][perm[0]] > 0:
            distance += distance_matrix[perm[-1]][perm[0]]
            if distance < min_distance:
                min_distance = distance
                best_path = perm
    
    if best_path is None:
        return None, float('inf')
    
    return [city_names[i] for i in best_path] + [city_names[best_path[0]]], min_distance

def two_opt_swap(route, i, j):
    return route[:i] + route[i:j+1][::-1] + route[j+1:]

def calculate_total_distance(route, distance_matrix):
    return sum(distance_matrix[route[i]][route[i+1]] for i in range(len(route)-1))

def two_opt_tsp(distance_matrix, city_names):
    n = len(city_names)
    current_route_names, _ = nearest_neighbor_tsp(distance_matrix, city_names)
    current_route = [city_names.index(city) for city in current_route_names[:-1]]
    
    improvement = True
    while improvement:
        improvement = False
        best_distance = calculate_total_distance(current_route + [current_route[0]], distance_matrix)
        
        for i in range(1, n-2):
            for j in range(i+1, n):
                new_route = two_opt_swap(current_route, i, j)
                new_distance = calculate_total_distance(new_route + [new_route[0]], distance_matrix)
                
                if new_distance < best_distance:
                    current_route = new_route
                    best_distance = new_distance
                    improvement = True
                    break
            if improvement:
                break
    
    return [city_names[i] for i in current_route + [current_route[0]]], best_distance

# 실행 예시
distance_matrix = create_distance_matrix(cities)

small_cities = city_names[:8]
small_matrix = distance_matrix[:8, :8]

# Nearest Neighbor 실행
start_time = time.perf_counter_ns()
nn_path, nn_distance = nearest_neighbor_tsp(small_matrix, small_cities)
end_time = time.perf_counter_ns()
print(f"Nearest Neighbor Distance for 8 cities: {nn_distance:.2f} km")
print("Path:", ' -> '.join(nn_path))
print(f"Time taken: {(end_time - start_time)/1_000_000:.2f} miliseconds")

start_time = time.perf_counter_ns()
nn_path, nn_distance = nearest_neighbor_tsp(distance_matrix, city_names)
end_time = time.perf_counter_ns()
print(f"\nNearest Neighbor Distance for 20 cities: {nn_distance:.2f} km")
print("Path:", ' -> '.join(nn_path))
print(f"Time taken: {(end_time - start_time)/1_000_000:.2f} miliseconds")

# 2-opt 실행
start_time = time.perf_counter_ns()
two_opt_path, two_opt_distance = two_opt_tsp(small_matrix, small_cities)
end_time = time.perf_counter_ns()
print(f"\n2-opt Distance for 8 cities: {two_opt_distance:.2f} km")
print("Path:", ' -> '.join(two_opt_path))
print(f"Time taken: {(end_time - start_time)/1_000_000:.2f} miliseconds")

start_time = time.perf_counter_ns()
two_opt_path, two_opt_distance = two_opt_tsp(distance_matrix, city_names)
end_time = time.perf_counter_ns()
print(f"\n2-opt Distance for 20 cities: {two_opt_distance:.2f} km")
print("Path:", ' -> '.join(two_opt_path))
print(f"Time taken: {(end_time - start_time)/1_000_000:.2f} miliseconds")

for n in range(8, 12):
    print(f"\nTesting for {n} cities...")
    small_cities = city_names[:n]
    small_matrix = distance_matrix[:n, :n]
    
    start_time = time.perf_counter_ns()
    bf_path, bf_distance = brute_force_tsp(small_matrix, small_cities)
    end_time = time.perf_counter_ns()
    
    print(f"Brute Force Distance for {n} cities: {bf_distance:.2f} km")
    print("Path:", ' -> '.join(bf_path))
    print(f"Time taken: {(end_time - start_time)/1_000_000:.2f} miliseconds")
