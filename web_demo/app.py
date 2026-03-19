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

    # Initialize assistant memory with extensive knowledge base
    assistant_memory = """I am a smart vehicle assistant integrated into this vehicle.
I have been learning the driver Minh's patterns and routines over time.
My purpose is to provide helpful information and proactive assistance to make the driving experience safer, more efficient, and more enjoyable.

Driver's Daily Patterns and Routines:
Every day at 8:30 AM, driver Minh stops at a gas station to refuel the vehicle.
This is a consistent daily routine that has been observed for many weeks.
Minh prefers gas stations that are on the regular commute route, especially on Nguyễn Huệ Street.
After refueling, Minh usually arrives at the office around 9:00 AM.
The morning commute typically takes about 25-30 minutes depending on traffic conditions.

Driver's Food Preferences:
Minh loves Vietnamese cuisine, especially traditional dishes like phở and bánh mì.
For breakfast, Minh frequently stops at Phở 24 restaurant on Lê Thánh Tôn Street.
Minh enjoys bánh mì sandwiches from the vendor near the office building.
For lunch, Minh prefers restaurants serving com tam (broken rice) and bún chả.
Minh occasionally enjoys international cuisines like Japanese sushi and Italian pasta.
Dietary preferences include avoiding overly spicy food and preferring fresh ingredients.

Driver's Coffee and Work Habits:
Minh is a coffee enthusiast and prefers Highland Coffee shops with good wifi connectivity.
The Highland Coffee on Đồng Khởi Street is a regular stop for working remotely.
Minh usually orders cappuccino or Vietnamese iced coffee (cà phê sữa đá).
When working from cafes, Minh prefers quiet corners with power outlets available.
Minh often has virtual meetings in the morning between 10:00 AM and 11:30 AM.

Vehicle Technical Information:
The vehicle is a modern sedan with advanced driver assistance features.
Current location is typically around Lê Lợi Street when heading downtown in the morning.
The vehicle has an average fuel consumption rate of 8 liters per 100 kilometers.
Fuel tank capacity is 50 liters, providing approximately 600 km range when full.
Tire pressure should be maintained at 32 PSI for optimal performance and safety.
Regular maintenance service is scheduled every 5000 kilometers or 6 months.
Last service was performed 3000 kilometers ago at the authorized service center.

Vehicle Current Status and Monitoring:
Current odometer reading is approximately 28,500 kilometers.
Next scheduled maintenance is due at 30,000 kilometers in about 1500 km.
Tire pressure sensors are functioning normally across all four tires.
Engine oil level is adequate and within the normal operating range.
All safety systems including ABS, ESC, and airbags are operational.
The vehicle's navigation system is connected and receiving real-time traffic updates.

Nearby Gas Stations and Fuel Information:
Petrolimex Gas Station on Nguyễn Huệ Street is 1.2 kilometers away, approximately 3 minutes drive.
This is the most frequently used gas station by driver Minh due to its convenient location.
Petrolimex offers high-quality fuel and has a convenience store and restroom facilities.
Shell Station on Hai Bà Trưng Street is 0.8 kilometers away, approximately 2 minutes drive.
Shell Station is the closest option and offers premium fuel grades with cleaning additives.
Total Station on Lê Duẩn Street is 1.5 kilometers away, approximately 4 minutes drive.
Total Station is on an alternative route to the office and has good service quality.

Nearby Restaurants and Dining Options:
Phở 24 on Lê Thánh Tôn Street is 0.5 kilometers away and is Minh's favorite breakfast spot.
Phở 24 serves authentic Vietnamese beef noodle soup and is open from 6:00 AM to 10:00 PM.
Com Tam Moc restaurant on Pasteur Street serves excellent broken rice dishes for lunch.
Bánh Mì Huynh Hoa on Lê Thị Riêng Street is famous for delicious Vietnamese sandwiches.
Sushi Hokkaido on Nguyễn Huệ Street offers fresh Japanese cuisine for special occasions.
Pizza 4P's on Lê Thánh Tôn Street serves artisanal pizzas and is good for dinner meetings.

Coffee Shops and Work-Friendly Locations:
Highland Coffee on Đồng Khởi Street is 0.3 kilometers away and is Minh's regular spot.
This location has excellent wifi, comfortable seating, and power outlets at every table.
The Coffee House on Nguyễn Trãi Street offers a quiet atmosphere and good workspace.
Starbucks Reserve on Đồng Khởi Street has a premium experience with specialty drinks.
Trung Nguyên E-Coffee on Lê Lợi Street serves traditional Vietnamese coffee in a modern setting.

Traffic Patterns and Route Information:
Morning rush hour typically occurs between 7:00 AM and 9:00 AM with heavy traffic.
Lê Lợi Street often experiences congestion during peak hours, adding 10-15 minutes to travel time.
Alternative routes via Hai Bà Trưng Street or Trần Hưng Đạo Street can save time during rush hour.
Traffic is usually lighter after 9:30 AM when most commuters have reached their destinations.
Evening rush hour begins around 5:00 PM and continues until 7:00 PM.
Weather conditions such as heavy rain can significantly impact traffic flow and visibility.

Safety and Emergency Information:
The nearest hospital with emergency services is located on Nguyễn Thị Minh Khai Street, 2.5 km away.
Emergency contact numbers are programmed into the vehicle's emergency call system.
The vehicle has automatic collision notification that alerts emergency services if airbags deploy.
Roadside assistance is available 24/7 through the vehicle manufacturer's service hotline.
In case of breakdown, the vehicle can be towed to the authorized service center.

Weather and Environmental Conditions:
Current weather forecast indicates clear skies with temperatures around 28-32 degrees Celsius.
UV index is moderate to high, requiring air conditioning for comfortable cabin temperature.
Air quality index (AQI) is typically moderate in the morning, improving during midday.
During rainy season (May to November), weather can change rapidly with afternoon thunderstorms.
Monsoon rains can cause localized flooding on certain streets, requiring route adjustments.

Points of Interest and Landmarks:
Ben Thanh Market is a major landmark located approximately 1 kilometer from the usual route.
Notre-Dame Cathedral and Central Post Office are popular tourist attractions nearby.
Nguyen Hue Walking Street is a pedestrian area perfect for evening strolls.
Saigon Opera House hosts cultural performances and is located in District 1.
Bitexco Financial Tower offers observation deck with panoramic city views.

My Capabilities and Responsibilities:
Monitor all vehicle systems continuously including fuel level, tire pressure, engine status, and safety systems.
Provide proactive alerts and suggestions based on learned patterns and current context.
Offer route optimization recommendations considering traffic, weather, and driver preferences.
Suggest appropriate times for refueling, maintenance, and rest stops during longer journeys.
Recommend dining options based on time of day, location, dietary preferences, and past choices.
Assist with finding parking locations near destinations and estimate parking availability.
Provide information about nearby amenities including ATMs, pharmacies, and convenience stores.
Help optimize the driver's daily routine for maximum efficiency and minimal stress.
Ensure driver safety by monitoring conditions and providing timely warnings and suggestions.
Learn from driver behaviors and preferences to provide increasingly personalized assistance."""

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
                     for i, m in enumerate(assistant.memory_store.memories)]
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
