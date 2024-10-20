import mido
import json

def convert_json_to_midi(json_file_path, output_midi_path):
    # Load the JSON file with the note data
    with open(json_file_path, 'r') as json_file:
        midi_data = json.load(json_file)

    # Create a new MIDI file and a track
    midi = mido.MidiFile()
    track = mido.MidiTrack()
    midi.tracks.append(track)

    ticks_per_beat = midi.ticks_per_beat
    current_time_in_ticks = 0  # Time tracker in ticks

    # Go through each note in the JSON and recreate the note_on and note_off messages
    for note in midi_data['notes']:
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

# Example usage
output_file = "/Users/maxkessler/Desktop/Fetch/output.midi"
json_data = "/Users/maxkessler/Desktop/Fetch/midi_data.json"
convert_json_to_midi(json_data, output_file)