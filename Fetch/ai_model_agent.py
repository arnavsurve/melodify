from uagents import Agent, Context, Model, Field
from gradio_client import Client, handle_file

# Define a model class to handle incoming MIDI requests
class MidiRequest(Model):
    midi_file_path: str  # The path to the MIDI file to process

class MidiResponse(Model):
    output: str  # The response returned from the model after processing the MIDI file

# Create the AI Model Agent
ai_model_agent = Agent(name="ai_model_agent")

# Gradio Client setup to interact with the Hugging Face API (skytnt/midi-composer)
client = Client("skytnt/midi-composer")

@ai_model_agent.on_message(model=MidiRequest)
async def handle_midi_request(ctx: Context, sender: str, msg: MidiRequest):
    try:
        # Use the MIDI file provided in the request
        midi_file_path = msg.midi_file_path

        # Call the `/lambda_1` API endpoint with the MIDI file
        result = client.predict(
            api_name="/lambda_1",  # Call the /lambda_1 endpoint
            mid=handle_file(midi_file_path),  # Pass the MIDI file as input
        )
        
        # Send the result back to the sender
        await ctx.send(sender, MidiResponse(output=str(result)))
        ctx.logger.info(f"Successfully processed and sent response: {result}")

    except Exception as e:
        ctx.logger.error(f"Failed to process MIDI request: {e}")
        await ctx.send(sender, MidiResponse(output=f"Error: {str(e)}"))

if __name__ == "__main__":
    ai_model_agent.run()