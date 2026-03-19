"""
Flask Web Demo for Proactive Conversational Agents with Inner Thoughts

This application provides a web interface to demonstrate the thoughtful agents framework
with a 3+1 column layout:
- Column 1: Long-term Memory (LTM)
- Column 2: Conversation (with multi-user support and system triggers)
- Column 3: Inner Thoughts
- Control Panel: User input and system trigger sections

Features:
- Multi-user conversation simulation (Driver, Passenger A, Passenger B)
- System triggers for vehicle events (low fuel, tire pressure, etc.)
- Real-time updates via Server-Sent Events (SSE)
- Proactive AI behavior based on triggers and context
"""

import asyncio
import json
import queue
import threading
from datetime import datetime
from flask import Flask, render_template, request, Response, jsonify
from typing import Dict, Optional, List

from thoughtful_agents.models import Agent, Human, Conversation
from thoughtful_agents.utils.turn_taking_engine import (
    decide_next_speaker_and_utterance,
    predict_turn_taking_type
)

app = Flask(__name__)

# Global state
event_queue = queue.Queue()
conversation = None
participants: Dict[str, any] = {}
assistant = None
demo_running = False


class UIAgent(Agent):
    """Extended Agent that emits events for UI updates"""

    async def send_message(self, message: str, conversation: Conversation):
        """Override to emit events when agent sends messages"""
        event = await super().send_message(message, conversation)
        emit_event('agent_message', {
            'speaker': self.name,
            'message': message,
            'turn': len(conversation.events)
        })
        return event

    async def generate_thoughts(self, conversation: Conversation, num_system1: int = 1, num_system2: int = 2):
        """Override to emit inner thoughts"""
        thoughts = await super().generate_thoughts(conversation, num_system1, num_system2)
        for thought in thoughts:
            # Emit thought with IM score after evaluation
            pass
        return thoughts

    async def evaluate_thoughts(self, thoughts: List, conversation: Conversation):
        """Override to emit thoughts with IM scores"""
        await super().evaluate_thoughts(thoughts, conversation)
        for thought in thoughts:
            if hasattr(thought, 'intrinsic_motivation_score') and thought.intrinsic_motivation_score is not None:
                emit_event('inner_thought', {
                    'turn': len(conversation.events),
                    'score': thought.intrinsic_motivation_score,
                    'content': thought.content,
                    'thought_type': thought.thought_type if hasattr(thought, 'thought_type') else 'unknown'
                })


class UIHuman(Human):
    """Extended Human that emits events for UI updates"""

    async def send_message(self, message: str, conversation: Conversation):
        """Override to emit events when human sends messages"""
        event = await super().send_message(message, conversation)
        emit_event('human_message', {
            'speaker': self.name,
            'message': message,
            'turn': len(conversation.events)
        })
        return event


def emit_event(event_type: str, data: dict):
    """Add an event to the queue for SSE streaming"""
    event_queue.put({
        'type': event_type,
        'data': data,
        'timestamp': datetime.now().isoformat()
    })


def initialize_scenario():
    """Initialize the vehicle assistant scenario with rich memory"""
    global conversation, participants, assistant, demo_running

    if demo_running:
        return

    demo_running = True

    # Create conversation context
    conversation = Conversation(
        context="A conversation in a vehicle with a driver and passengers. "
                "The vehicle has a smart assistant that monitors status and assists proactively. "
                "Current time is around 8:25 AM on a weekday morning."
    )

    # Create participants
    participants['driver'] = UIHuman(name="Minh (Driver)")
    participants['passenger_a'] = UIHuman(name="Passenger A")
    participants['passenger_b'] = UIHuman(name="Passenger B")

    # Create proactive assistant
    assistant = UIAgent(name="Smart Vehicle Assistant", proactivity_config={
        'im_threshold': 2.5,  # Lower threshold for more proactive behavior
        'system1_prob': 0.4,
        'interrupt_threshold': 2.8  # Will proactively interrupt for important matters
    })

    # Initialize assistant memory
    assistant_memory = """I am a smart vehicle assistant integrated into this vehicle.
I have been learning the driver Minh's patterns and routines over time.

Driver's Daily Patterns:
- Every day at 8:30 AM, driver Minh stops at a gas station to refuel
- Preferred gas stations are on the commute route (Nguyễn Huệ Street)
- Usually arrives at office around 9:00 AM after refueling
- Likes Vietnamese food, especially phở and bánh mì
- Prefers coffee shops with good wifi for working

Vehicle Information:
- Current location: Lê Lợi Street, heading downtown
- Typical fuel consumption: 8L/100km
- Tire pressure should be maintained at 32 PSI
- Regular service every 5000 km

Nearby Points of Interest:
1. Petrolimex Gas Station - Nguyễn Huệ St (1.2km, 3 min) - Most frequently used
2. Shell Station - Hai Bà Trưng St (0.8km, 2 min) - Closest option
3. Phở 24 - Lê Thánh Tôn St (0.5km) - Favorite breakfast spot
4. Highland Coffee - Đồng Khởi St (0.3km) - Regular stop for coffee

My Responsibilities:
- Monitor vehicle status and alert driver to important events
- Provide proactive suggestions based on learned patterns
- Help optimize the driver's daily routine and safety
- Suggest routes, restaurants, and services based on context and preferences
"""

    assistant.initialize_memory(assistant_memory, by_paragraphs=True)

    # Add participants to conversation
    conversation.add_participant(participants['driver'])
    conversation.add_participant(participants['passenger_a'])
    conversation.add_participant(participants['passenger_b'])
    conversation.add_participant(assistant)

    # Emit initialization events
    emit_event('scenario_started', {
        'participants': [p.name for p in conversation.participants]
    })

    emit_event('memory_initialized', {
        'count': len(assistant.memory_store.memories),
        'memories': [{'id': i+1, 'content': m.content[:200] + '...' if len(m.content) > 200 else m.content}
                     for i, m in enumerate(assistant.memory_store.memories[:10])]
    })


