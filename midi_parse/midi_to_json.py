import mido
import json

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

# Example usage
midi_file = "midi_parse/midi_data/Sequences/ok.mid"
output_json = "midi_parse/midi_to_json.json"
midi_to_custom_json(midi_file, output_json)