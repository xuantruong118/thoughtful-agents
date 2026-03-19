# Thoughtful Agents Web Demo

A web-based visualization interface for the Thoughtful Agents framework, demonstrating proactive AI agents with inner thoughts in real-time.

## 🎯 Features

### Core Visualization
- **Three-Panel Interface**: Visualize Long-term Memory (LTM), Conversation, and Inner Thoughts simultaneously
- **Real-Time Updates**: Server-Sent Events (SSE) for live streaming of agent activities
- **Interactive Controls**: Enhanced control panel with multiple interaction modes

### Multi-User Support
- **Speaker Selection**: Dropdown to simulate conversations with multiple participants (Driver, Passenger A, Passenger B)
- **Multi-party Conversations**: Support for complex dialogue scenarios with multiple humans and AI agents

### System Triggers
- **Vehicle Event Simulation**: Dedicated control panel for simulating vehicle system events
- **Preset Triggers**: Quick-select common vehicle scenarios:
  - ⛽ Low Fuel Warning
  - 🔧 Tire Pressure Alert
  - 🌧️ Weather Changes
  - 🚦 Traffic Alerts
  - 🔩 Maintenance Reminders
- **Custom Triggers**: JSON-based custom event system for advanced scenarios

### Enhanced UI Elements
- **Live Counters**: Real-time display of memory items, conversation turns, and thought counts
- **Color-Coded Messages**: Visual distinction between human, agent, and system messages
- **Legend Panel**: Clear explanation of UI elements and IM (Intrinsic Motivation) scores
- **Responsive Design**: Adaptive layout for different screen sizes

## 🏗 Architecture

### Backend (Flask + SSE)
- `app.py`: Flask server with Server-Sent Events endpoints
- Extends the vehicle assistant scenario with UI event emissions
- Handles real-time event streaming to connected clients
- Multi-trigger support (user messages + system events)
- `/start`: Initialize demo scenario
- `/trigger`: Send user messages or system events
- `/state`: Get current demo state
- `/events`: SSE stream for real-time updates

### Frontend
- `templates/index.html`: Enhanced 3-column layout with control panels
- `static/css/style.css`: Modern, responsive styling with gradient themes
- `static/js/app.js`: Client-side SSE handling, multi-user support, and trigger management

### Event Types
The demo supports the following event types:
- `scenario_started`: Demo initialization with scenario info
- `memory_initialized`: Agent long-term memory loaded
- `agent_message`: AI agent speaks
- `human_message`: Human participant speaks
- `system_message`: System status updates
- `system_trigger`: Vehicle system events
- `inner_thought`: Agent generates internal thought (with IM score)
- `scenario_completed`: Demo finished

## 📦 Installation

### Prerequisites
```bash
# Install required Python packages
pip install flask

# Or install all dependencies
pip install -r ../requirements.txt
```

### Environment Setup
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

## 🚀 Running the Demo

### 1. Start the Flask Server
```bash
cd web_demo
python app.py
```

### 2. Open in Browser
Navigate to: `http://localhost:5000`

### 3. Use the Demo

#### A. Start the Scenario
1. Click "▶️ Start Demo" button
2. Watch the three panels populate with real-time data:
   - **Memory Panel**: Shows agent's learned patterns (e.g., daily refueling routine)
   - **Conversation Panel**: Displays dialogue between participants
   - **Inner Thoughts Panel**: Reveals agent's cognitive process with IM scores

#### B. Send User Messages (Multi-User Mode)
1. Select speaker from dropdown (Minh, Passenger A, Passenger B)
2. Type a message in the user input field
3. Click "Send" or press Enter
4. Watch the agent respond based on the message and context

Example messages:
- "I'm feeling hungry, any restaurant nearby?"
- "What's the weather like today?"
- "How much fuel do we have left?"

#### C. Send System Triggers (Proactive Mode)
1. **Use Presets**: Select from common vehicle events
   - ⛽ Low Fuel (15%)
   - 🔧 Low Tire Pressure
   - 🌧️ Heavy Rain
   - 🚦 Traffic Congestion
   - 🔩 Maintenance Due

2. **Custom JSON Triggers**: Enter your own event
   ```json
   {"event": "engine_warning", "code": "P0420"}
   {"event": "navigation", "action": "route_deviation"}
   {"event": "phone_call", "caller": "Office"}
   ```

3. Click "Send Trigger"
4. Observe how the agent:
   - Generates inner thoughts in response
   - Decides whether to speak proactively
   - Interrupts conversation if priority is high

## 🎨 UI Components

### Control Panel
- **Start/Restart Button**: Launch or restart the demo scenario
- **Status Indicator**: Shows current demo state (Ready, Running, Completed)
- **User Message Section**: Multi-user conversation input
- **System Trigger Section**: Vehicle event simulation with presets

### Panel Details