async def process_message_async(speaker_name: str, message: str, message_type: str = 'user'):
    """Process a message asynchronously"""
    global conversation, participants, assistant

    if not conversation:
        initialize_scenario()

    try:
        # Get the speaker
        if message_type == 'system':
            # System trigger - emit as system message
            emit_event('system_trigger', {
                'message': message,
                'turn': len(conversation.events) + 1
            })

            # Create a system event description for the agent to process
            system_event_description = f"System event: {message}"

            # Have the agent process this system event
            # The agent should generate thoughts about it
            await assistant.recalibrate_saliency_for_event(None)

            # Generate and evaluate thoughts about the system event
            thoughts = await assistant.generate_thoughts(conversation, num_system1=1, num_system2=2)
            await assistant.evaluate_thoughts(thoughts, conversation)

            # Determine if assistant should respond
            turn_allocation = await predict_turn_taking_type(conversation)
            next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)

            if next_speaker and next_speaker.name == assistant.name and utterance:
                await assistant.send_message(utterance, conversation)
                await conversation.broadcast_event(conversation.events[-1])

        else:
            # Regular user message
            speaker = participants.get(speaker_name.lower().replace(' ', '_'))
            if not speaker:
                speaker = participants['driver']  # Default to driver

            # Send message
            event = await speaker.send_message(message, conversation)

            # Predict turn taking and broadcast
            turn_allocation = await predict_turn_taking_type(conversation)
            await conversation.broadcast_event(event)

            # Determine next speaker
            next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)

            if next_speaker and utterance:
                await next_speaker.send_message(utterance, conversation)
                turn_allocation = await predict_turn_taking_type(conversation)
                await conversation.broadcast_event(conversation.events[-1])

    except Exception as e:
        emit_event('error', {'message': str(e)})


def run_async_task(coro):
    """Run an async coroutine in a new event loop"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(coro)
    finally:
        loop.close()


async def run_demo_scenario():
    """Run the initial demo scenario"""
    global conversation, participants, assistant

    initialize_scenario()

    # Wait a moment for initialization
    await asyncio.sleep(1)

    # Simulate a few initial interactions
    emit_event('system_message', {
        'message': '=== Demo Scenario Starting ===',
        'turn': 0
    })

    # Scenario 1: Passengers discuss cars
    await asyncio.sleep(1)
    await process_message_async('passenger_a',
                                'Hey, have you seen the new Vinfast cars? They look pretty impressive!',
                                'user')

    await asyncio.sleep(2)
    await process_message_async('passenger_b',
                                'Yeah, I heard they\'re getting popular. How do they compare to BMW or Mercedes?',
                                'user')

    # Wait for natural conversation flow
    await asyncio.sleep(3)

    # Scenario 2: Low fuel trigger
    emit_event('system_message', {
        'message': '=== Triggering Low Fuel Event ===',
        'turn': len(conversation.events) + 1
    })

    await asyncio.sleep(1)
    await process_message_async('system',
                                '{"event": "low_fuel", "level": "15%", "range": "45km"}',
                                'system')

    emit_event('scenario_completed', {
        'total_turns': len(conversation.events) if conversation else 0
    })


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start_demo():
    """Start the demo scenario"""
    thread = threading.Thread(target=run_async_task, args=(run_demo_scenario(),))
    thread.daemon = True
    thread.start()

    return jsonify({'status': 'started'})


@app.route('/trigger', methods=['POST'])
def trigger_event():
    """Handle custom triggers from the UI"""
    data = request.json
    message = data.get('message', '')
    speaker = data.get('speaker', 'driver')
    trigger_type = data.get('type', 'user')  # 'user' or 'system'

    thread = threading.Thread(
        target=run_async_task,
        args=(process_message_async(speaker, message, trigger_type),)
    )
    thread.daemon = True
    thread.start()

    return jsonify({'status': 'triggered'})


@app.route('/state', methods=['GET'])
def get_state():
    """Get the current demo state"""
    global conversation, participants, assistant

    return jsonify({
        'running': demo_running,
        'participants': [p.name for p in conversation.participants] if conversation else [],
        'memory_count': len(assistant.memory_store.memories) if assistant else 0,
        'turn_count': len(conversation.events) if conversation else 0
    })


@app.route('/events')
def stream_events():
    """Server-Sent Events endpoint for real-time updates"""

    def generate():
        """Generate SSE stream"""
        try:
            while True:
                try:
                    event = event_queue.get(timeout=30)
                    yield f"data: {json.dumps(event)}\n\n"
                except queue.Empty:
                    # Send heartbeat to keep connection alive
                    yield f": heartbeat\n\n"
        except GeneratorExit:
            pass

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    print("Starting Thoughtful Agents Web Demo...")
    print("Open http://localhost:5000 in your browser")
    print("\nFeatures:")
    print("- Multi-user conversation (Driver, Passenger A, Passenger B)")
    print("- System triggers for vehicle events")
    print("- Real-time Inner Thoughts visualization")
    print("- Long-term Memory display")
    print("\nPress Ctrl+C to stop")

    app.run(debug=True, threaded=True, port=5000)
