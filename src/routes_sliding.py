from flask import Blueprint, jsonify, render_template, request, session

from .game import Game, generate_15_puzzle, generate_solvable_15_puzzle, SOLVED, is_solvable

puzzle_bp = Blueprint('puzzle', __name__, template_folder='templates')

def is_solved(board):
    return board == SOLVED

@puzzle_bp.route("/")
def home():
    return render_template("index.html")

@puzzle_bp.route("/puzzle")
def puzzle():
    return render_template("index.html")

@puzzle_bp.route("/api/puzzle")
def api_puzzle():
    board = generate_15_puzzle()
    if 'board' not in session:
        session['board'] = board
    return jsonify({"board": session['board']})

@puzzle_bp.route("/api/new_sliding_puzzle", methods=["POST"])
def api_new_sliding_puzzle():
    board = generate_solvable_15_puzzle()
    session['board'] = board
    return jsonify({
        "message": "New solvable board generated.",
        "board": board
    })

@puzzle_bp.route("/api/new_sliding_puzzle/easy", methods=["POST"])
def api_new_easy_sliding_puzzle():
    board = generate_15_puzzle()
    session['board'] = board
    return jsonify({
        "message": "New solvable board generated.",
        "board": board
    })

@puzzle_bp.route("/api/move", methods=["POST"])
def api_move():
    data = request.get_json()
    row, col = data['row'], data['col']
    board = session.get('board', generate_solvable_15_puzzle())
    if 'board' not in session:
        session['board'] = board
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                empty_row, empty_col = i, j
    if abs(empty_row - row) + abs(empty_col - col) == 1:
        board[empty_row][empty_col], board[row][col] = board[row][col], board[empty_row][empty_col]
        session['board'] = board
    solved = is_solved(board)
    return jsonify({"board": board, "solved": solved})

@puzzle_bp.route("/api/plan", methods=["GET"])
def plan_solution():
    board = session.get('board')
    for row in board:
        print(row)
    if not board:
        return jsonify({"error": "No board in session."}), 400

    if not is_solvable(board):
        return jsonify({"error": "Board is unsolvable."}), 400

    game = Game(board)
    solution_moves = game.get_solution()

    if not solution_moves:
        return jsonify({"error": "No solution found."}), 400

    return jsonify({
        "solution_moves": solution_moves,
        "move_count": len(solution_moves),
        "solved": is_solved(board)
    })
