from flask import Flask, request, jsonify
import mido
from model_api import generateNewMidi
import socket
import json
import os

app = Flask(__name__)

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_IP = "127.0.0.1"
UDP_PORT = 4999

def send_udp_json(json_file_path):
    # Read JSON data from the file
    if not os.path.exists(json_file_path):
        print(f"Error: The file {json_file_path} does not exist.")
        return
    
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
    
    # Convert the JSON data to a string
    json_string = json.dumps(json_data)

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 4999)

    # Chunk the JSON string into manageable parts (512 bytes each)
    chunk_size = 512
    for i in range(0, len(json_string), chunk_size):
        chunk = json_string[i:i + chunk_size]
        sock.sendto(chunk.encode('utf-8'), server_address)

    # Send the "ENDOF" marker to indicate end of transmission
    sock.sendto("ENDOF".encode('utf-8'), server_address)
    print("Data has been sent successfully.")

    # Close the socket
    sock.close()

def midi_to_custom_json(midi_file_path, output_json_path):
    midi = mido.MidiFile(midi_file_path)
    ticks_per_beat = midi.ticks_per_beat
    notes = []
    current_time = 0  # To track absolute time in ticks
    active_notes = {}  # To store note-on events
    note_id = 1  # We will assign a note ID to each note

    # Loop through each track and extract note information
    for track in midi.tracks:
        for msg in track:
            current_time += msg.time  # Accumulate time in ticks

            if msg.type == 'note_on' and msg.velocity > 0:
                # Store the note-on event with additional data needed for JSON
                active_notes[msg.note] = {
                    'start_time': current_time,
                    'velocity': msg.velocity,
                    'note_id': note_id,
                    'mute': 0,  # Assuming notes are not muted
                    'probability': 1,  # Assuming full probability for notes
                    'velocity_deviation': 0,  # Assuming no velocity deviation
                    'release_velocity': 0  # Assuming no release velocity
                }
                note_id += 1

            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in active_notes:
                    # Calculate the note duration
                    note_on_data = active_notes.pop(msg.note)
                    start_time = note_on_data['start_time']
                    velocity = note_on_data['velocity']
                    duration = current_time - start_time

                    # Convert ticks to seconds (assuming 120 BPM for simplicity)
                    start_time_in_seconds = mido.tick2second(start_time, ticks_per_beat, 500000)
                    duration_in_seconds = mido.tick2second(duration, ticks_per_beat, 500000)

                    # Add the note to the list in the required format
                    notes.append({
                        'note_id': note_on_data['note_id'],
                        'pitch': msg.note,
                        'start_time': start_time_in_seconds,
                        'duration': duration_in_seconds,
                        'velocity': velocity,
                        'mute': note_on_data['mute'],
                        'probability': note_on_data['probability'],
                        'velocity_deviation': note_on_data['velocity_deviation'],
                        'release_velocity': note_on_data['release_velocity']
                    })

    # Save the note data as JSON in the exact structure
    midi_data = {'notes': notes}
    with open(output_json_path, 'w') as json_file:
        json.dump(midi_data, json_file, indent=4)

    print(f"Converted MIDI to custom JSON and saved to {output_json_path}")

    return output_json_path


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

    path = generateNewMidi();
    output_json = "midi_parse/converted.json"
    midi_to_custom_json(path, output_json)

    send_udp_json(output_json)

    return jsonify({"tempo": tempo, "notes": notes}), 200

if __name__ == "__main__":
    try:
        app.run("127.0.0.1", 5001)
    finally:
        udp_socket.close()

