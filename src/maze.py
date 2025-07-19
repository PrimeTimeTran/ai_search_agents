import random
from collections import deque

def find_all_paths(maze, start, goal, limit=2):
    """Find up to `limit` unique paths from start to goal using BFS (not optimal for all paths)."""
    rows, cols = len(maze), len(maze[0])
    all_paths = []
    queue = deque()
    queue.append((start, [start]))
    seen_paths = set()

    while queue and len(all_paths) < limit:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            p_tuple = tuple(path)
            if p_tuple not in seen_paths:
                all_paths.append(list(path))
                seen_paths.add(p_tuple)
            continue

        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < rows and 0 <= ny < cols and
                maze[nx][ny] != 1 and (nx, ny) not in path
            ):
                queue.append(((nx, ny), path + [(nx, ny)]))
    return all_paths

class MazeGame:
    def __init__(self, rows=21, cols=29, maze=None, start=None, goal=None):
        if maze:
            self.maze = maze
            self.rows = len(maze)
            self.cols = len(maze[0])
            self.start = start or self._find_symbol('S')
            self.goal = goal or self._find_symbol('G')
        else:
            self.rows = rows if rows % 2 == 1 else rows + 1
            self.cols = cols if cols % 2 == 1 else cols + 1
            self.start = start or (0, 0)
            self.goal = goal or (self.rows - 1, self.cols - 1)
            self.generate_maze()

        self.history = []
        self.steps = 0


    def _find_symbol(self, symbol):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == symbol:
                    return (i, j)
        raise ValueError(f"Symbol {symbol} not found in maze.")

    def in_bounds(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols

    def generate_perfect_maze(self):
        self.maze = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
        visited = set()

        def carve(x, y):
            visited.add((x, y))
            self.maze[x][y] = 0
            dirs = [(0,2), (0,-2), (2,0), (-2,0)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and (nx, ny) not in visited:
                    between_x, between_y = x + dx // 2, y + dy // 2
                    self.maze[between_x][between_y] = 0
                    carve(nx, ny)

        carve(*self.start)
        self.maze[self.start[0]][self.start[1]] = 0
        self.maze[self.goal[0]][self.goal[1]] = 0

    def generate_maze(self):
        self.maze = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

        def carve_passages(x, y):
            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and self.maze[nx][ny] == 1:
                    self.maze[nx][ny] = 0
                    self.maze[x + dx // 2][y + dy // 2] = 0
                    carve_passages(nx, ny)
        self.maze[self.start[0]][self.start[1]] = 0
        carve_passages(*self.start)
        self.maze[self.goal[0]][self.goal[1]] = 0
        self.maze[self.start[0]][self.start[1]] = 'S'
        self.maze[self.goal[0]][self.goal[1]] = 'G'

    def add_second_path(self):
        """Attempt to create a second unique path to the goal by breaking one wall"""
        path = find_all_paths(self.maze, self.start, self.goal, limit=1)[0]
        wall_candidates = []

        for (x, y) in path:
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                wx, wy = x + dx, y + dy
                nx, ny = x + 2*dx, y + 2*dy
                if (
                    self.in_bounds(wx, wy) and self.in_bounds(nx, ny) and
                    self.maze[wx][wy] == 1 and self.maze[nx][ny] == 0 and (nx, ny) not in path
                ):
                    wall_candidates.append((wx, wy))

        random.shuffle(wall_candidates)
        for wx, wy in wall_candidates:
            self.maze[wx][wy] = 0
            paths = find_all_paths(self.maze, self.start, self.goal, limit=2)
            if len(paths) >= 2:
                return True  # Success!
            else:
                self.maze[wx][wy] = 1  # Revert

        return False  # Could not make second path

    def generate_maze_with_two_paths(self):
        self.generate_perfect_maze()
        success = self.add_second_path()
        self.maze[self.start[0]][self.start[1]] = 'S'
        self.maze[self.goal[0]][self.goal[1]] = 'G'
        if not success:
            print("Warning: Could not create a second path to the goal.")

    def print_maze(self):
        for row in self.maze:
            print(''.join(['█' if cell == 1 else str(cell) if cell in ['S', 'G'] else ' ' for cell in row]))

    def solve(self, algorithm='bfs'):
        if algorithm == 'bfs':
            return self._bfs()
        elif algorithm == 'dfs':
            return self._dfs()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    def _bfs(self):
        start = self.start
        goal = self.goal
        queue = deque([(start, [start])])
        visited = set()
        while queue:
            (x, y), path = queue.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            self.history.append((x, y))
            self.steps += 1
            if (x, y) == goal:
                return path
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and self.maze[nx][ny] in [0, 'G'] and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))
        return []

    def _dfs(self):
        start = self.start
        goal = self.goal
        stack = [(start, [start])]
        visited = set()
        while stack:
            (x, y), path = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            self.history.append((x, y))
            self.steps += 1
            if (x, y) == goal:
                return path
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and self.maze[nx][ny] in [0, 'G'] and (nx, ny) not in visited:
                    stack.append(((nx, ny), path + [(nx,ny)]))
        return []

    def get_stats(self):
        return {
            'steps': self.steps,
            'path_length': len(self.history),
            'visited_cells': self.history,
        }
