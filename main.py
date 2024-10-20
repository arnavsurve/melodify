from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_IP = "127.0.0.1"
UDP_PORT = 4999


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

    # convert notes and tempo to bytes and send over UDP
    notes_bytes = bytes(str(notes), 'utf-8')
    tempo_bytes = bytes(str(tempo), 'utf-8')

    # send tempo and notes separately
    udp_socket.sendto(tempo_bytes, (UDP_IP, UDP_PORT))
    udp_socket.sendto(notes_bytes, (UDP_IP, UDP_PORT))

    return jsonify({"tempo": tempo, "notes": notes}), 200

if __name__ == "__main__":
    try:
        app.run("127.0.0.1", 5001)
    finally:
        udp_socket.close()
