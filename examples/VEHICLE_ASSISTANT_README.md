# Vehicle Virtual Assistant Simulation

This directory contains implementations of a proactive virtual assistant for vehicle scenarios, demonstrating the capabilities of the Thoughtful Agents framework.

## Overview

The implementation includes two scenarios that showcase proactive AI behavior in a vehicle context:

### Scenario 1: Passenger Conversation About Car Brands
**Vietnamese**: Trong xe đang có 2 hành khách trò chuyện với nhau, chủ đề là đang thảo luận về xe oto Vinfast, BMW, Mercedes

**Description**: Two passengers have a conversation discussing car brands (Vinfast, BMW, Mercedes). A virtual assistant listens and proactively provides relevant information when appropriate, without being explicitly asked.

**Key Features**:
- Multi-party conversation (2 passengers + 1 assistant)
- Proactive information sharing based on conversation context
- Knowledge base about car brands
- Natural turn-taking and interruption behavior

### Scenario 2: Memory-Based Low Fuel Alert
**Vietnamese**: Trong xe chỉ có tài xế. Memory ghi nhớ lại hằng ngày đúng 8h30 tài xế sẽ tìm cây xăng để đổ xăng. Tiếp tục, ngày hôm nay, sẽ có 1 trigger event là xe gần hết xăng, từ trigger đó, agent phải đưa ra gợi ý cây xăng gần nhất.

**Description**: Only the driver is in the vehicle. The assistant has learned that the driver refuels daily at 8:30 AM. When a low fuel warning triggers, the assistant proactively suggests the nearest gas station based on learned patterns and preferences.

**Key Features**:
- Memory-based pattern recognition
- Event-driven triggers (low fuel warning)
- Context-aware suggestions
- Temporal reasoning (time-based patterns)
- Location-aware recommendations

## Files

```
examples/
├── vehicle_assistant_scenario1.py   # Scenario 1: Passenger conversation
├── vehicle_assistant_scenario2.py   # Scenario 2: Memory-based alerts
├── vehicle_assistant_demo.py        # Combined demo runner
└── VEHICLE_ASSISTANT_README.md      # This file
```

## Requirements

1. **Python 3.8+**
2. **Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **OpenAI API Key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Optional Configuration**:
   ```bash
   # Customize models (optional)
   export COMPLETION_MODEL="gpt-4o"  # Default
   export EMBEDDING_MODEL="text-embedding-3-small"  # Default
   ```

## Usage

### Run Both Scenarios
```bash
python examples/vehicle_assistant_demo.py
```

### Run Individual Scenarios
```bash
# Scenario 1 only
python examples/vehicle_assistant_scenario1.py

# Scenario 2 only
python examples/vehicle_assistant_scenario2.py

# Or use the demo runner
python examples/vehicle_assistant_demo.py 1  # Scenario 1
python examples/vehicle_assistant_demo.py 2  # Scenario 2
```

### Verbose Mode
```bash
# With detailed thoughts (default)
python examples/vehicle_assistant_demo.py both true

# Without detailed thoughts (cleaner output)
python examples/vehicle_assistant_demo.py both false
```

## Implementation Details

### Proactivity Configuration

The assistant's proactive behavior is controlled by three parameters:

```python
proactivity_config = {
    'im_threshold': 3.2,        # Intrinsic Motivation threshold to speak
    'system1_prob': 0.3,        # Probability of quick intuitive responses
    'interrupt_threshold': 3.8  # Threshold to interrupt ongoing conversation
}
```

**Scenario 1 Configuration**:
- `im_threshold`: 3.2 (moderate - speaks when has relevant info)
- `system1_prob`: 0.3 (balanced between quick and deliberate)
- `interrupt_threshold`: 3.8 (interrupts for highly relevant info)

**Scenario 2 Configuration**:
- `im_threshold`: 2.5 (lower - more eager to help)
- `system1_prob`: 0.4 (balanced for routine matters)
- `interrupt_threshold`: 2.8 (proactive for important matters)

### Memory System

The assistant uses a dual-memory architecture:

1. **Long-term Memory**: Initialized with domain knowledge
   - Scenario 1: Information about car brands
   - Scenario 2: Driver patterns, gas stations, vehicle context

2. **Short-term Memory**: Recent conversation utterances
   - Automatically maintained during conversation
   - Used for context-aware responses

### Thought Process

The assistant follows a cognitive cycle:

1. **Event Reception**: Receives utterance or system event
2. **Memory Retrieval**: Recalls relevant information via saliency
3. **Thought Generation**:
   - System 1: Fast, intuitive thoughts
   - System 2: Deliberate, memory-based thoughts
4. **Evaluation**: Scores thoughts on intrinsic motivation (1-5)
5. **Selection**: Decides whether to speak based on proactivity config
6. **Articulation**: Converts internal thought to natural language

## Example Output

### Scenario 1 Output (abbreviated)
```
👤 Hương: Nam, what do you think about the new Vinfast cars?
👤 Nam: The Vinfast VF 8 looks pretty nice. But BMW or Mercedes are more reliable...
🤖 Vehicle Assistant: I can provide some context on these brands. Vinfast is Vietnam's
    first domestic car manufacturer, founded in 2017...
```

