"""
Flask Web UI for Thoughtful Agents Demo

This application provides a web-based visualization of the thoughtful agents framework,
displaying memory, conversation, and inner thoughts in real-time.
"""

import asyncio
import json
import queue
import threading
from datetime import datetime
from flask import Flask, render_template, request, Response, jsonify
from typing import Optional, Dict, Any

# Import the vehicle assistant scenario
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from examples.vehicle_assistant_scenario2 import run_scenario2
from thoughtful_agents.models import (
    Agent,
    Human,
    Conversation,
)
from thoughtful_agents.utils.turn_taking_engine import decide_next_speaker_and_utterance, predict_turn_taking_type
from thoughtful_agents.utils.timing import TimingTracker, set_timing_tracker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thoughtful-agents-demo'

# Global state for the demo
demo_state = {
    'conversation': None,
    'driver': None,
    'assistant': None,
    'event_queue': queue.Queue(),
    'is_running': False,
    'lock': threading.Lock()
}


def emit_event(event_type: str, data: Dict[str, Any]):
    """Emit an event to all connected clients via SSE."""
    event_data = {
        'type': event_type,
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    demo_state['event_queue'].put(event_data)


class UIAgent(Agent):
    """Extended Agent that emits UI events for thoughts and messages."""

    async def send_message(self, content: str, conversation):
        """Override to emit UI event before sending message."""
        emit_event('agent_message', {
            'speaker': self.name,
            'content': content,
            'turn': conversation.turn_number
        })
        return await super().send_message(content, conversation)

    def add_thought(self, thought):
        """Override to emit UI event when thought is added."""
        super().add_thought(thought)
        emit_event('inner_thought', {
            'agent': self.name,
            'thought': thought.content,
            'intrinsic_motivation': thought.intrinsic_motivation['score'],
            'turn': thought.generated_turn
        })


class UIHuman(Human):
    """Extended Human that emits UI events for messages."""

    async def send_message(self, content: str, conversation):
        """Override to emit UI event before sending message."""
        emit_event('human_message', {
            'speaker': self.name,
            'content': content,
            'turn': conversation.turn_number
        })
        return await super().send_message(content, conversation)


async def run_demo_scenario():
    """Run the vehicle assistant scenario with UI updates."""
    tracker = TimingTracker()
    set_timing_tracker(tracker)

    current_time_context = "8:25 AM"

    # Create conversation
    conversation = Conversation(
        context=f"A conversation in a vehicle with only the driver present. "
                f"Current time is {current_time_context}. The vehicle has a virtual assistant "
                f"that monitors the vehicle status and assists the driver. The assistant has "
                f"learned the driver's patterns and behaviors over time."
    )

    # Create participants using UI-aware classes
    driver = UIHuman(name="Minh")

    assistant = UIAgent(name="Smart Vehicle Assistant", proactivity_config={
        'im_threshold': 2.5,
        'system1_prob': 0.4,
        'interrupt_threshold': 2.8
    })

    # Initialize assistant memory
    assistant_memory = """I am a smart vehicle assistant integrated into this vehicle.
I have been learning the driver Minh's patterns and routines over time.

Driver's Daily Patterns (Learned from Memory):
Every day at exactly 8:30 AM, driver Minh stops at a gas station to refuel the vehicle.
This is a consistent daily routine that has been observed for many weeks.
Minh prefers gas stations that are on the regular commute route.
Minh usually goes to work after refueling, arriving at the office around 9:00 AM.
The typical refueling location is on Nguyễn Huệ Street.

Current Vehicle Information:
Vehicle location: Currently on Lê Lợi Street, heading towards downtown.
Time: 8:25 AM - It's almost time for the usual 8:30 AM refueling routine.
Fuel level: Will be updated based on sensor data.

Nearby Gas Stations:
1. Petrolimex Station - Nguyễn Huệ St (1.2 km, 3 minutes) - On usual route, most frequently used
2. Shell Station - Hai Bà Trưng St (0.8 km, 2 minutes) - Slightly off route but closest
3. Total Station - Lê Duẩn St (1.5 km, 4 minutes) - On alternative route to office
4. Chevron Station - Trần Hưng Đạo St (2.0 km, 5 minutes) - Further but has good amenities

My Responsibilities:
Monitor vehicle status and alert driver to important events.
Provide proactive suggestions based on learned patterns.
Help optimize the driver's daily routine.
Ensure safety by alerting about low fuel, maintenance needs, etc.
Suggest optimal routes and timing for errands.

Current Context:
It's 8:25 AM, close to Minh's usual 8:30 AM refueling time.
I should be prepared to suggest the gas station when appropriate.
I need to monitor fuel level and provide timely suggestions."""

    assistant.initialize_memory(assistant_memory, by_paragraphs=True)

    # Emit memory initialization event
    emit_event('memory_initialized', {
        'agent': assistant.name,
        'memory_items': [mem.content for mem in assistant.memory]
    })

    # Add participants
    conversation.add_participant(driver)
    conversation.add_participant(assistant)

    # Store in global state
    demo_state['conversation'] = conversation
    demo_state['driver'] = driver
    demo_state['assistant'] = assistant

    emit_event('scenario_started', {
        'scenario': 'Vehicle Assistant - Low Fuel Memory Pattern',
        'time': current_time_context,
        'participants': [driver.name, assistant.name]
    })

    # Turn 1: Morning greeting
    await asyncio.sleep(1)
    greeting_prompt = f"It's {current_time_context}, close to the driver's usual 8:30 AM refueling time."
    event = await driver.send_message(greeting_prompt, conversation)

    emit_event('system_message', {
        'content': f"⏰ Time is {current_time_context} (5 minutes before usual refueling time)",
        'turn': conversation.turn_number
    })

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    # Emit thoughts
    for thought in assistant.thought_reservoir.thoughts:
        if thought.generated_turn == conversation.turn_number:
            emit_event('inner_thought', {
                'agent': assistant.name,
                'thought': thought.content,
                'intrinsic_motivation': thought.intrinsic_motivation['score'],
                'turn': thought.generated_turn
            })

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)
        await predict_turn_taking_type(conversation)
        await conversation.broadcast_event(event)

    # Turn 2: Low fuel warning
    await asyncio.sleep(2)
    low_fuel_message = (
        "⚠️ LOW FUEL WARNING: Fuel level is at 15%. "
        "Approximately 50 km remaining range. Please refuel soon."
    )
    event = await driver.send_message(low_fuel_message, conversation)

    emit_event('system_message', {
        'content': f"🚨 Vehicle System Alert: {low_fuel_message}",
        'turn': conversation.turn_number
    })

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    # Emit thoughts
    for thought in assistant.thought_reservoir.thoughts:
        if thought.generated_turn == conversation.turn_number:
            emit_event('inner_thought', {
                'agent': assistant.name,
                'thought': thought.content,
                'intrinsic_motivation': thought.intrinsic_motivation['score'],
                'turn': thought.generated_turn
            })

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)
        await predict_turn_taking_type(conversation)
        await conversation.broadcast_event(event)

    # Turn 3: Driver response
    await asyncio.sleep(2)
    driver_response = (
        "Cảm ơn! Đúng rồi, đã gần đến giờ đổ xăng rồi. "
        "Mình sẽ đi đến trạm Petrolimex trên đường Nguyễn Huệ nhé. "
        "(Thanks! That's right, it's almost time to refuel. "
        "I'll go to the Petrolimex station on Nguyễn Huệ Street.)"
    )
    event = await driver.send_message(driver_response, conversation)

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    # Emit thoughts
    for thought in assistant.thought_reservoir.thoughts:
        if thought.generated_turn == conversation.turn_number:
            emit_event('inner_thought', {
                'agent': assistant.name,
                'thought': thought.content,
                'intrinsic_motivation': thought.intrinsic_motivation['score'],
                'turn': thought.generated_turn
            })

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)
        await predict_turn_taking_type(conversation)
        await conversation.broadcast_event(event)

    # Turn 4: Navigation
    await asyncio.sleep(2)
    nav_prompt = "The driver has decided to go to Petrolimex on Nguyễn Huệ Street."
    event = await driver.send_message(nav_prompt, conversation)

    emit_event('system_message', {
        'content': "📍 Driver heading to Petrolimex station",
        'turn': conversation.turn_number
    })

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    # Emit thoughts
    for thought in assistant.thought_reservoir.thoughts:
        if thought.generated_turn == conversation.turn_number:
            emit_event('inner_thought', {
                'agent': assistant.name,
                'thought': thought.content,
                'intrinsic_motivation': thought.intrinsic_motivation['score'],
                'turn': thought.generated_turn
            })

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)

    emit_event('scenario_completed', {
        'total_turns': len(conversation.event_history),
        'assistant_turns': sum(1 for e in conversation.event_history if e.participant_name == assistant.name)
    })

    demo_state['is_running'] = False


