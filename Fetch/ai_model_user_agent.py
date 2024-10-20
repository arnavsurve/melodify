from uagents import Agent, Context, Model

# Define a model class for requesting MIDI file processing
class MidiRequest(Model):
    midi_file_path: str

class MidiResponse(Model):
    output: str  # The processed response from the AI Model Agent

# Create the AI Model User Agent
ai_model_user_agent = Agent(name="ai_model_user_agent")

# Address of the AI Model Agent
AI_MODEL_AGENT_ADDRESS = "agent1qfhleus80ckt5s4krllm22aam39d23etyy2pm2aw6vl6yyye82jxvuweqp9"

@ai_model_user_agent.on_event("startup")
async def send_midi_request(ctx: Context):
    """Send a MIDI file to the AI Model Agent when the agent starts."""
    midi_file_path = "midi_parse/midi_data/Melodies/bruhbruh.mid"  # Change to your MIDI file path
    ctx.logger.info(f"Sending MIDI file {midi_file_path} to AI Model Agent")
    
    await ctx.send(AI_MODEL_AGENT_ADDRESS, MidiRequest(midi_file_path=midi_file_path))

@ai_model_user_agent.on_message(model=MidiResponse)
async def handle_midi_response(ctx: Context, sender: str, msg: MidiResponse):
    """Handle the response from the AI Model Agent after MIDI processing."""
    ctx.logger.info(f"Received response from AI Model Agent: {msg.output}")

if __name__ == "__main__":
    ai_model_user_agent.run()