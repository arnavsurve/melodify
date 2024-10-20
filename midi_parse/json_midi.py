import json
import os
from midiutil import MIDIFile

def convert_json_to_midi(json_data, output_file="output.mid"):
    # Create a MIDI file with 1 track
    midi = MIDIFile(1)
    track = 0
    time = 0
    
    # Set track name and tempo
    midi.addTrackName(track, time, "Converted from Ableton Live")
    midi.addTempo(track, time, 140)  # Default tempo 120 BPM
    
    # Parse JSON data and sort by note_id
    notes_data = json_data["notes"]
    notes_data.sort(key=lambda x: x["note_id"])
    
    # Find the time scaling factor
    # Let's try scaling the time to make it match the original MIDI
    # Assuming the original MIDI was about 1/4 of the current length
    TIME_SCALE = 0.25  
    
    # Add notes to the MIDI file
    for note in notes_data:
        # Extract note parameters
        pitch = note["pitch"]
        # Scale the time values
        start_time = note["start_time"] * TIME_SCALE
        duration = note["duration"] * TIME_SCALE
        velocity = int(note["velocity"])
        
        # Add note to MIDI file
        midi.addNote(track, 0, pitch, start_time, duration, velocity)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write the MIDI file
    with open(output_file, "wb") as f:
        midi.writeFile(f)

def analyze_timing(notes_data):
    """Analyze timing information from the notes data"""
    start_times = [note["start_time"] for note in notes_data]
    durations = [note["duration"] for note in notes_data]
    
    print(f"Time Analysis:")
    print(f"Min start time: {min(start_times)}")
    print(f"Max start time: {max(start_times)}")
    print(f"Average duration: {sum(durations) / len(durations)}")
    print(f"Total unique note_ids: {len(set(note['note_id'] for note in notes_data))}")

def main():
    # Define input and output paths
    input_path = "midi_parse/midi_dd.json"
    output_path = "midi_parse/output123.mid"
    
    # Read JSON file
    try:
        with open(input_path, "r") as f:
            json_data = json.load(f)
        
        # Analyze timing before conversion
        print("Analyzing JSON data timing...")
        analyze_timing(json_data["notes"])
            
        # Convert to MIDI
        convert_json_to_midi(json_data, output_path)
        print(f"Successfully converted JSON to MIDI file ({output_path})")
        
    except FileNotFoundError:
        print(f"Error: Input JSON file not found at {input_path}")
    except Exception as e:
        print(f"Error during conversion: {str(e)}")

if __name__ == "__main__":
    main()