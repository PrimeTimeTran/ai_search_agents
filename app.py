import os
from flask import Flask
from src.routes_sliding import puzzle_bp
from src.routes_maze import maze_bp

app = Flask(__name__)
app.secret_key = "secret"
app.register_blueprint(puzzle_bp)
app.register_blueprint(maze_bp)

@app.context_processor
def inject_commit_info():
    return {
        "commit_sha": os.getenv("COMMIT_SHA", "unknown"),
        "commit_url": os.getenv("COMMIT_URL", "#")
    }

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

