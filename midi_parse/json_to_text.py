import json

def parse_midi_json_to_text(json_file, output_file):
    with open(json_file, 'r') as f:
        midi_data = json.load(f)
    
    output_lines = []
    
    # Iterate over the notes in the JSON and extract necessary fields
    for note in midi_data['notes']:
        pitch = note['pitch']
        start_time = note['start_time']
        duration = note['duration']
        velocity = note['velocity']
        
        # Format the output for each note
        output_lines.append(f"{pitch},{start_time},{duration},{velocity}")
    
    # Join all lines and write to the output file
    output_text = "\n".join(output_lines)
    with open(output_file, 'w') as out_f:
        out_f.write(output_text)

# Usage
json_file = "midi_parse/midi_to_json.json"
output_file = "midi_parse/parsed_midi_data.txt"
parse_midi_json_to_text(json_file, output_file)

print(f"Parsed MIDI data saved to {output_file}")