import copy
from random import choice

from collections import deque

SOLVED = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]

REVERSE_DIRECTION = {
    'up': 'down',
    'down': 'up',
    'left': 'right',
    'right': 'left'
}

def is_solvable(board):
    flat = [num for row in board for num in row]
    inversions = 0

    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] != 0 and flat[j] != 0 and flat[i] > flat[j]:
                inversions += 1

    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                row_from_bottom = 3 - i

    return (inversions + row_from_bottom) % 2 == 0


def generate_solvable_15_puzzle():
    solved = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]
    game = Game(solved)
    directions = ['up', 'down', 'left', 'right']
    for _ in range(10):
        possible = game.current_state.possible_moves()
        if possible:
            move = choice(possible)
            game.current_state = move
    return game.current_state.board


def generate_15_puzzle():
    return [
        [1, 2, 0, 3],
        [5, 6, 7, 4],
        [9, 10, 11, 8],
        [13, 14, 15, 12]
    ]

def bfs(start_state, max_nodes=100000):
    visited = set()
    queue = deque([start_state])
    count = 0

    while queue:
        current = queue.popleft()
        count += 1

        if count > max_nodes:
            print("BFS aborted: too many nodes explored.")
            return None

        if current.is_goal():
            return current.moves

        visited.add(current)

        for neighbor in current.possible_moves():
            if neighbor not in visited:
                queue.append(neighbor)

    return None



class PuzzleState:
    def __init__(self, board, empty_pos=None, moves=[]):
        self.board = board
        self.moves = moves

        if empty_pos is None:
            for i in range(4):
                for j in range(4):
                    if board[i][j] == 0:
                        self.empty_pos = (i, j)
                        break
        else:
            self.empty_pos = empty_pos

    def is_goal(self):
        return self.board == SOLVED

    def possible_moves(self):
        directions = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }

        moves = []
        x, y = self.empty_pos

        for direction, (dx, dy) in directions.items():
            dx, dy = x + dx, y + dy
            if 0 <= dx < 4 and 0 <= dy < 4:
                new_board = copy.deepcopy(self.board)
                new_board[x][y], new_board[dx][dy] = new_board[dx][dy], new_board[x][y]
                new_moves = self.moves + [direction]
                moves.append(PuzzleState(new_board, (dx, dy), new_moves))
        return moves

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))


class Game:
    def __init__(self, initial_board):
        self.initial_state = PuzzleState(initial_board)
        self.current_state = self.initial_state
        self.history = [{
            "board": copy.deepcopy(self.initial_state.board),
            "direction": None,
            "tile": None
        }]

    def reset(self):
        self.current_state = self.initial_state
        self.history = [{
            "board": copy.deepcopy(self.initial_state.board),
            "direction": None,
            "tile": None
        }]


    def move(self, direction):
        possible_states = self.current_state.possible_moves()
        for state in possible_states:
            if state.moves[-1] == direction:
                # Find what tile was moved (swapped with 0)
                x0, y0 = self.current_state.empty_pos
                x1, y1 = state.empty_pos  # new empty position (0 moved here)
                moved_tile = self.current_state.board[x1][y1]

                self.current_state = state
                self.history.append({
                    "board": copy.deepcopy(state.board),
                    "direction": REVERSE_DIRECTION[direction],  # flip it
                    "tile": moved_tile
                })
                return True
        return False

    def solve(self):
        # Clear history and include initial state before solving
        self.history = [{
            "board": copy.deepcopy(self.current_state.board),
            "direction": None,
            "tile": None
        }]


        solution_moves = bfs(self.current_state)
        if solution_moves is None:
            print("No solution found.")
            return []

        for move in solution_moves:
            self.move(move)

        return solution_moves

    def get_solution(self):
        print("Planning solution from current state...")
        solution_moves = bfs(self.current_state)
        print("Finished planning.")
        if solution_moves is None:
            print("No solution found.")
            return []
        return solution_moves


    def print_history(self):
        for i, step in enumerate(self.history):
            print(f"Move {i}:")
            if step["direction"] is not None:
                print(f"  → Moved tile {step['tile']} {step['direction']}")
            for row in step["board"]:
                print(row)
            print()


# def is_solvable(board):
#     flat = [num for row in board for num in row]
#     inversions = 0

#     for i in range(len(flat)):
#         for j in range(i + 1, len(flat)):
#             if flat[i] != 0 and flat[j] != 0 and flat[i] > flat[j]:
#                 inversions += 1

#     for i in range(4):
#         for j in range(4):
#             if board[i][j] == 0:
#                 blank_row_from_bottom = 4 - i

#     return (inversions + blank_row_from_bottom) % 2 == 0

# is_solvable_result = is_solvable(generate_15_puzzle())
# print('is_solvable_result: ', is_solvable_result)
