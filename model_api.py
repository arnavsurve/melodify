import shutil
from gradio_client import Client, handle_file

# Step 1: Call /lambda_1
client = Client("skytnt/midi-composer")
lambda_result = client.predict(api_name="/lambda_1")

# Step 2: Call /run with your local MIDI file
# midi_file_path = "midi_parse/midi_data/Sequences/ok.mid"  # Replace with your actual MIDI file path
midi_file_path = "./midi_parse/minecraft_type_melody.mid"  # Replace with your actual MIDI file path

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
    gen_events=256,
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

# copy from /private/var/folders/...
shutil.copy(finish_result[0], "./midi_parse/generated/")
