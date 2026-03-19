"""
Vehicle Virtual Assistant - Extended Scenario with Rich Content

This is an extended version of vehicle_assistant_scenario2 with additional features:
- Restaurant suggestions based on preferences
- Museum and attraction information
- More varied conversation scenarios
- Enhanced memory with detailed user preferences
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
from thoughtful_agents.utils.timing import TimingTracker, set_timing_tracker


async def run_extended_scenario(verbose: bool = True):
    """
    Run an extended vehicle assistant simulation with rich content including
    restaurant suggestions, museum information, and varied conversation scenarios.

    Args:
        verbose: Whether to print detailed thought processes
    """
    tracker = TimingTracker()
    set_timing_tracker(tracker)

    current_time_context = "8:25 AM"

    # Create conversation with rich context
    conversation = Conversation(
        context=f"A conversation in a vehicle with only the driver present. "
                f"Current time is {current_time_context}. The vehicle has a smart virtual assistant "
                f"that monitors vehicle status, assists with navigation, provides recommendations, "
                f"and learns from the driver's preferences and patterns over time."
    )

    driver = Human(name="Minh")

    # Create assistant with proactive configuration
    assistant = Agent(name="Smart Vehicle Assistant", proactivity_config={
        'im_threshold': 2.5,
        'system1_prob': 0.4,
        'interrupt_threshold': 2.8
    })

    # Initialize with rich, detailed memory
    assistant_memory = """I am a smart vehicle assistant with comprehensive knowledge of the driver's preferences and patterns.

DRIVER PROFILE - MINH:
Personal Information:
- Occupation: Software engineer at a tech company
- Lives in District 1, works in District 3, Ho Chi Minh City
- Daily commute: 20-25 minutes
- Languages: Vietnamese (native), English (fluent)

Daily Routines:
- Wakes up: 7:00 AM on weekdays
- Leaves for work: 8:00 AM typically
- Refueling routine: Every day at exactly 8:30 AM at gas stations
- Lunch time: Usually 12:00-1:00 PM
- Returns home: Around 6:30 PM
- Weekend activities: Museums, parks, dining out with family

FOOD & DINING PREFERENCES:
Favorite Cuisines:
1. Vietnamese (Phở, Bún Bò Huế, Bánh Mì) - Strongly preferred
2. Japanese (Sushi, Ramen) - Frequently chosen
3. Italian (Pasta, Pizza) - Occasional
4. Korean (BBQ, Bibimbap) - When with friends

Dietary Restrictions:
- No shellfish allergies
- Prefers less spicy food (mild to medium heat)
- Enjoys vegetarian options occasionally
- Avoids overly sweet desserts

Restaurant Preferences:
- Price range: Mid-range to upscale (200,000-500,000 VND per person)
- Atmosphere: Clean, modern, with parking
- Location: Within 5km of regular routes
- Must have good reviews (4+ stars)
- Prefers places with air conditioning

Favorite Restaurants:
1. "Phở Hòa Pasteur" - Nguyễn Công Trứ St - Best phở, visited monthly
2. "Sushi Hokkaido" - Lê Lợi St - Fresh sushi, special occasions
3. "Cơm Niêu Singapore" - Hai Bà Trưng St - Comfort food, weekly visits
4. "Bún Bò Huế An Nam" - Trần Hưng Đạo St - Authentic, weekend favorite

Recent Dining History:
- Last week: Had phở at Phở Hòa Pasteur (loved it)
- 3 days ago: Tried new Italian place, wasn't impressed
- Mentioned wanting to try: More Japanese restaurants, vegetarian options

CULTURAL & ENTERTAINMENT PREFERENCES:
Museums & Attractions:
Visited Recently:
- War Remnants Museum - Found it informative and moving
- Ho Chi Minh City Museum - Interested in local history
- Fine Arts Museum - Appreciates traditional Vietnamese art

Interests:
- Vietnamese history and culture (strong interest)
- Modern art and photography (moderate interest)
- Science and technology exhibitions (high interest)
- Architecture and urban development (emerging interest)

Want to Visit:
- Museum of Vietnamese History - Mentioned 3 times
- Saigon Central Post Office - For photography
- Independence Palace - Historical significance
- Bitexco Financial Tower Observation Deck - City views

