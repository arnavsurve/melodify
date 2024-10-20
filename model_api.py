import os
import requests
import json
from gradio_client import Client, handle_file

# Step 1: Call /lambda_1
client = Client("skytnt/midi-composer")
lambda_result = client.predict(api_name="/lambda_1")

# Step 2: Call /run with your local MIDI file
midi_file_path = "midi_parse/midi_data/Sequences/ok.mid"  # Replace with your actual MIDI file path

run_result = client.predict(
    model_name="generic pretrain model (tv2o-medium) by skytnt",
    continuation_select="all",
    instruments=["Acoustic Grand"],
    drum_kit="None",
    bpm=0,
    time_sig="auto",
    key_sig="auto",
    mid=handle_file(midi_file_path),  # Use your local MIDI file
    midi_events=128,
    reduce_cc_st=True,
    remap_track_channel=True,
    add_default_instr=True,
    remove_empty_channels=False,
    seed=0,
    seed_rand=True,
    gen_events=512,
    temp=1,
    top_p=0.95,
    top_k=20,
    allow_cc=True,
    api_name="/run"
)
print(f"Run API result: {run_result}")

# Step 3: Call /finish_run to finalize and retrieve MIDI files
finish_result = client.predict(
    model_name="generic pretrain model (tv2o-medium) by skytnt",
    api_name="/finish_run"
)

selected_notes = finish_result[0]

print(selected_notes)

folder_path = 'backend/json_files'

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Define the file path where you want to save the JSON file
file_path = os.path.join(folder_path, 'selected_notes.json')

# Save the selected notes as a JSON file
with open(file_path, 'w') as json_file:
    json.dump(selected_notes, json_file, indent=4)

print(f'Saved finish_result[0] as a JSON file at: {file_path}')