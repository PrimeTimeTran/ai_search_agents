from flask import Blueprint, jsonify, render_template, request, session
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

# # Works. But doesn't include optimal path
# @maze_bp.route("/api/maze/solve")
# def solve_maze():
#     maze_data = session.get('maze')
#     if not maze_data:
#         return jsonify({'error': 'Maze not generated yet'}), 400

#     game = MazeGame(maze=maze_data)
#     algorithm = request.args.get('algorithm', 'bfs')

#     path = game.solve(algorithm=algorithm)
#     stats = game.get_stats()

#     return jsonify({
#         'maze': game.maze,
#         'path': path,
#         'visited': stats['visited_cells'],
#         'steps': stats['steps']
#     })


@maze_bp.route("/api/maze/solve")
def solve_maze():
    import copy

    algorithm = request.args.get('algorithm', 'bfs')
    raw_maze = session.get('maze')

    if not raw_maze:
        return jsonify({'error': 'Maze not generated yet'}), 400

    # Remove 'S' and 'G' before solving
    def clean_maze(maze):
        return [
            [0 if cell in ('S', 'G') else cell for cell in row]
            for row in maze
        ]

    cleaned_maze = clean_maze(raw_maze)
    start = (0, 0)
    goal = (len(cleaned_maze) - 1, len(cleaned_maze[0]) - 1)

    # Create MazeGame with cleaned maze
    game = MazeGame(maze=copy.deepcopy(cleaned_maze), start=start, goal=goal)
    path = game.solve(algorithm=algorithm)
    stats = game.get_stats()

    # Also solve optimally with BFS
    optimal_game = MazeGame(maze=copy.deepcopy(cleaned_maze), start=start, goal=goal)
    optimal_path = optimal_game.solve(algorithm='bfs')

    return jsonify({
        'maze': raw_maze,  # for rendering with 'S' and 'G'
        'path': path or [],
        'visited': stats['visited_cells'],
        'steps': stats['steps'],
        'optimal': optimal_path or []
    })