def run_scenario_thread():
    """Run the scenario in a separate thread with its own event loop."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_demo_scenario())
    finally:
        loop.close()


@app.route('/')
def index():
    """Render the main demo page."""
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start_demo():
    """Start the demo scenario."""
    with demo_state['lock']:
        if demo_state['is_running']:
            return jsonify({'error': 'Demo is already running'}), 400

        demo_state['is_running'] = True
        # Clear the event queue
        while not demo_state['event_queue'].empty():
            demo_state['event_queue'].get()

        # Start the scenario in a separate thread
        thread = threading.Thread(target=run_scenario_thread)
        thread.daemon = True
        thread.start()

        return jsonify({'status': 'started'})


@app.route('/events')
def events():
    """Server-Sent Events endpoint for real-time updates."""
    def generate():
        while True:
            try:
                # Wait for an event with timeout
                event = demo_state['event_queue'].get(timeout=30)
                yield f"data: {json.dumps(event)}\n\n"
            except queue.Empty:
                # Send keep-alive comment
                yield ": keep-alive\n\n"

    return Response(generate(), mimetype='text/event-stream')


@app.route('/trigger', methods=['POST'])
def trigger_event():
    """Manually trigger a custom event in the conversation."""
    data = request.json
    message = data.get('message', '')

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    if not demo_state['conversation'] or not demo_state['driver']:
        return jsonify({'error': 'Demo not initialized'}), 400

    # Run the trigger in a separate thread
    def send_trigger():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            conversation = demo_state['conversation']
            driver = demo_state['driver']
            assistant = demo_state['assistant']

            async def process_trigger():
                event = await driver.send_message(message, conversation)
                await predict_turn_taking_type(conversation)
                await conversation.broadcast_event(event)

                # Emit thoughts
                for thought in assistant.thought_reservoir.thoughts:
                    if thought.generated_turn == conversation.turn_number:
                        emit_event('inner_thought', {
                            'agent': assistant.name,
                            'thought': thought.content,
                            'intrinsic_motivation': thought.intrinsic_motivation['score'],
                            'turn': thought.generated_turn
                        })

                next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
                if next_speaker and next_speaker.name == assistant.name:
                    event = await assistant.send_message(utterance, conversation)
                    await predict_turn_taking_type(conversation)
                    await conversation.broadcast_event(event)

            loop.run_until_complete(process_trigger())
        finally:
            loop.close()

    thread = threading.Thread(target=send_trigger)
    thread.daemon = True
    thread.start()

    return jsonify({'status': 'triggered'})


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚗 Thoughtful Agents Web Demo 🚗")
    print("="*70)
    print("\nStarting Flask server...")
    print("Open http://localhost:5000 in your browser to view the demo\n")

    app.run(debug=True, threaded=True, port=5000)
