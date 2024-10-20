from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/midi', methods=["POST"])
def handle_post_midi():
    data = request.get_json()
    if not data or 'notes' not in data:
        return jsonify({"status": "error", "message": "Invalid input"}), 400

    notes = data["notes"]
    tempo = data["tempo"]
    print(data)
    return jsonify({"tempo": tempo, "notes": notes}), 200 # TODO: return newly generated midi

if __name__ == "__main__":
    app.run("127.0.0.1", 5001)
