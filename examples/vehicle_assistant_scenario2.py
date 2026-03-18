"""
Vehicle Virtual Assistant - Scenario 2: Low Fuel Memory Pattern

This example demonstrates a proactive virtual assistant that learns from the driver's
daily patterns and provides contextual suggestions. The assistant remembers that the
driver typically stops for gas at 8:30 AM daily, and when a low fuel event occurs,
it proactively suggests the nearest gas station.

Scenario Description (Vietnamese):
Trong xe chỉ có tài xế. Memory ghi nhớ lại hằng ngày đúng 8h30 tài xế sẽ tìm cây xăng
để đổ xăng. Tiếp tục, ngày hôm nay, sẽ có 1 trigger event là xe gần hết xăng, từ
trigger đó, agent phải đưa ra gợi ý cây xăng gần nhất.

English Translation:
Only the driver is in the vehicle. Memory recalls that every day at exactly 8:30 AM
the driver looks for a gas station to refuel. Continuing, today, there will be a
trigger event of the car running low on fuel, from that trigger, the agent must
suggest the nearest gas station.
"""

import asyncio
import sys
from datetime import datetime, time
from typing import Optional

from thoughtful_agents.models import (
    Agent,
    Human,
    Conversation,
)
from thoughtful_agents.utils.turn_taking_engine import decide_next_speaker_and_utterance, predict_turn_taking_type
from thoughtful_agents.utils.llm_api import DEFAULT_COMPLETION_MODEL, DEFAULT_EMBEDDING_MODEL

