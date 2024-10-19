import mido

def note_number_to_name(note_number):
    """Convert MIDI note number to note name (e.g., C4, D#3)."""
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (note_number // 12) - 1
    note = note_names[note_number % 12]
    return f"{note}{octave}"

def parse_midi_with_mido(midi_file_path):
    midi = mido.MidiFile(midi_file_path)

    # Extract the ticks per beat (PPQ) from the MIDI file
    ticks_per_beat = midi.ticks_per_beat

    output_lines = []
    output_lines.append(f"Tempo: {80.00:.2f} BPM")  # Default tempo or extracted tempo here if needed
    output_lines.append(f"Ticks per beat: {ticks_per_beat}")

    # Loop through each track and extract note information without track names
    for track in midi.tracks:
        cumulative_time = 0  # To track the absolute time of the note events in ticks

        for msg in track:
            # Sum up the delta time to get the absolute time in ticks
            cumulative_time += msg.time

            if msg.type == 'note_on' and msg.velocity > 0:
                note_name = note_number_to_name(msg.note)

                output_lines.append(f"Note_on - Note: {note_name} (MIDI {msg.note}), "
                                    f"Velocity: {msg.velocity}, "
                                    f"Time (ticks): {cumulative_time}")

            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                note_name = note_number_to_name(msg.note)

                output_lines.append(f"Note_off - Note: {note_name} (MIDI {msg.note}), "
                                    f"Velocity: {msg.velocity}, "
                                    f"Time (ticks): {cumulative_time}")

    # Join all output lines into a single text string
    midi_text = "\n".join(output_lines)
    return midi_text


# Usage
midi_file_path = "/Users/syrusaslam1/code_projects/backend/midi_parse/midi_data/Chords/bruhbruhbruh.mid"
midi_text = parse_midi_with_mido(midi_file_path)

# Save to a file or print
with open("parsed_midi_with_note_names.txt", "w") as text_file:
    text_file.write(midi_text)

print(midi_text)
