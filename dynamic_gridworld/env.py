import gym
from gym import spaces
import numpy as np
import pygame
import time
import random

class DynamicGridWorldEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, size=5, render_mode="human", delay=0.5, initial_position="corner"):
        super().__init__()
        self.size = size  # Grid size
        self.goal_pos = np.array([size - 1, size - 1])  # Goal at bottom-right corner
        self.window_size = 512  # Window size in pixels
        self.render_mode = render_mode
        self.render_enabled = render_mode == "human"
        self.delay = delay if self.render_enabled else 0.0  # Delay in seconds between actions
        self.initial_position = initial_position  # Initial position of the agent ("center" or "corner")
        self.reward_goal = 100  # Reward for reaching the goal
        self.reward_step = -1  # Penalty for each step to encourage shorter paths
        self.action_space = spaces.Discrete(4)  # Up, Down, Left, Right
        # Define observation space
        self.observation_space = spaces.Dict({
            "agent": spaces.MultiDiscrete([size, size]),
            "objects": spaces.MultiBinary((size, size)),
            "horizontal_walls": spaces.MultiBinary((size + 1, size)),  # Horizontal walls
            "vertical_walls": spaces.MultiBinary((size, size + 1))     # Vertical walls
        })

        self.reset()

    def reset(self):
        """Reset the environment and place the agent at the specified initial position."""
        if self.initial_position == "center":
            center = self.size // 2
            self.agent_pos = np.array([center, center])
        elif self.initial_position == "corner":
            self.agent_pos = np.array([0, 0])
        else:
            raise ValueError("Invalid initial_position. Choose 'center' or 'corner'.")

        # Initialize object grid and wall grids (empty by default)
        self.objects_grid = np.zeros((self.size, self.size), dtype=int)
        self.horizontal_walls = np.zeros((self.size + 1, self.size), dtype=int)
        self.vertical_walls = np.zeros((self.size, self.size + 1), dtype=int)

        # Render the empty environment
        self.render()
        time.sleep(self.delay)
        return self._get_obs()
    
    def step(self, action):
        """Perform an action (move) and return (obs, reward, done, info)."""
        prev_pos = self.agent_pos.copy()
        
        # Move agent based on action
        if action == 0:  # Up
            self.move('up')
        elif action == 1:  # Down
            self.move('down')
        elif action == 2:  # Left
            self.move('left')
        elif action == 3:  # Right
            self.move('right')

        # Calculate reward
        reward = self.reward_goal if np.array_equal(self.agent_pos, self.goal_pos) else self.reward_step
        
        # Check if goal is reached
        done = np.array_equal(self.agent_pos, self.goal_pos)

        return self._get_obs(), reward, done, {}


    def generate_random_walls(self, num_horizontal=0, num_vertical=0):
        """Randomly generate horizontal and vertical walls."""
        for _ in range(num_horizontal):
            x = random.randint(0, self.size)  # Between rows (0 to size)
            y = random.randint(0, self.size - 1)  # Within columns (0 to size-1)
            if not (x == 0 and y == 0):  # Avoid blocking the initial position of the agent
                self.horizontal_walls[x][y] = 1

        for _ in range(num_vertical):
            x = random.randint(0, self.size - 1)  # Within rows (0 to size-1)
            y = random.randint(0, self.size)  # Between columns (0 to size)
            if not (x == 0 and y == 0):  # Avoid blocking the initial position of the agent
                self.vertical_walls[x][y] = 1

    def _get_obs(self):
        return {
            "agent": self.agent_pos.copy(),
            "objects": self.objects_grid.copy(),
            "horizontal_walls": self.horizontal_walls.copy(),
            "vertical_walls": self.vertical_walls.copy()
        }
    
    def move(self, direction):
        """Move the agent in the specified direction."""
        x, y = self.agent_pos

        if direction == 'up' and x > 0 and not self.horizontal_walls[x][y]:
            self.agent_pos[0] -= 1
        elif direction == 'down' and x < self.size - 1 and not self.horizontal_walls[x + 1][y]:
            self.agent_pos[0] += 1
        elif direction == 'left' and y > 0 and not self.vertical_walls[x][y]:
            self.agent_pos[1] -= 1
        elif direction == 'right' and y < self.size - 1 and not self.vertical_walls[x][y + 1]:
            self.agent_pos[1] += 1

        self.render()
        time.sleep(self.delay)

    def move_up(self):
        """Shortcut to move up."""
        self.move('up')

    def move_down(self):
        """Shortcut to move down."""
        self.move('down')

    def move_left(self):
        """Shortcut to move left."""
        self.move('left')

    def move_right(self):
        """Shortcut to move right."""
        self.move('right')

    def place(self):
        self.objects_grid[tuple(self.agent_pos)] = 1
        self.render()
        time.sleep(self.delay)

    def pick_up(self):
        self.objects_grid[tuple(self.agent_pos)] = 0
        self.render()
        time.sleep(self.delay)

    def sense(self, direction):
        """
        Sense if there is a wall or a box in the given direction.
        Returns a dictionary with keys 'wall' and 'box' indicating the presence of each.
        """
        x, y = self.agent_pos

        if direction == 'up':
            # Check for a wall above the agent
            wall = self.horizontal_walls[x][y] if x > 0 else True  # Boundary is treated as a wall
            # Check for a box in the cell above the agent
            box = self.objects_grid[x - 1][y] if x > 0 else False
        elif direction == 'down':
            wall = self.horizontal_walls[x + 1][y] if x < self.size - 1 else True
            box = self.objects_grid[x + 1][y] if x < self.size - 1 else False
        elif direction == 'left':
            wall = self.vertical_walls[x][y] if y > 0 else True
            box = self.objects_grid[x][y - 1] if y > 0 else False
        elif direction == 'right':
            wall = self.vertical_walls[x][y + 1] if y < self.size - 1 else True
            box = self.objects_grid[x][y + 1] if y < self.size - 1 else False
        else:
            raise ValueError("Invalid direction. Choose from 'up', 'down', 'left', or 'right'.")

        return {"wall": bool(wall), "box": bool(box)}

    def sense_up(self):
        return self.sense('up')

    def sense_down(self):
        return self.sense('down')

    def sense_left(self):
        return self.sense('left')

    def sense_right(self):
        return self.sense('right')

    def sense_up_box(self):
        return self.sense('up')["box"]

    def sense_down_box(self):
        return self.sense('down')["box"]

    def sense_left_box(self):
        return self.sense('left')["box"]

    def sense_right_box(self):
        return self.sense('right')["box"]

    def sense_up_wall(self):
        return self.sense('up')["wall"]

    def sense_down_wall(self):
        return self.sense('down')["wall"]

    def sense_left_wall(self):
        return self.sense('left')["wall"]

    def sense_right_wall(self):
        return self.sense('right')["wall"]

    def sense_all(self):
        """Sense all directions for both boxes and walls."""
        return {
            "up": self.sense("up"),
            "down": self.sense("down"),
            "left": self.sense("left"),
            "right": self.sense("right")
        }

    def sense_all_box(self):
        """Sense all directions specifically for boxes."""
        return [
            self.sense_up_box(),
            self.sense_down_box(),
            self.sense_left_box(),
            self.sense_right_box()
        ]
    
    def render(self):
        """Render the gridworld environment."""
        if not self.render_enabled:
            return  # Skip rendering if disabled
        
        if not hasattr(self, "screen"):
            pygame.init()
            pygame.display.set_caption("Dynamic GridWorld")
            self.screen = pygame.display.set_mode((self.window_size, self.window_size))
            self.clock = pygame.time.Clock()

        cell_size = self.window_size // self.size

        # Clear screen
        self.screen.fill((255, 255, 255))

        # Draw grid lines and elements
        for x in range(self.size):
            for y in range(self.size):
                rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, width=1)

                # Draw objects as green squares
                if self.objects_grid[x][y] == 1:
                    pygame.draw.rect(
                        self.screen,
                        (0, 255, 0),
                        rect,
                    )

                # Draw agent as a blue circle
                if (x, y) == tuple(self.agent_pos):
                    pygame.draw.circle(
                        self.screen,
                        (0, 0, 255),
                        rect.center,
                        cell_size // 3,
                    )

        # Draw horizontal walls as thick lines between rows
        for x in range(self.size + 1):
            for y in range(self.size):
                if self.horizontal_walls[x][y]:
                    start_pos = (y * cell_size, x * cell_size)
                    end_pos = ((y + 1) * cell_size, x * cell_size)
                    pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos, width=5)

        # Draw vertical walls as thick lines between columns
        for x in range(self.size):
            for y in range(self.size + 1):
                if self.vertical_walls[x][y]:
                    start_pos = (y * cell_size, x * cell_size)
                    end_pos = (y * cell_size, (x + 1) * cell_size)
                    pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos, width=5)

        pygame.display.flip()

    def get_adjacency_matrix(self):
        """
        현재 환경의 벽 상태를 고려하여 인접 행렬을 반환합니다.
        Returns:
            numpy.ndarray: size*size x size*size 크기의 인접 행렬
        """
        n = self.size * self.size
        adj_matrix = np.zeros((n, n), dtype=int)
        
        for x in range(self.size):
            for y in range(self.size):
                current = x * self.size + y
                # 현재 위치 임시 저장
                temp_pos = self.agent_pos.copy()
                self.agent_pos = np.array([x, y])
                
                # 상하좌우 이동 가능 여부 확인
                if x > 0 and not self.sense_up_wall():
                    adj_matrix[current][(x-1)*self.size + y] = 1
                
                if x < self.size-1 and not self.sense_down_wall():
                    adj_matrix[current][(x+1)*self.size + y] = 1
                
                if y > 0 and not self.sense_left_wall():
                    adj_matrix[current][x*self.size + (y-1)] = 1
                
                if y < self.size-1 and not self.sense_right_wall():
                    adj_matrix[current][x*self.size + (y+1)] = 1
                
                # 원래 위치로 복원
                self.agent_pos = temp_pos
                
        return adj_matrix

    def get_adjacency_list(self):
        """
        현재 환경의 벽 상태를 고려하여 좌표 튜플의 양방향 인접 리스트 그래프를 반환합니다.
        Returns:
            dict: {(x,y): [(nx1,ny1), (nx2,ny2), ...]} 형태의 인접 리스트
        """
        adj_list = {}
        
        # 모든 셀에 대해 순회
        for x in range(self.size):
            for y in range(self.size):
                adj_list[(x,y)] = []
                
                # 현재 위치 임시 저장
                temp_pos = self.agent_pos.copy()
                self.agent_pos = np.array([x, y])
                
                # 상하좌우 이동 가능 여부 확인
                # 위쪽 확인
                if x > 0 and not self.sense_up_wall():
                    adj_list[(x,y)].append((x-1, y))
                
                # 아래쪽 확인
                if x < self.size-1 and not self.sense_down_wall():
                    adj_list[(x,y)].append((x+1, y))
                
                # 왼쪽 확인
                if y > 0 and not self.sense_left_wall():
                    adj_list[(x,y)].append((x, y-1))
                
                # 오른쪽 확인
                if y < self.size-1 and not self.sense_right_wall():
                    adj_list[(x,y)].append((x, y+1))
                
                # 원래 위치로 복원
                self.agent_pos = temp_pos
                
        return adj_list
    
    def follow_path(self, path):
        """
        주어진 경로를 따라 로봇을 이동시킵니다.
        
        Args:
            path: 좌표 튜플들의 리스트 [(x1,y1), (x2,y2), ...]
        """
        if not path:
            print("유효한 경로가 없습니다.")
            return
        
        print("\n경로 따라 이동 시작:")
        for i in range(len(path)-1):
            current = path[i]
            next_pos = path[i+1]
            
            # 이동 방향 결정
            dx = next_pos[0] - current[0]
            dy = next_pos[1] - current[1]
            self.place()

            # 해당 방향으로 이동
            if dx == -1:
                print(f"{current} -> 위로 이동")
                self.move_up()
            elif dx == 1:
                print(f"{current} -> 아래로 이동")
                self.move_down()
            elif dy == -1:
                print(f"{current} -> 왼쪽으로 이동")
                self.move_left()
            elif dy == 1:
                print(f"{current} -> 오른쪽으로 이동")
                self.move_right()
                
        self.place()
        print(f"목표 지점 도달: {path[-1]}")

    def load_broken_bridge(self):
        """깨진 다리 패턴을 로드하고 에이전트를 시작 위치로 설정합니다."""
        # 박스 패턴 정의
        self.objects_grid = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 0, 1, 0, 0],
            [1, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 1],
            [0, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 0, 1]
        ])
        
        # 에이전트 위치를 첫 번째 다리의 시작점으로 설정
        self.agent_pos = np.array([3, 0])
        
        # 환경 렌더링
        self.render()
        time.sleep(self.delay)

    def create_room(self):
        """Create a simple room with walls and a box."""
        self.reset()

        # Horizontal walls (between rows)
        self.horizontal_walls[1][1:4] = 1
        self.horizontal_walls[4][1:4] = 1
        self.vertical_walls[1][1] = 1     # Block column 2 partially (row 0 to row 1)
        self.vertical_walls[2][1] = 1     # Block column 2 partially (row 0 to row 1)
        self.vertical_walls[3][1] = 1     # Block column 2 partially (row 0 to row 1)
        self.vertical_walls[1][4] = 1     # Block column 2 partially (row 0 to row 1)
        self.vertical_walls[3][4] = 1     # Block column 2 partially (row 0 to row 1)
        
        self.objects_grid[3, 1] = 1

        self.render()
        time.sleep(self.delay)
        return self._get_obs()

    def create_random_maze(self, complexity=0.75, density=0.5):
        """
        Generate a random maze with customizable complexity and density.
        Ensures there is at least one valid path from the start to the goal.

        Parameters:
            complexity (float): Determines the number of walls. Range: 0 to 1.
            density (float): Determines the size of open areas. Range: 0 to 1.
        """
        self.reset()

        # Ensure complexity and density are within valid ranges
        complexity = max(0, min(complexity, 1))
        density = max(0, min(density, 1))

        # Initialize grids
        self.horizontal_walls = np.ones((self.size + 1, self.size), dtype=int)
        self.vertical_walls = np.ones((self.size, self.size + 1), dtype=int)

        # Adjust complexity and density relative to maze size
        num_cells = self.size * self.size
        num_walls = int(complexity * (5 * num_cells))
        
        # Create a random maze using Prim's algorithm
        visited = np.zeros((self.size, self.size), dtype=bool)
        
        def is_within_bounds(x, y):
            """Check if coordinates are within grid bounds."""
            return 0 <= x < self.size and 0 <= y < self.size

        def knock_down_wall(x1, y1, x2, y2):
            """Remove the wall between two adjacent cells."""
            if x1 == x2:  # Vertical wall
                wall_y = min(y1, y2)
                self.vertical_walls[x1][wall_y] = 0
            elif y1 == y2:  # Horizontal wall
                wall_x = min(x1, x2)
                self.horizontal_walls[wall_x][y1] = 0

        # Start with a random cell
        stack = [(np.random.randint(self.size), np.random.randint(self.size))]
        visited[stack[0][0], stack[0][1]] = True

        while stack:
            x, y = stack[-1]
            neighbors = []

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if is_within_bounds(nx, ny) and not visited[nx][ny]:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = neighbors[np.random.randint(len(neighbors))]
                knock_down_wall(x, y, nx, ny)
                visited[nx][ny] = True
                stack.append((nx, ny))
            else:
                stack.pop()

        # Add additional random walls based on complexity
        for _ in range(num_walls):
            if np.random.rand() > 0.5:  # Horizontal wall
                x = np.random.randint(0, self.size + 1)
                y = np.random.randint(0, self.size)
                self.horizontal_walls[x][y] = 1
            else:  # Vertical wall
                x = np.random.randint(0, self.size)
                y = np.random.randint(0, self.size + 1)
                self.vertical_walls[x][y] = 1

        # Ensure connectivity using BFS or DFS to validate path existence
        if not self._ensure_path_exists():
            print("Warning: Maze generated without a valid path. Retrying...")
            return self.create_random_maze(complexity=complexity * 0.9)

        self.render()
        time.sleep(self.delay)
        return self._get_obs()

    def _ensure_path_exists(self):
        """Check if there's a valid path from start to goal using BFS."""
        from queue import Queue

        start = (0, 0)
        goal = (self.size - 1, self.size - 1)
        
        queue = Queue()
        queue.put(start)
        
        visited_path_check = set()
        visited_path_check.add(start)

        def is_within_bounds(x, y):
            return 0 <= x < self.size and 0 <= y < self.size

        while not queue.empty():
            cx, cy = queue.get()
            if (cx, cy) == goal:
                return True

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if is_within_bounds(nx, ny) and (nx, ny) not in visited_path_check:
                    if dx == -1 and not self.horizontal_walls[cx][cy]:       # Up
                        queue.put((nx, ny))
                        visited_path_check.add((nx, ny))
                    elif dx == 1 and not self.horizontal_walls[cx + 1][cy]: # Down
                        queue.put((nx, ny))
                        visited_path_check.add((nx, ny))
                    elif dy == -1 and not self.vertical_walls[cx][cy]:      # Left
                        queue.put((nx, ny))
                        visited_path_check.add((nx, ny))
                    elif dy == 1 and not self.vertical_walls[cx][cy + 1]:   # Right
                        queue.put((nx, ny))
                        visited_path_check.add((nx, ny))

        return False

    def create_maze(self):
        """Create a predefined maze with no cycles."""
        self.reset()

        # Horizontal walls (between rows)
        self.horizontal_walls[1][1:3] = 1  # Block row 1 partially
        self.horizontal_walls[2][2:3] = 1  # Block row 2 partially
        self.horizontal_walls[3][2:3] = 1  # Block row 3 partially

        # Vertical walls (between columns)
        self.vertical_walls[0][1] = 1     # Block column 2 partially (row 0 to row 1)
        self.vertical_walls[2][1] = 1     # Block column 2 partially (row 0 to row 1)
        self.vertical_walls[3][1] = 1     # Block column 2 partially (row 0 to row 1)
        self.vertical_walls[2][3] = 1     # Block column 3 partially (row 2 to row 3)
        self.vertical_walls[3][3] = 1     # Block column 2 partially (row 0 to row 1)

        self.render()
        time.sleep(self.delay)
        return self._get_obs()

    def keep_window_open(self):
        """PyGame 창을 유지하고 종료 이벤트를 처리합니다."""
        print("Press 'ESC' or 'ENTER' to close the window to exit.")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 창 닫기 버튼 클릭 시 종료
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # ESC 키를 누르면 종료
                        running = False

        self.close()  # 환경 정리