### Scenario 2 Output (abbreviated)
```
⏰ System: Time is 8:25 AM (5 minutes before usual refueling time)
🚨 Vehicle System Alert: LOW FUEL WARNING: Fuel level is at 15%
🤖 Smart Vehicle Assistant: I notice we're running low on fuel and it's approaching
    your usual 8:30 AM refueling time. The Petrolimex station on Nguyễn Huệ Street
    is 1.2 km away, about 3 minutes. Would you like directions?
```

## Technical Architecture

### Framework Components Used

1. **Agent Class** (`thoughtful_agents.models.Agent`)
   - Core cognitive loop
   - Thought generation and evaluation
   - Memory management

2. **Conversation Class** (`thoughtful_agents.models.Conversation`)
   - Multi-participant management
   - Event broadcasting
   - Turn tracking

3. **Turn-Taking Engine** (`thoughtful_agents.utils.turn_taking_engine`)
   - Predicts next speaker
   - Implements conversation analysis principles
   - Handles interruptions

4. **Memory System** (`thoughtful_agents.models.memory`)
   - Long-term knowledge storage
   - Saliency-based retrieval
   - Embedding-based similarity

5. **LLM Integration** (`thoughtful_agents.utils.llm_api`)
   - OpenAI API wrapper
   - Async completions and embeddings
   - Retry logic

### Event Flow

```
User/System Event
    ↓
Conversation.record_event()
    ↓
Conversation.interpret_event()  [Generate semantic meaning]
    ↓
Conversation.broadcast_event()  [Send to all agents in parallel]
    ↓
Agent.think()  [For each agent]
    ├─ Recalibrate memory saliency
    ├─ Generate System 1 thoughts (intuitive)
    ├─ Generate System 2 thoughts (deliberate)
    ├─ Evaluate thoughts (intrinsic motivation scores)
    └─ Store in thought reservoir
    ↓
decide_next_speaker_and_utterance()
    ├─ Check turn allocation
    ├─ Apply proactivity rules
    └─ Select highest-motivated speaker
    ↓
Agent.articulate_thought()  [Convert to natural language]
    ↓
Agent.send_message()  [Create new event]
    ↓
[Loop continues...]
```

## Customization

### Modify Knowledge Base

Edit the memory initialization strings in each scenario:

```python
# Scenario 1
assistant_knowledge = """I am a virtual assistant...
About Vinfast:
...your custom content here...
"""
assistant.initialize_memory(assistant_knowledge, by_paragraphs=True)
```

### Adjust Conversation Script

Modify the `conversation_script` list in Scenario 1:

```python
conversation_script = [
    {
        "speaker": passenger1,
        "message": "Your custom message here"
    },
    # Add more turns...
]
```

### Change Trigger Events

Modify the trigger event messages in Scenario 2:

```python
low_fuel_message = "⚠️ Your custom trigger message"
event = await driver.send_message(low_fuel_message, conversation)
```

### Tune Proactivity

Adjust the proactivity configuration:

```python
assistant = Agent(name="Assistant", proactivity_config={
    'im_threshold': 2.0,        # Lower = more proactive
    'system1_prob': 0.5,        # Higher = more intuitive
    'interrupt_threshold': 3.0  # Lower = interrupts more
})
```

## Research Foundation

This implementation is based on:

**Paper**: "Proactive Conversational Agents with Inner Thoughts" (CHI 2025)

**Key Concepts**:
- Dual-system thinking (System 1 + System 2)
- Intrinsic motivation for proactive behavior
- Saliency-based memory retrieval
- Turn-taking prediction

## Troubleshooting

### Issue: API Key Error
```
Error: OpenAI API key not set
```
**Solution**: Export your API key:
```bash
export OPENAI_API_KEY="sk-..."
```

### Issue: Import Error
```
ModuleNotFoundError: No module named 'thoughtful_agents'
```
**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Assistant Not Speaking
**Solution**: Lower the `im_threshold` in proactivity config to make the assistant more eager to participate.

### Issue: Too Many Interruptions
**Solution**: Increase the `interrupt_threshold` to reduce interruptions.

## Future Enhancements

Potential extensions to these scenarios:

1. **Navigation Integration**: Real-time route planning and traffic updates
2. **Voice Interface**: Speech-to-text and text-to-speech capabilities
3. **Multi-modal Input**: Process vehicle sensor data, GPS, etc.
4. **Persistent Memory**: Save and load learned patterns across sessions
5. **Personalization**: Adapt to individual driver preferences over time
6. **Multi-language**: Support for full Vietnamese language conversations
7. **Safety Features**: Drowsiness detection, emergency assistance
8. **Entertainment**: Music recommendations, podcast suggestions

## License

This implementation uses the Thoughtful Agents framework.
See the main repository LICENSE file for details.

## Contributing

To contribute improvements or new scenarios:

1. Follow the existing code structure and naming conventions
2. Include docstrings and comments
3. Test with various configurations
4. Update this README with new features

## Contact

For questions or issues, please refer to the main Thoughtful Agents repository.
