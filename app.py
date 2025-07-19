from flask import Flask
from src.sliding_game import puzzle_bp
from src.game import Game, generate_solvable_15_puzzle

app = Flask(__name__)
app.secret_key = "secret"
app.register_blueprint(puzzle_bp)

@app.route("/test")
def test():
    return "Hello from test route"

if __name__ == "__main__":
    # game = Game(generate_solvable_15_puzzle())
    # game.solve()
    # game.print_history()
    app.run(debug=True, use_reloader=True)