Preferred Visit Times:
- Weekend mornings (9:00-11:00 AM) - Less crowded
- Weekday late afternoons (4:00-6:00 PM) - After work
- Avoids: Midday heat, peak tourist hours

CURRENT VEHICLE & LOCATION INFORMATION:
Vehicle Status:
- Location: Currently on Lê Lợi Street, heading towards downtown
- Direction: Northeast towards work
- Time: 8:25 AM
- Fuel level: Will be updated based on sensor data
- Weather: Clear, 28°C, good visibility

Nearby Points of Interest (within 2km):
Gas Stations:
1. Petrolimex Station - Nguyễn Huệ St (1.2 km, 3 min) - Regular station
2. Shell Station - Hai Bà Trưng St (0.8 km, 2 min) - Closest
3. Total Station - Lê Duẩn St (1.5 km, 4 min) - On alternate route

Restaurants (for future reference):
1. Phở Hòa Pasteur - Nguyễn Công Trứ St (1.8 km, 5 min)
2. Sushi Hokkaido - Lê Lợi St (0.6 km, 2 min) - On current street
3. Cơm Niêu Singapore - Hai Bà Trưng St (1.2 km, 4 min)
4. Secret Garden Restaurant - Pasteur St (1.5 km, 5 min) - Vietnamese, highly rated
5. L'Usine Café - Đồng Khởi St (1.0 km, 3 min) - Trendy, good coffee

Cultural Sites:
1. Fine Arts Museum - Phó Đức Chính St (2.0 km, 6 min)
2. Saigon Central Post Office - Công xã Paris (1.3 km, 4 min)
3. Notre-Dame Cathedral Basilica - Công xã Paris (1.4 km, 5 min)
4. Bitexco Financial Tower - Hải Triều St (1.0 km, 3 min)

ASSISTANT CAPABILITIES:
I can provide:
✓ Proactive vehicle status monitoring and alerts
✓ Navigation assistance with real-time traffic updates
✓ Restaurant recommendations based on preferences, time, and location
✓ Cultural site information and optimal visiting times
✓ Weather and traffic condition updates
✓ Calendar and schedule management
✓ Personalized suggestions based on learned patterns
✓ Safety alerts and maintenance reminders

