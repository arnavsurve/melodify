import mido
import re

def parse_text_to_midi(text_data, output_midi_file):
    # Initialize a new MIDI file and track
    midi = mido.MidiFile()
    track = mido.MidiTrack()
    midi.tracks.append(track)
    
    # Use regular expressions to extract tempo, ticks per beat, and note events
    tempo_regex = r'Tempo: (\d+\.\d+) BPM'
    ppq_regex = r'Ticks per beat: (\d+)'
    note_on_regex = r'Note_on - Note: (.+?) \(MIDI (\d+)\), Velocity: (\d+), Time \(ticks\): (\d+)'
    note_off_regex = r'Note_off - Note: (.+?) \(MIDI (\d+)\), Velocity: (\d+), Time \(ticks\): (\d+)'
    
    current_time = 0
    
    # Extract tempo
    tempo_match = re.search(tempo_regex, text_data)
    if tempo_match:
        bpm = float(tempo_match.group(1))
        tempo = mido.bpm2tempo(bpm)  # Convert BPM to microseconds per quarter note
        track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    # Extract ticks per beat (PPQ)
    ppq_match = re.search(ppq_regex, text_data)
    if ppq_match:
        ticks_per_beat = int(ppq_match.group(1))
        midi.ticks_per_beat = ticks_per_beat
    else:
        midi.ticks_per_beat = 480  # Default value if PPQ is not found

    # Extract all note events
    for line in text_data.splitlines():
        # Handle Note On events
        note_on_match = re.search(note_on_regex, line)
        if note_on_match:
            midi_note = int(note_on_match.group(2))
            velocity = int(note_on_match.group(3))
            event_time = int(note_on_match.group(4))

            delta_time = event_time - current_time  # Calculate delta time in ticks
            current_time = event_time

            # Add the note_on event to the track
            track.append(mido.Message('note_on', note=midi_note, velocity=velocity, time=delta_time))
        
        # Handle Note Off events
        note_off_match = re.search(note_off_regex, line)
        if note_off_match:
            midi_note = int(note_off_match.group(2))
            velocity = int(note_off_match.group(3))  # This is usually 0 for note_off events
            event_time = int(note_off_match.group(4))

            delta_time = event_time - current_time  # Calculate delta time in ticks
            current_time = event_time

            # Add the note_off event to the track
            track.append(mido.Message('note_off', note=midi_note, velocity=velocity, time=delta_time))

    # Save the constructed MIDI file
    midi.save(output_midi_file)
    print(f"Saved MIDI file to {output_midi_file}")

