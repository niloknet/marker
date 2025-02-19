import random
import heapq
import math
import time

import numpy as np
import pandas as pd
from tabulate import tabulate

# 그리드 초기화
grid_size = 800
grid = np.zeros((grid_size, grid_size))

# 여러 개의 가중치 경로를 생성하는 함수
def create_weighted_paths(grid, num_paths=10, max_weight=10):
    for _ in range(num_paths):
        start = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
        end = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
        weight = random.randint(1, max_weight)
        # 간단한 경로 생성 (수평 및 수직)
        if start[0] == end[0]:  # 같은 행
            grid[start[0], min(start[1], end[1]):max(start[1], end[1])+1] = weight
        elif start[1] == end[1]:  # 같은 열
            grid[min(start[0], end[0]):max(start[0], end[0])+1, start[1]] = weight
        else:  # 대각선 경로
            for i in range(min(abs(start[0] - end[0]), abs(start[1] - end[1])) + 1):
                if min(start[0], end[0]) + i < grid_size and min(start[1], end[1]) + i < grid_size:
                    grid[min(start[0], end[0]) + i, min(start[1], end[1]) + i] = weight

# 병목 현상을 만들기 위해 장애물을 추가하는 함수
def add_obstacles(grid, num_obstacles=1000):
    for _ in range(num_obstacles):
        x = random.randint(0, grid_size-1)
        y = random.randint(0, grid_size-1)
        grid[x, y] = -1  # 장애물을 -1로 표시

# 긴 대각선 경로를 생성하는 함수
def create_long_diagonal_paths(grid, num_paths=10, max_weight=10):
    for _ in range(num_paths):
        start_x = random.randint(0, grid_size-1)
        start_y = random.randint(0, grid_size-1)
        end_x = random.randint(0, grid_size-1)
        end_y = random.randint(0, grid_size-1)
        weight = random.randint(1, max_weight)
        # 긴 대각선 경로 생성
        for i in range(min(abs(start_x - end_x), abs(start_y - end_y)) + 1):
            if start_x + i < grid_size and start_y + i < grid_size:
                grid[start_x + i, start_y + i] = weight

# 지형 비용을 할당하는 함수
def assign_terrain_costs(grid, terrain_types=['평지', '언덕', '산악'], max_weight=1):
    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x, y] != -1:  # 장애물이 아닌 경우
                terrain = random.choice(terrain_types)
                if terrain == '평지':
                    grid[x, y] = random.randint(1, max_weight // 2)
                elif terrain == '언덕':
                    grid[x, y] = random.randint(max_weight // 2, max_weight)
                elif terrain == '산악':
                    grid[x, y] = random.randint(max_weight, max_weight * 2)

# 그리드 생성
create_weighted_paths(grid, num_paths=5, max_weight=3)
add_obstacles(grid, num_obstacles=1000)
create_long_diagonal_paths(grid, num_paths=5)
assign_terrain_costs(grid, terrain_types=['평지', '언덕', '산악'], max_weight=5)

def astar(grid, start, goal, heuristic_func):
    def get_neighbors(x, y):
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != -1:
                neighbors.append((nx, ny))
        return neighbors

    def get_cost(current, neighbor):
        return grid[neighbor[0]][neighbor[1]]

    def reconstruct_path(came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: abs(heuristic_func(start, goal))}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(*current):
            tentative_g_score = g_score[current] + get_cost(current, neighbor)

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + abs(heuristic_func(neighbor, goal))
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # 경로를 찾지 못함

# 휴리스틱 함수 예시
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def chebyshev_distance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def zero_heuristic(a, b):
    return 0  # A*를 다익스트라 알고리즘처럼 동작하게 함

def weighted_manhattan(a, b, weight=1.2):
    return weight * manhattan_distance(a, b)

def your_heuristic_function(a, b):
    # ########## 여기에 자신만의 휴리스틱을 구현하세요 #################
    # a와 b는 튜플 (x, y) 형태의 좌표입니다.
    return int(time.time()*1000) % 10 # 0에서 9사이 값을 랜덤하게 반환하는 휴리스틱 함수
    # ###############################################################

def measure_execution_times(grid, start, goal):
    results = {}
    
    # 휴리스틱 함수를 사용한 테스트 케이스 정의
    test_cases = {
        'zero (dijkstra)': zero_heuristic,
        'manhattan': manhattan_distance,
        'weighted manhattan': lambda a, b: manhattan_distance(a, b) * 1.2,
        'euclidean': euclidean_distance,
        # 'chebyshev': chebyshev_distance,
        'your_heuristic': your_heuristic_function
    }
    
    for name, heuristic in test_cases.items():
        start_time = time.time()
        path = astar(grid, start, goal, heuristic)
        execution_time = (time.time() - start_time)
        results[name] = {
            'time': execution_time,
            'path_length': len(path) if path else 0
        }
    
    return results

# 사용 예시
start = (0, 0)
goal = (grid_size-1, grid_size-1)

# 비교 테이블 생성 및 실행
results = measure_execution_times(grid, start, goal)

# DataFrame 생성 (results 딕셔너리로부터)
df = pd.DataFrame.from_dict(results, orient='index')
df = df.rename(columns={'time': 'duration (s)', 'path_length': 'path length'})
df = df.reset_index().rename(columns={'index': 'algorithm'})

# tabulate로 출력
print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