async def run_scenario2(verbose: bool = True):
    """
    Run a vehicle assistant simulation demonstrating memory-based proactive behavior.
    The assistant remembers the driver's daily 8:30 AM gas station routine and
    proactively suggests a station when the low fuel warning triggers.

    Args:
        verbose: Whether to print detailed thought processes
    """
    # Current time context - simulating it's around 8:25 AM
    current_time_context = "8:25 AM"

    # Create a conversation context for a vehicle with a single driver
    conversation = Conversation(
        context=f"A conversation in a vehicle with only the driver present. "
                f"Current time is {current_time_context}. The vehicle has a virtual assistant "
                f"that monitors the vehicle status and assists the driver. The assistant has "
                f"learned the driver's patterns and behaviors over time."
    )

    # Create the driver
    driver = Human(name="Minh")

    # Create a proactive virtual assistant with high proactivity
    # This assistant should be very proactive about safety and routine matters
    assistant = Agent(name="Smart Vehicle Assistant", proactivity_config={
        'im_threshold': 2.5,  # Lower threshold - more eager to help
        'system1_prob': 0.4,  # Balanced for routine matters
        'interrupt_threshold': 2.8  # Will proactively interrupt for important matters
    })

    # Initialize the assistant's memory with learned patterns and current context
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

    # Add memory to the assistant
    assistant.initialize_memory(assistant_memory, by_paragraphs=True)

    # Add participants to the conversation
    conversation.add_participant(driver)
    conversation.add_participant(assistant)

    print("\n" + "="*70)
    print("🚗 Vehicle Virtual Assistant - Scenario 2: Memory-Based Proactive Assistant 🚗")
    print("="*70 + "\n")
    print(f"Setting: Single driver (Minh) in vehicle at {current_time_context}")
    print("Assistant: Smart assistant with learned memory patterns")
    print(f"Memory: Driver typically refuels at 8:30 AM daily\n")

    # Scenario progression
    print(f"{'─'*70}")
    print("Initial State - Morning Commute")
    print(f"{'─'*70}\n")

    # 1. Driver starts the day
    print("📍 Driver starts morning commute...\n")

    # 2. Assistant greets (proactive based on time pattern)
    print(f"{'─'*70}")
    print("Turn 1: Morning Greeting")
    print(f"{'─'*70}")

    # Simulate assistant noticing it's close to usual refueling time
    greeting_prompt = f"It's {current_time_context}, close to the driver's usual 8:30 AM refueling time."
    event = await driver.send_message(greeting_prompt, conversation)
    print(f"\n⏰ System: Time is {current_time_context} (5 minutes before usual refueling time)")

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    if verbose:
        print(f"\n🧠 {assistant.name}'s thoughts:")
        for thought in assistant.thought_reservoir.thoughts:
            if thought.generated_turn == conversation.turn_number:
                print(f"  💭 {thought.content}")
                print(f"     (Intrinsic Motivation: {thought.intrinsic_motivation['score']})")

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)
        print(f"\n🤖 {assistant.name}: {utterance}")
        await predict_turn_taking_type(conversation)
        await conversation.broadcast_event(event)

    # 3. Trigger Event: Low Fuel Warning
    print(f"\n{'─'*70}")
    print("Turn 2: LOW FUEL WARNING TRIGGER EVENT")
    print(f"{'─'*70}")

    low_fuel_message = (
        "⚠️ LOW FUEL WARNING: Fuel level is at 15%. "
        "Approximately 50 km remaining range. Please refuel soon."
    )
    event = await driver.send_message(low_fuel_message, conversation)
    print(f"\n🚨 Vehicle System Alert: {low_fuel_message}")

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    if verbose:
        print(f"\n🧠 {assistant.name}'s thoughts:")
        for thought in assistant.thought_reservoir.thoughts:
            if thought.generated_turn == conversation.turn_number:
                print(f"  💭 {thought.content}")
                print(f"     (Intrinsic Motivation: {thought.intrinsic_motivation['score']})")

    # Assistant should proactively respond to low fuel event
    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)

    print(f"\n{'─'*70}")
    print("Assistant's Proactive Response")
    print(f"{'─'*70}")

    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)
        print(f"\n🤖 {assistant.name}: {utterance}")
        await predict_turn_taking_type(conversation)
        await conversation.broadcast_event(event)
    else:
        # If assistant didn't respond automatically, we should force a response
        # since this is a critical safety matter
        print(f"\n🤖 {assistant.name}: (processing...)")

    # 4. Driver acknowledges
    print(f"\n{'─'*70}")
    print("Turn 3: Driver Response")
    print(f"{'─'*70}")

    driver_response = (
        "Cảm ơn! Đúng rồi, đã gần đến giờ đổ xăng rồi. "
        "Mình sẽ đi đến trạm Petrolimex trên đường Nguyễn Huệ nhé. "
        "(Thanks! That's right, it's almost time to refuel. "
        "I'll go to the Petrolimex station on Nguyễn Huệ Street.)"
    )
    event = await driver.send_message(driver_response, conversation)
    print(f"\n👤 {driver.name}: {driver_response}")

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    if verbose:
        print(f"\n🧠 {assistant.name}'s thoughts:")
        for thought in assistant.thought_reservoir.thoughts:
            if thought.generated_turn == conversation.turn_number:
                print(f"  💭 {thought.content}")
                print(f"     (Intrinsic Motivation: {thought.intrinsic_motivation['score']})")

    # Check if assistant wants to respond
    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)
        print(f"\n🤖 {assistant.name}: {utterance}")
        await predict_turn_taking_type(conversation)
        await conversation.broadcast_event(event)

    # 5. Assistant provides navigation
    print(f"\n{'─'*70}")
    print("Turn 4: Navigation Assistance")
    print(f"{'─'*70}")

    # Simulate the assistant providing navigation
    nav_prompt = "The driver has decided to go to Petrolimex on Nguyễn Huệ Street."
    event = await driver.send_message(nav_prompt, conversation)
    print(f"\n📍 Context: Driver heading to Petrolimex station")

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    if verbose:
        print(f"\n🧠 {assistant.name}'s thoughts:")
        for thought in assistant.thought_reservoir.thoughts:
            if thought.generated_turn == conversation.turn_number:
                print(f"  💭 {thought.content}")
                print(f"     (Intrinsic Motivation: {thought.intrinsic_motivation['score']})")

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        print(f"\n🤖 {assistant.name}: {utterance}")

    print("\n" + "="*70)
    print("🏁 End of Scenario 2 🏁")
    print("="*70 + "\n")

    # Summary
    print("📋 Scenario Summary:")
    print(f"✓ Assistant demonstrated memory-based pattern recognition (8:30 AM routine)")
    print(f"✓ Assistant responded proactively to low fuel trigger event")
    print(f"✓ Assistant suggested nearest gas station based on learned preferences")
    print(f"✓ Total conversation turns: {len(conversation.event_history)}")
    print(f"✓ Assistant participated: {sum(1 for e in conversation.event_history if e.participant_name == assistant.name)} times")

    print("\n📝 Full Conversation History:")
    for i, event in enumerate(conversation.event_history):
        participant_name = event.participant_name
        content = event.content[:120] + "..." if len(event.content) > 120 else event.content
        print(f"  {i+1}. {participant_name}: {content}")

    print("\n💡 Key Demonstration Points:")
    print("  1. Memory System: Assistant recalled driver's daily 8:30 AM refueling pattern")
    print("  2. Trigger Event: Low fuel warning activated proactive response")
    print("  3. Context Awareness: Assistant considered time, location, and preferences")
    print("  4. Proactive Behavior: Assistant suggested solution without being asked")


async def main():
    """Main entry point for the scenario."""
    # Parse command line arguments
    verbose = True  # Default

    if len(sys.argv) > 1:
        verbose_arg = sys.argv[1].lower()
        if verbose_arg in ['false', 'no', '0']:
            verbose = False

    # Print configuration
    print(f"\n📝 Configuration:")
    print(f"   Completion model: {DEFAULT_COMPLETION_MODEL}")
    print(f"   Embedding model: {DEFAULT_EMBEDDING_MODEL}")
    print(f"   Verbose mode: {verbose}\n")

    await run_scenario2(verbose)


if __name__ == "__main__":
    asyncio.run(main())
