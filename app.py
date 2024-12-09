from flask import Flask, send_from_directory

app = Flask(__name__)

# Route to serve JSON files
@app.route("/<path:filename>")
def serve_json(filename):
    return send_from_directory("static/json", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)