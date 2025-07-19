from flask import Blueprint, jsonify, request, session

from .maze import MazeGame

maze_bp = Blueprint('maze', __name__, template_folder='templates')

@maze_bp.route("/api/maze")
def maze():
    maze = MazeGame().maze
    session['maze'] = maze
    return jsonify(maze)

@maze_bp.route("/api/multi_path_maze")
def multi_path_maze():
    game = MazeGame(rows=21, cols=31)
    game.generate_maze_with_two_paths()
    maze = game.maze
    session['maze'] = maze
    return jsonify(maze)

@maze_bp.route("/api/maze/solve")
def solve_maze():
    import copy

    algorithm = request.args.get('algorithm', 'bfs')
    raw_maze = session.get('maze')

    if not raw_maze:
        return jsonify({'error': 'Maze not generated yet'}), 400

    def clean_maze(maze):
        return [
            [0 if cell in ('S', 'G') else cell for cell in row]
            for row in maze
        ]

    cleaned_maze = clean_maze(raw_maze)
    start = (0, 0)
    goal = (len(cleaned_maze) - 1, len(cleaned_maze[0]) - 1)

    game = MazeGame(maze=copy.deepcopy(cleaned_maze), start=start, goal=goal)
    path = game.solve(algorithm=algorithm)
    stats = game.get_stats()

    optimal_game = MazeGame(maze=copy.deepcopy(cleaned_maze), start=start, goal=goal)
    optimal_path = optimal_game.solve(algorithm='bfs')

    return jsonify({
        'maze': raw_maze,
        'path': path or [],
        'visited': stats['visited_cells'],
        'steps': stats['steps'],
        'optimal': optimal_path or []
    })
