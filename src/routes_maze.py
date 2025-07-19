from flask import Blueprint, jsonify, render_template, request, session
from .maze import MazeGame

maze_bp = Blueprint('maze', __name__, template_folder='templates')

@maze_bp.route("/api/maze")
def maze():
    maze = MazeGame().maze
    session['maze'] = maze
    return jsonify(maze)


@maze_bp.route("/api/maze/solve")
def solve_maze():
    maze_data = session.get('maze')
    if not maze_data:
        return jsonify({'error': 'Maze not generated yet'}), 400

    game = MazeGame(maze=maze_data)
    algorithm = request.args.get('algorithm', 'bfs')

    path = game.solve(algorithm=algorithm)
    stats = game.get_stats()

    return jsonify({
        'maze': game.maze,
        'path': path,
        'visited': stats['visited_cells'],
        'steps': stats['steps']
    })
