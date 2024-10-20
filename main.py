from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/midi', methods=["POST"])
def handle_post_midi():
    notes = request.json['notes']
    print(notes)
    return jsonify({"status": "success", "notes_received": notes}), 200 # TODO: return newly generated midi

if __name__ == "__main__":
    app.run("127.0.0.1", 5001)
