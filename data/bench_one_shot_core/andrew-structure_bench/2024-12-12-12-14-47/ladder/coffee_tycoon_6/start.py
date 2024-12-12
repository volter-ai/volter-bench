from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='deploy/dist')

# More specific CORS configuration
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3001",  # internal preview frontend port
            "http://localhost:5002",  # internal preview server port
            "http://127.0.0.1:3001",  # internal preview frontend port
            "http://127.0.0.1:5002",  # internal preview server port
            "http://0.0.0.0:3001",  # internal preview frontend port
            "http://0.0.0.0:5002",  # internal preview server port
        ],
        "methods": ["GET", "POST", "OPTIONS"],  # Specify allowed methods
        "allow_headers": ["Content-Type"]  # Specify allowed headers
    }
})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 8000))