# Thoughtful Agents Web Demo

A web-based visualization interface for the Thoughtful Agents framework, demonstrating proactive AI agents with inner thoughts in real-time.

## Features

- **Three-Panel Interface**: Visualize Memory, Conversation, and Inner Thoughts simultaneously
- **Real-Time Updates**: Server-Sent Events (SSE) for live streaming of agent activities
- **Interactive Triggers**: Send custom messages to trigger agent responses
- **Vehicle Assistant Demo**: Based on the low fuel memory pattern scenario

## Architecture

### Backend (Flask)
- `app.py`: Flask server with SSE endpoints
- Extends the vehicle assistant scenario with UI event emissions
- Handles real-time event streaming to connected clients

### Frontend
- `templates/index.html`: Three-panel layout
- `static/css/style.css`: Modern, responsive styling
- `static/js/app.js`: Client-side SSE handling and UI updates

## Installation

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Ensure you have your OpenAI API key set:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Running the Demo

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser to:
```
http://localhost:5000
```

3. Click "▶️ Start Demo" to run the vehicle assistant scenario

4. Watch as the three panels update in real-time:
   - **Memory**: Shows the agent's learned patterns and knowledge
   - **Conversation**: Displays the dialogue between driver and assistant
   - **Inner Thoughts**: Reveals the agent's cognitive process and intrinsic motivation scores

## Custom Triggers

Use the trigger input box to send custom messages to the agent during the demo:

Example triggers:
- "Traffic ahead on Nguyễn Huệ Street"
- "Driver seems tired"
- "Restaurant recommendation needed"

## How It Works

1. **Event Stream**: The server establishes an SSE connection with the client
2. **Scenario Execution**: The vehicle assistant scenario runs asynchronously
3. **Event Emission**: Key events (thoughts, messages, memory updates) are pushed to clients
4. **UI Updates**: JavaScript handlers update the appropriate panels in real-time

## Technical Details

### Server-Sent Events (SSE)
The demo uses SSE for one-way server-to-client communication, which is ideal for:
- Real-time updates without polling
- Automatic reconnection
- Simple implementation compared to WebSockets

### Extended Classes
- `UIAgent`: Extends `Agent` to emit UI events for thoughts and messages
- `UIHuman`: Extends `Human` to emit UI events for messages

### Event Types
- `scenario_started`: Demo initialization
- `memory_initialized`: Agent memory loaded
- `agent_message`: Agent speaks
- `human_message`: Human speaks
- `system_message`: System events
- `inner_thought`: Agent generates a thought
- `scenario_completed`: Demo finished

## Customization

### Adding New Scenarios
To add a new scenario:

1. Create your scenario function (similar to `run_demo_scenario`)
2. Use `UIAgent` and `UIHuman` for participants
3. Call `emit_event()` for custom events
4. Update the UI to handle new event types

### Styling
Modify `static/css/style.css` to customize:
- Color schemes
- Panel layouts
- Animations
- Responsive breakpoints

## Future Enhancements

- [ ] Support for multiple concurrent scenarios
- [ ] Recording and playback of demo sessions
- [ ] Export conversation history
- [ ] Voice integration for driver messages
- [ ] Additional vehicle assistant scenarios (restaurants, museums, etc.)

## Troubleshooting

**SSE connection drops:**
- Check that the Flask server is running
- Verify no firewall blocking port 5000
- Look for errors in browser console

**No updates appearing:**
- Ensure OpenAI API key is set correctly
- Check Flask console for errors
- Verify asyncio event loop is running

**Memory not displaying:**
- Wait for the `memory_initialized` event
- Check that agent memory is properly initialized

## Related Files

- Main scenario: `../examples/vehicle_assistant_scenario2.py`
- Framework core: `../thoughtful_agents/`
- Requirements: `../requirements.txt`
