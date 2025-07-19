import random
from collections import deque

class MazeGame:
    def __init__(self, rows=21, cols=29, maze=None):
        if maze:
            self.maze = maze
            self.rows = len(maze)
            self.cols = len(maze[0])
            self.start = self._find_symbol('S')
            self.goal = self._find_symbol('G')
        else:
            self.rows = rows if rows % 2 == 1 else rows + 1
            self.cols = cols if cols % 2 == 1 else cols + 1
            self.start = (0, 0)
            self.goal = (self.rows - 1, self.cols - 1)
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