#### 💾 Long-term Memory Panel
- Displays agent's learned patterns and knowledge
- Each memory item shows:
  - Knowledge ID (KNO #)
  - Content text
  - Contextual information

#### 💬 Conversation Panel
- Shows chronological dialogue
- Color-coded by participant type:
  - 🟢 Human messages (green)
  - 🔵 Agent messages (blue)
  - 🟠 System events (orange)
- Turn numbers for reference

#### 💭 Inner Thoughts Panel
- Reveals agent's cognitive process
- Each thought shows:
  - Turn number when generated
  - IM Score (Intrinsic Motivation)
  - Thought content
  - (Future: Reference tags to related memory/conversation)

### Legend
The legend explains color coding and IM score meaning:
- **IM Score**: Measures agent's motivation to express a thought
- Higher scores = more likely to speak
- Threshold determines if agent will interrupt or wait

## 🔧 Technical Details

### Server-Sent Events (SSE)
The demo uses SSE for one-way server-to-client communication:
- ✅ Real-time updates without polling
- ✅ Automatic reconnection
- ✅ Simpler than WebSockets for this use case
- ✅ Built-in browser support

### Extended Classes
To enable UI event emission:
- `UIAgent`: Extends `Agent` to emit events for thoughts and messages
- `UIHuman`: Extends `Human` to emit events for messages

### Proactive Behavior Flow
1. **System Trigger** arrives (e.g., low fuel)
2. **Agent receives** the trigger without explicit request
3. **Inner Thoughts** are generated via deliberation
4. **Evaluation** of intrinsic motivation (IM score)
5. **Decision**: Speak now, wait, or stay silent
6. **UI Updates**: All steps visible in real-time

## 🎓 Understanding the Demo

### What is Proactive AI?
Unlike traditional reactive chatbots, this agent:
- **Monitors context** continuously (vehicle state, user patterns)
- **Generates thoughts** autonomously without prompts
- **Decides when to speak** based on intrinsic motivation
- **Can interrupt** when information is urgent

### Inner Thoughts Explained
The thoughts you see represent:
- Agent's interpretation of events
- Retrieval of relevant memories
- Evaluation of whether to speak
- Reasoning about user needs and priorities

Example thought sequence:
1. "Fuel level is 15%, below normal range"
2. "Driver usually refuels at 8:30 AM every day"
3. "Current time is 8:25 AM, close to usual time"
4. "Should proactively suggest the usual gas station"

### IM Score Interpretation
- **< 2.0**: Low motivation, agent stays silent
- **2.0 - 3.0**: Moderate motivation, waits for turn
- **> 3.0**: High motivation, may interrupt
- **> 4.0**: Urgent, definitely interrupts

(Thresholds can be configured per agent)

## 🛠 Customization

### Adding New Scenarios
To add a new scenario:

1. Create scenario function in `app.py`:
```python
async def run_custom_scenario():
    # Your scenario logic
    conversation = Conversation(context="...")
    agent = UIAgent(name="...", proactivity_config={...})
    # ... scenario steps
```

2. Update `/start` endpoint to call your scenario
3. Customize memory, participants, and events

### Adding New Trigger Presets
Edit `templates/index.html`, add to the `triggerPreset` select:
```html
<option value='{"event": "new_event", "data": "value"}'>
  🔔 New Event Name
</option>
```

### Styling Customization
Modify `static/css/style.css`:
- Color schemes: Update gradient definitions
- Panel layouts: Adjust grid-template-columns
- Animations: Modify @keyframes definitions
- Responsive breakpoints: Update @media queries

### Adding More Participants
Update `templates/index.html`, add to `speakerSelect`:
```html
<option value="Passenger C">👤 Passenger C</option>
<option value="Child">👶 Child</option>
```

## 📊 Use Cases

### 1. Research & Development
- Visualize how proactive agents think
- Debug inner thought generation
- Test different proactivity configurations
- Compare agent behaviors across scenarios

### 2. Education & Demonstration
- Teaching conversational AI concepts
- Explaining cognitive architectures
- Demonstrating System 1 vs System 2 thinking
- Showing real-time agent decision making

### 3. Vehicle UX Design
- Prototype in-vehicle assistant behaviors
- Test different trigger scenarios
- Evaluate user experience with proactive AI
- Design conversation flows

### 4. Agent Evaluation
- Assess response quality
- Measure proactivity appropriateness
- Test multi-user conversation handling
- Evaluate memory utilization

## 🐛 Troubleshooting

### SSE Connection Drops
- Check Flask server is running
- Verify no firewall blocking port 5000
- Look for errors in browser console
- Ensure no other process using port 5000

### No Updates Appearing
- Verify OpenAI API key is set correctly
- Check Flask console for errors
- Ensure asyncio event loop is running
- Check browser network tab for SSE connection

### Memory Not Displaying
- Wait for `memory_initialized` event
- Check agent memory is properly initialized
- Verify memory items are being emitted

### Triggers Not Working
- Ensure demo is started first
- Check trigger message format
- Verify `/trigger` endpoint is receiving data
- Look for errors in Flask console

### Performance Issues
- Close other browser tabs
- Reduce number of memory items
- Simplify scenario complexity
- Consider pagination for long conversations

## 🔮 Future Enhancements

- [ ] WebSocket support for bidirectional communication
- [ ] Recording and playback of demo sessions
- [ ] Export conversation history (JSON/CSV)
- [ ] Voice input for driver messages
- [ ] Multiple concurrent scenarios
- [ ] Memory editing interface
- [ ] Advanced filtering and search
- [ ] Thought visualization (graph view)
- [ ] React/Next.js frontend version
- [ ] Docker containerization

## 📚 Related Files

- Main scenario: `../examples/vehicle_assistant_scenario2.py`
- Framework core: `../thoughtful_agents/`
- Requirements: `../requirements.txt`
- Quick start guide: `QUICKSTART.md`

## 📖 References

- Paper: [Proactive Conversational Agents with Inner Thoughts](https://arxiv.org/pdf/2501.00383) (CHI 2025)
- Framework: [thoughtful-agents on GitHub](https://github.com/xybruceliu/thoughtful-agents)
- Documentation: See main `README.md` in repository root

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional vehicle scenarios
- UI/UX enhancements
- Performance optimizations
- Bug fixes
- Documentation improvements

## 📝 License

This demo is part of the thoughtful-agents framework, licensed under Apache License 2.0.

---

**Built with ❤️ using Flask, Vanilla JavaScript, and the Thoughtful Agents framework**
