from uagents import Agent, Context, Model
from flask import Flask, request, jsonify
import json
import mido

# Define the models to structure communication
class MidiData(Model):
    midi_file: str 

class GeneratedMidi(Model):
    generated_midi_json: str  # Generated MIDI data in JSON format

# AI Model User Agent address for communication
API_AGENT_ADDRESS = "agent1qvj38h98tq34se027alqcmvmlyp06l3k5vp47n3uvpqr2g3w3x0jc94p0a2"

# Initialize API agent
api_agent = Agent(
    name="api_agent",
    port=8000,
    seed="api_agent_secret_phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

# Flask app for handling HTTP requests (from Ableton or external source)
app = Flask(__name__)

# Handle incoming JSON from Ableton's plugin and forward it to the AI Model User Agent
@app.route("/submit", methods=["POST"])
def receive_midi_data():
    assert request.method == ["POST"]
    try:
        # Step 1: Receive the MIDI data as JSON
        data = request.get_json()
        notes = data.get('notes')

        # Step 2: Convert the JSON to MIDI (if necessary) or just send the raw data
        midi_file_path = "/tmp/input_midi.mid"
        convert_json_to_midi(notes, midi_file_path)  # Convert JSON to MIDI file

        # Step 3: Send the MIDI data to the AI Model User Agent
        midi_message = MidiData(midi_file_path)
        api_agent.send(API_AGENT_ADDRESS, midi_message)  # Send the message to the AI Model User Agent

        # Acknowledge request success
        return jsonify({"message": "MIDI data forwarded to AI Model User Agent"}), 200

    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

# When the API agent receives generated MIDI data back from the AI Model User Agent
@api_agent.on_message(model=GeneratedMidi)
async def handle_generated_midi(ctx: Context, sender: str, message: GeneratedMidi):
    ctx.logger.info(f"Received generated MIDI data: {message.generated_midi_json}")

    # Step 4: Optionally parse the generated MIDI data back into a MIDI file
    midi_file_path = "/tmp/generated_midi.mid"
    generated_midi_json = json.loads(message.generated_midi_json)

    # Convert the generated JSON to a MIDI file
    convert_json_to_midi(generated_midi_json, midi_file_path)

    # Step 5: Optionally send the MIDI data back to Ableton plugin, or save/send it
    # Send the MIDI data back to Ableton or handle as needed

    # For now, just log the generated MIDI
    return jsonify({"message": "Generated MIDI processed"}), 200

def convert_json_to_midi(json_body, output_midi_path):
    # do not handle json as a file but as a dictionary object
    # unmarshal JSON into .mid file and write to output_midi_path

    # Create a new MIDI file and a track
    midi = mido.MidiFile()
    track = mido.MidiTrack()
    midi.tracks.append(track)

    ticks_per_beat = midi.ticks_per_beat
    current_time_in_ticks = 0  # Time tracker in ticks

    # Go through each note in the JSON and recreate the note_on and note_off messages
    for note in json_body['notes']:
        pitch = note['pitch']
        start_time_in_seconds = note['start_time']
        duration_in_seconds = note['duration']
        velocity = int(note['velocity'])

        # Convert start time and duration from seconds to ticks
        start_time_in_ticks = mido.second2tick(start_time_in_seconds, ticks_per_beat, 500000)  # No BPM assumption
        duration_in_ticks = mido.second2tick(duration_in_seconds, ticks_per_beat, 500000)

        # Add a note_on message at the start time
        time_since_last_event = max(0, int(start_time_in_ticks - current_time_in_ticks))
        track.append(mido.Message('note_on', note=pitch, velocity=velocity, time=time_since_last_event))

        # Update current time to the start time of this event
        current_time_in_ticks = start_time_in_ticks

        # Add a note_off message after the duration
        time_to_note_off = max(0, int(duration_in_ticks))
        track.append(mido.Message('note_off', note=pitch, velocity=0, time=time_to_note_off))

        # Update current time to include the note's duration
        current_time_in_ticks += time_to_note_off

    # Save the MIDI file
    midi.save(output_midi_path)
    print(f"Converted JSON to MIDI and saved to {output_midi_path}")

# Run both Flask (for HTTP requests) and uAgent API agent for communication
if __name__ == "__main__":
    # Run Flask app for external HTTP communication
    app.run(host="0.0.0.0", port=5001)  # Flask runs on port 5001 for Ableton to communicate

    # Run the API agent for handling inter-agent communication
    api_agent.run()