CURRENT CONTEXT:
It's 8:25 AM, close to Minh's usual 8:30 AM refueling time.
Minh is on the regular commute route to work.
I should be prepared to:
1. Monitor fuel level and suggest appropriate gas station
2. Provide traffic updates if relevant
3. Remember today's schedule and offer helpful suggestions
4. Be ready to recommend restaurants if asked (though unlikely during morning commute)
5. Suggest cultural activities for weekend planning if conversation naturally flows there"""

    assistant.initialize_memory(assistant_memory, by_paragraphs=True)

    conversation.add_participant(driver)
    conversation.add_participant(assistant)

    print("\n" + "="*80)
    print("🚗 Vehicle Virtual Assistant - Extended Scenario with Rich Content 🚗")
    print("="*80 + "\n")
    print(f"Setting: Single driver (Minh) in vehicle at {current_time_context}")
    print("Assistant: Smart assistant with comprehensive knowledge and preferences")
    print(f"Features: Fuel monitoring, restaurant suggestions, cultural recommendations\n")

    # PART 1: Morning Commute - Low Fuel Alert
    print(f"{'─'*80}")
    print("PART 1: Morning Commute - Low Fuel Alert")
    print(f"{'─'*80}\n")

    print("📍 Driver starts morning commute...\n")

    # Turn 1: Time-based greeting
    print(f"{'─'*80}")
    print("Turn 1: Morning Context")
    print(f"{'─'*80}")

    greeting_prompt = f"It's {current_time_context}, close to the driver's usual 8:30 AM refueling time."
    event = await driver.send_message(greeting_prompt, conversation)
    print(f"\n⏰ System: Time is {current_time_context} (5 minutes before usual refueling)")

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    if verbose:
        print(f"\n🧠 {assistant.name}'s thoughts:")
        for thought in assistant.thought_reservoir.thoughts:
            if thought.generated_turn == conversation.turn_number:
                print(f"  💭 {thought.content}")
                print(f"     (IM: {thought.intrinsic_motivation['score']:.2f})")

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)
        print(f"\n🤖 {assistant.name}: {utterance}")
        await predict_turn_taking_type(conversation)
        await conversation.broadcast_event(event)

    # Turn 2: Low fuel warning
    await asyncio.sleep(1)
    print(f"\n{'─'*80}")
    print("Turn 2: LOW FUEL WARNING")
    print(f"{'─'*80}")

    low_fuel_message = (
        "⚠️ LOW FUEL WARNING: Fuel level at 15%. "
        "Approximately 50 km remaining. Please refuel soon."
    )
    event = await driver.send_message(low_fuel_message, conversation)
    print(f"\n🚨 Vehicle System: {low_fuel_message}")

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    if verbose:
        print(f"\n🧠 {assistant.name}'s thoughts:")
        for thought in assistant.thought_reservoir.thoughts:
            if thought.generated_turn == conversation.turn_number:
                print(f"  💭 {thought.content}")
                print(f"     (IM: {thought.intrinsic_motivation['score']:.2f})")

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)
        print(f"\n🤖 {assistant.name}: {utterance}")
        await predict_turn_taking_type(conversation)
        await conversation.broadcast_event(event)

    # Turn 3: Driver acknowledges
    await asyncio.sleep(1)
    print(f"\n{'─'*80}")
    print("Turn 3: Driver Response")
    print(f"{'─'*80}")

    driver_response = "Cảm ơn! Mình sẽ đi Petrolimex. (Thanks! I'll go to Petrolimex.)"
    event = await driver.send_message(driver_response, conversation)
    print(f"\n👤 {driver.name}: {driver_response}")

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    if verbose:
        print(f"\n🧠 {assistant.name}'s thoughts:")
        for thought in assistant.thought_reservoir.thoughts:
            if thought.generated_turn == conversation.turn_number:
                print(f"  💭 {thought.content}")
                print(f"     (IM: {thought.intrinsic_motivation['score']:.2f})")

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)
        print(f"\n🤖 {assistant.name}: {utterance}")

    # PART 2: Lunch Planning - Restaurant Recommendation
    await asyncio.sleep(2)
    print(f"\n\n{'─'*80}")
    print("PART 2: Lunch Planning - Restaurant Recommendation")
    print(f"{'─'*80}\n")
    print("⏰ Later that day, around 11:45 AM...\n")

    # Turn 4: Driver asks about lunch
    print(f"{'─'*80}")
    print("Turn 4: Lunch Inquiry")
    print(f"{'─'*80}")

    lunch_query = (
        "Hey, tớ đang muốn ăn trưa, có gợi ý gì không? "
        "Hôm nay muốn ăn nhẹ thôi. "
        "(Hey, I'm thinking about lunch, any suggestions? Want something light today.)"
    )
    event = await driver.send_message(lunch_query, conversation)
    print(f"\n👤 {driver.name}: {lunch_query}")

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    if verbose:
        print(f"\n🧠 {assistant.name}'s thoughts:")
        for thought in assistant.thought_reservoir.thoughts:
            if thought.generated_turn == conversation.turn_number:
                print(f"  💭 {thought.content}")
                print(f"     (IM: {thought.intrinsic_motivation['score']:.2f})")

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)
        print(f"\n🤖 {assistant.name}: {utterance}")
        await predict_turn_taking_type(conversation)
        await conversation.broadcast_event(event)

    # Turn 5: Follow-up about specific restaurant
    await asyncio.sleep(1)
    print(f"\n{'─'*80}")
    print("Turn 5: Restaurant Selection")
    print(f"{'─'*80}")

    restaurant_decision = (
        "Secret Garden nghe hay đó! Mình có thể đặt bàn được không? "
        "(Secret Garden sounds good! Can I make a reservation?)"
    )
    event = await driver.send_message(restaurant_decision, conversation)
    print(f"\n👤 {driver.name}: {restaurant_decision}")

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    if verbose:
        print(f"\n🧠 {assistant.name}'s thoughts:")
        for thought in assistant.thought_reservoir.thoughts:
            if thought.generated_turn == conversation.turn_number:
                print(f"  💭 {thought.content}")
                print(f"     (IM: {thought.intrinsic_motivation['score']:.2f})")

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)
        print(f"\n🤖 {assistant.name}: {utterance}")

    # PART 3: Weekend Planning - Museum Suggestion
    await asyncio.sleep(2)
    print(f"\n\n{'─'*80}")
    print("PART 3: Weekend Planning - Museum Suggestion")
    print(f"{'─'*80}\n")
    print("📅 Friday evening, planning for the weekend...\n")

    # Turn 6: Driver asks about weekend activities
    print(f"{'─'*80}")
    print("Turn 6: Weekend Activity Query")
    print(f"{'─'*80}")

    weekend_query = (
        "Cuối tuần này mình muốn đi bảo tàng, có gợi ý nào không? "
        "(This weekend I want to visit a museum, any suggestions?)"
    )
    event = await driver.send_message(weekend_query, conversation)
    print(f"\n👤 {driver.name}: {weekend_query}")

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    if verbose:
        print(f"\n🧠 {assistant.name}'s thoughts:")
        for thought in assistant.thought_reservoir.thoughts:
            if thought.generated_turn == conversation.turn_number:
                print(f"  💭 {thought.content}")
                print(f"     (IM: {thought.intrinsic_motivation['score']:.2f})")

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)
        print(f"\n🤖 {assistant.name}: {utterance}")
        await predict_turn_taking_type(conversation)
        await conversation.broadcast_event(event)

    # Turn 7: Express interest in specific museum
    await asyncio.sleep(1)
    print(f"\n{'─'*80}")
    print("Turn 7: Museum Selection")
    print(f"{'─'*80}")

    museum_decision = (
        "Museum of Vietnamese History nghe hấp dẫn! "
        "Khi nào là thời gian tốt nhất để đi? "
        "(Museum of Vietnamese History sounds appealing! "
        "When is the best time to visit?)"
    )
    event = await driver.send_message(museum_decision, conversation)
    print(f"\n👤 {driver.name}: {museum_decision}")

    await predict_turn_taking_type(conversation)
    await conversation.broadcast_event(event)

    if verbose:
        print(f"\n🧠 {assistant.name}'s thoughts:")
        for thought in assistant.thought_reservoir.thoughts:
            if thought.generated_turn == conversation.turn_number:
                print(f"  💭 {thought.content}")
                print(f"     (IM: {thought.intrinsic_motivation['score']:.2f})")

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        event = await assistant.send_message(utterance, conversation)
        print(f"\n🤖 {assistant.name}: {utterance}")

    print("\n" + "="*80)
    print("🏁 End of Extended Scenario 🏁")
    print("="*80 + "\n")

    # Summary
    print("📋 Extended Scenario Summary:")
    print(f"✓ Part 1: Low fuel alert with proactive gas station suggestion")
    print(f"✓ Part 2: Personalized restaurant recommendation based on preferences")
    print(f"✓ Part 3: Weekend cultural activity suggestion with timing advice")
    print(f"✓ Total conversation turns: {len(conversation.event_history)}")
    print(f"✓ Assistant participated: {sum(1 for e in conversation.event_history if e.participant_name == assistant.name)} times")

    print("\n💡 Key Demonstration Features:")
    print("  1. Rich Memory: Detailed driver preferences and patterns")
    print("  2. Contextual Awareness: Time, location, and situation-appropriate responses")
    print("  3. Multi-Domain Knowledge: Transportation, dining, culture")
    print("  4. Proactive Assistance: Anticipating needs based on patterns")
    print("  5. Natural Dialogue: Bilingual support (Vietnamese/English)")

    print("\n")
    tracker.print_summary(detailed=False)


async def main():
    """Main entry point for the extended scenario."""
    verbose = True

    if len(sys.argv) > 1:
        verbose_arg = sys.argv[1].lower()
        if verbose_arg in ['false', 'no', '0']:
            verbose = False

    print(f"\n📝 Configuration:")
    print(f"   Completion model: {DEFAULT_COMPLETION_MODEL}")
    print(f"   Embedding model: {DEFAULT_EMBEDDING_MODEL}")
    print(f"   Verbose mode: {verbose}\n")

    await run_extended_scenario(verbose)


if __name__ == "__main__":
    asyncio.run(main())
