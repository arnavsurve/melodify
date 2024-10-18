from flask import Flask, request

app = Flask(__name__)

@app.route('/midi', methods=['POST'])
def receive_midi():
    req = request.json  # Expecting MIDI data in JSON format
    print(f"Received data: {req}")
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9998)

