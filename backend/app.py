from flask import Flask
from flask_cors import CORS
from routes.nodes import nodes_bp
from routes.edges import edges_bp
from database.db import init_db

app = Flask(__name__)
CORS(app)

app.register_blueprint(nodes_bp)
app.register_blueprint(edges_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)