# Example usage
text_data = """Tempo: 80.00 BPM
Ticks per beat: 15360
Note_on - Note: E5 (MIDI 76), Velocity: 115, Time (ticks): 0
Note_on - Note: D5 (MIDI 74), Velocity: 116, Time (ticks): 3840
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 4591
Note_on - Note: C5 (MIDI 72), Velocity: 105, Time (ticks): 7680
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 8481
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 15227
Note_on - Note: A4 (MIDI 69), Velocity: 107, Time (ticks): 15360
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 25293
Note_on - Note: E5 (MIDI 76), Velocity: 116, Time (ticks): 30720
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 34328
Note_on - Note: D5 (MIDI 74), Velocity: 111, Time (ticks): 34560
Note_on - Note: C5 (MIDI 72), Velocity: 118, Time (ticks): 38400
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 39647
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 45947
Note_on - Note: A4 (MIDI 69), Velocity: 108, Time (ticks): 46080
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 57194
Note_on - Note: C5 (MIDI 72), Velocity: 119, Time (ticks): 61440
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 74095
Note_on - Note: D5 (MIDI 74), Velocity: 118, Time (ticks): 76800
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 86406
Note_on - Note: E5 (MIDI 76), Velocity: 119, Time (ticks): 92160
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 110034
Note_on - Note: E5 (MIDI 76), Velocity: 116, Time (ticks): 122880
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 126291
Note_on - Note: D5 (MIDI 74), Velocity: 109, Time (ticks): 126720
Note_on - Note: C5 (MIDI 72), Velocity: 102, Time (ticks): 130560
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 131754
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 137931
Note_on - Note: A4 (MIDI 69), Velocity: 105, Time (ticks): 138240
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 146508
Note_on - Note: E5 (MIDI 76), Velocity: 117, Time (ticks): 153600
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 157405
Note_on - Note: D5 (MIDI 74), Velocity: 107, Time (ticks): 157440
Note_on - Note: C5 (MIDI 72), Velocity: 116, Time (ticks): 161280
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 162359
Note_on - Note: A4 (MIDI 69), Velocity: 106, Time (ticks): 168960
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 170159
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 180258
Note_on - Note: C5 (MIDI 72), Velocity: 117, Time (ticks): 184320
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 209163
Note_on - Note: B4 (MIDI 71), Velocity: 113, Time (ticks): 215040
Note_off - Note: B4 (MIDI 71), Velocity: 0, Time (ticks): 233410
Note_on - Note: E5 (MIDI 76), Velocity: 119, Time (ticks): 245760
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 249204
Note_on - Note: D5 (MIDI 74), Velocity: 112, Time (ticks): 249600
Note_on - Note: C5 (MIDI 72), Velocity: 116, Time (ticks): 253440
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 254417
Note_on - Note: A4 (MIDI 69), Velocity: 110, Time (ticks): 261120
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 261430
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 272099
Note_on - Note: E5 (MIDI 76), Velocity: 117, Time (ticks): 276480
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 279891
Note_on - Note: D5 (MIDI 74), Velocity: 96, Time (ticks): 280320
Note_on - Note: C5 (MIDI 72), Velocity: 117, Time (ticks): 284160
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 285034
Note_on - Note: A4 (MIDI 69), Velocity: 111, Time (ticks): 291840
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 292421
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 303552
Note_on - Note: G4 (MIDI 67), Velocity: 116, Time (ticks): 307200
Note_on - Note: A4 (MIDI 69), Velocity: 112, Time (ticks): 322560
Note_off - Note: G4 (MIDI 67), Velocity: 0, Time (ticks): 322831
Note_on - Note: B4 (MIDI 71), Velocity: 112, Time (ticks): 337920
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 339061
Note_off - Note: B4 (MIDI 71), Velocity: 0, Time (ticks): 352580
Note_on - Note: C5 (MIDI 72), Velocity: 110, Time (ticks): 353280
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 356907
Note_on - Note: E5 (MIDI 76), Velocity: 109, Time (ticks): 368640
Note_on - Note: D5 (MIDI 74), Velocity: 96, Time (ticks): 372480
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 372567
Note_on - Note: C5 (MIDI 72), Velocity: 112, Time (ticks): 376320
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 377100
Note_on - Note: A4 (MIDI 69), Velocity: 110, Time (ticks): 384000
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 384384
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 393728
Note_on - Note: E5 (MIDI 76), Velocity: 116, Time (ticks): 399360
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 402812
Note_on - Note: D5 (MIDI 74), Velocity: 109, Time (ticks): 403200
Note_on - Note: C5 (MIDI 72), Velocity: 109, Time (ticks): 407040
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 407718
Note_on - Note: A4 (MIDI 69), Velocity: 106, Time (ticks): 414720
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 415580
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 424150
Note_on - Note: G4 (MIDI 67), Velocity: 112, Time (ticks): 430080
Note_off - Note: G4 (MIDI 67), Velocity: 0, Time (ticks): 444326
Note_on - Note: A4 (MIDI 69), Velocity: 107, Time (ticks): 445440
Note_on - Note: B4 (MIDI 71), Velocity: 109, Time (ticks): 460800
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 461433
Note_off - Note: B4 (MIDI 71), Velocity: 0, Time (ticks): 476153
Note_on - Note: C5 (MIDI 72), Velocity: 102, Time (ticks): 476160
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 479407
Note_on - Note: E5 (MIDI 76), Velocity: 111, Time (ticks): 491520
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 494694
Note_on - Note: D5 (MIDI 74), Velocity: 56, Time (ticks): 495360
Note_on - Note: C5 (MIDI 72), Velocity: 96, Time (ticks): 499200
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 499578
Note_on - Note: A4 (MIDI 69), Velocity: 105, Time (ticks): 506880
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 507149
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 516609
Note_on - Note: E5 (MIDI 76), Velocity: 113, Time (ticks): 522240
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 525188
Note_on - Note: D5 (MIDI 74), Velocity: 99, Time (ticks): 526080
Note_on - Note: C5 (MIDI 72), Velocity: 114, Time (ticks): 529920
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 530971
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 537291
Note_on - Note: A4 (MIDI 69), Velocity: 108, Time (ticks): 537600
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 546045
Note_on - Note: F5 (MIDI 77), Velocity: 113, Time (ticks): 552960
Note_off - Note: F5 (MIDI 77), Velocity: 0, Time (ticks): 566935
Note_on - Note: G5 (MIDI 79), Velocity: 109, Time (ticks): 576000
Note_off - Note: G5 (MIDI 79), Velocity: 0, Time (ticks): 579329
Note_on - Note: G5 (MIDI 79), Velocity: 116, Time (ticks): 583680
Note_off - Note: G5 (MIDI 79), Velocity: 0, Time (ticks): 589244
Note_on - Note: E5 (MIDI 76), Velocity: 111, Time (ticks): 614400
Note_on - Note: D5 (MIDI 74), Velocity: 76, Time (ticks): 618240
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 618557
Note_on - Note: C5 (MIDI 72), Velocity: 105, Time (ticks): 622080
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 622520
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 629254
Note_on - Note: A4 (MIDI 69), Velocity: 104, Time (ticks): 629760
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 637016
Note_on - Note: E5 (MIDI 76), Velocity: 116, Time (ticks): 645120
Note_on - Note: D5 (MIDI 74), Velocity: 109, Time (ticks): 648960
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 649141
Note_on - Note: C5 (MIDI 72), Velocity: 111, Time (ticks): 652800
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 653994
Note_on - Note: A4 (MIDI 69), Velocity: 101, Time (ticks): 660480
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 660646
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 666662
Note_on - Note: F5 (MIDI 77), Velocity: 114, Time (ticks): 675840
Note_off - Note: F5 (MIDI 77), Velocity: 0, Time (ticks): 685970
Note_on - Note: E5 (MIDI 76), Velocity: 116, Time (ticks): 691200
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 700453
Note_on - Note: D5 (MIDI 74), Velocity: 117, Time (ticks): 706560
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 714903
Note_on - Note: C5 (MIDI 72), Velocity: 118, Time (ticks): 721920
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 724773
Note_on - Note: E5 (MIDI 76), Velocity: 114, Time (ticks): 737280
Note_on - Note: D5 (MIDI 74), Velocity: 103, Time (ticks): 741120
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 741798
Note_on - Note: C5 (MIDI 72), Velocity: 107, Time (ticks): 744960
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 745564
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 752433
Note_on - Note: A4 (MIDI 69), Velocity: 104, Time (ticks): 752640
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 762348
Note_on - Note: E5 (MIDI 76), Velocity: 119, Time (ticks): 768000
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 771246
Note_on - Note: D5 (MIDI 74), Velocity: 107, Time (ticks): 771840
Note_on - Note: C5 (MIDI 72), Velocity: 114, Time (ticks): 775680
Note_off - Note: D5 (MIDI 74), Velocity: 0, Time (ticks): 776738
Note_on - Note: A4 (MIDI 69), Velocity: 106, Time (ticks): 783360
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 783649
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 792892
Note_on - Note: G4 (MIDI 67), Velocity: 115, Time (ticks): 798720
Note_off - Note: G4 (MIDI 67), Velocity: 0, Time (ticks): 819148
Note_on - Note: A4 (MIDI 69), Velocity: 101, Time (ticks): 821760
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 824219
Note_on - Note: A4 (MIDI 69), Velocity: 112, Time (ticks): 829440
Note_on - Note: G4 (MIDI 67), Velocity: 99, Time (ticks): 844800
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 844977
Note_off - Note: G4 (MIDI 67), Velocity: 0, Time (ticks): 852945
Note_on - Note: F4 (MIDI 65), Velocity: 111, Time (ticks): 860160
Note_off - Note: F4 (MIDI 65), Velocity: 0, Time (ticks): 875377
Note_on - Note: G4 (MIDI 67), Velocity: 104, Time (ticks): 875520
Note_off - Note: G4 (MIDI 67), Velocity: 0, Time (ticks): 890364
Note_on - Note: A4 (MIDI 69), Velocity: 104, Time (ticks): 890880
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 905621
Note_on - Note: C5 (MIDI 72), Velocity: 114, Time (ticks): 906240
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 920194
Note_on - Note: B4 (MIDI 71), Velocity: 114, Time (ticks): 921600
Note_on - Note: C5 (MIDI 72), Velocity: 110, Time (ticks): 936960
Note_off - Note: B4 (MIDI 71), Velocity: 0, Time (ticks): 938305
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 951805
Note_on - Note: A4 (MIDI 69), Velocity: 113, Time (ticks): 952320
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 980222
"""
# The full text data would be here

# Output MIDI file
output_midi_file = '/Users/syrusaslam1/code_projects/backend/midi_parse/unparsed_midi_output.mid'

# Parse the text data and save as MIDI
parse_text_to_midi(text_data, output_midi_file)