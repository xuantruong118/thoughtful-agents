"""
Vehicle Virtual Assistant - Scenario 1: Passenger Conversation

This example demonstrates a proactive virtual assistant in a vehicle where two passengers
are having a conversation about car brands (Vinfast, BMW, Mercedes). The assistant
listens to the conversation and proactively provides relevant information when
appropriate without being explicitly asked.

Scenario Description (Vietnamese):
Trong xe đang có 2 hành khách trò chuyện với nhau, chủ đề là đang thảo luận về
xe oto Vinfast, BMW, Mercedes

English Translation:
In the vehicle, there are 2 passengers conversing with each other, discussing
car brands: Vinfast, BMW, Mercedes
"""

import asyncio
import sys
from typing import Optional

from thoughtful_agents.models import (
    Agent,
    Human,
    Conversation,
)
from thoughtful_agents.utils.turn_taking_engine import decide_next_speaker_and_utterance, predict_turn_taking_type
from thoughtful_agents.utils.llm_api import DEFAULT_COMPLETION_MODEL, DEFAULT_EMBEDDING_MODEL

async def run_scenario1(num_turns: int = 10, verbose: bool = True):
    """
    Run a vehicle assistant simulation where two passengers discuss car brands.
    The virtual assistant proactively provides information when relevant.

    Args:
        num_turns: Number of conversation turns to simulate
        verbose: Whether to print detailed thought processes
    """
    # Create a conversation context for a vehicle setting
    conversation = Conversation(
        context="A conversation in a vehicle. Two passengers are discussing car brands "
                "including Vinfast, BMW, and Mercedes. A virtual assistant is present to "
                "provide helpful information when relevant."
    )

    # Create two human passengers
    passenger1 = Human(name="Hương")
    passenger2 = Human(name="Nam")

    # Create a proactive virtual assistant
    # The assistant should be helpful but not intrusive
    assistant = Agent(name="Vehicle Assistant", proactivity_config={
        'im_threshold': 3.2,  # Moderate threshold - speaks when has relevant info
        'system1_prob': 0.3,  # Balanced between quick and deliberate responses
        'interrupt_threshold': 3.8  # Will interrupt for highly relevant information
    })

    # Initialize the assistant's knowledge base with information about car brands
    assistant_knowledge = """I am a virtual assistant integrated into this vehicle.
My purpose is to provide helpful information to passengers when relevant to their conversation.

About Vinfast:
Vinfast is Vietnam's first domestic car manufacturer, founded in 2017 by Vingroup.
Vinfast produces electric vehicles (EVs) and has expanded to international markets including the US and Europe.
Popular Vinfast models include the VF 8 and VF 9 electric SUVs.
Vinfast is known for competitive pricing and modern technology features.
The company has ambitious plans to become a leading global EV manufacturer.

About BMW:
BMW (Bayerische Motoren Werke) is a German luxury vehicle manufacturer founded in 1916.
BMW is known for high performance, luxury, and the "Ultimate Driving Machine" slogan.
Popular BMW models include the 3 Series, 5 Series, X5 SUV, and the i4 electric vehicle.
BMW emphasizes driving dynamics, premium materials, and advanced technology.
BMW has a strong reputation for reliability and engineering excellence.

About Mercedes-Benz:
Mercedes-Benz is a German luxury automaker, part of the Mercedes-Benz Group AG.
Mercedes is known for luxury, comfort, innovation, and safety features.
Popular Mercedes models include the C-Class, E-Class, S-Class, and the EQS electric sedan.
Mercedes has a long history of automotive innovation including the first production automobile.
Mercedes-Benz emphasizes comfort, prestige, and cutting-edge technology.

Comparison:
Vinfast offers affordability and modern EV technology with Vietnamese pride.
BMW focuses on driving performance and sporty handling.
Mercedes emphasizes luxury, comfort, and prestige.
All three brands offer electric vehicle options.
BMW and Mercedes have longer heritage and established global reputation.
Vinfast is newer but growing rapidly with competitive pricing."""

    # Add knowledge to the assistant
    assistant.initialize_memory(assistant_knowledge, by_paragraphs=True)

    # Add participants to the conversation
    conversation.add_participant(passenger1)
    conversation.add_participant(passenger2)
    conversation.add_participant(assistant)

    print("\n" + "="*70)
    print("🚗 Vehicle Virtual Assistant - Scenario 1: Passenger Conversation 🚗")
    print("="*70 + "\n")
    print("Setting: Two passengers (Hương and Nam) discussing car brands")
    print("Assistant: Proactive vehicle assistant ready to help\n")

    # Define the conversation script between passengers
    conversation_script = [
        {
            "speaker": passenger1,
            "message": "Nam, anh nghĩ sao về những chiếc xe Vinfast mới? Em thấy họ đang quảng cáo nhiều lắm."
                      " (Nam, what do you think about the new Vinfast cars? I see they're advertising a lot.)"
        },
        {
            "speaker": passenger2,
            "message": "Ừ, em cũng để ý. Vinfast VF 8 trông khá đẹp đấy. Nhưng mà anh vẫn nghĩ BMW hay Mercedes "
                      "có độ tin cậy cao hơn, thương hiệu lâu đời mà. (Yeah, I've noticed too. The Vinfast VF 8 "
                      "looks pretty nice. But I still think BMW or Mercedes are more reliable, they're established brands.)"
        },
        {
            "speaker": passenger1,
            "message": "Đúng là vậy, nhưng mà giá của Vinfast rẻ hơn nhiều so với BMW hay Mercedes. Mình có thể "
                      "có được một chiếc xe điện hiện đại mà không tốn quá nhiều tiền. (That's true, but Vinfast "
                      "is much cheaper than BMW or Mercedes. We can get a modern electric car without spending too much.)"
        },
        {
            "speaker": passenger2,
            "message": "Ừ đúng rồi. BMW thì nổi tiếng về khả năng vận hành thể thao, còn Mercedes thì sang trọng "
                      "và thoải mái hơn. Nhưng mà cả hai đều đắt đỏ lắm. (True. BMW is famous for sporty driving, "
                      "and Mercedes is more luxurious and comfortable. But both are very expensive.)"
        },
        {
            "speaker": passenger1,
            "message": "Anh có biết là Vinfast đã bắt đầu xuất khẩu sang Mỹ và châu Âu không? Họ có tham vọng "
                      "lớn lắm đấy. (Do you know that Vinfast has started exporting to the US and Europe? "
                      "They have big ambitions.)"
        },
        {
            "speaker": passenger2,
            "message": "Vậy à? Thú vị đấy. Nếu chọn xe điện thì em sẽ chọn loại nào nhỉ? BMW i4, Mercedes EQS, "
                      "hay Vinfast VF 9? (Really? That's interesting. If choosing an electric car, which one would "
                      "you choose? BMW i4, Mercedes EQS, or Vinfast VF 9?)"
        }
    ]

    # Process the conversation
    for i, turn in enumerate(conversation_script):
        print(f"\n{'─'*70}")
        print(f"Turn {i+1}")
        print(f"{'─'*70}")

        speaker = turn["speaker"]
        message = turn["message"]

        # Passenger speaks
        event = await speaker.send_message(message, conversation)
        print(f"\n👤 {speaker.name}: {message}")

        # Predict turn allocation
        turn_allocation = await predict_turn_taking_type(conversation)
        if verbose:
            print(f"\n🎯 Turn-taking prediction: {turn_allocation}")

        # Broadcast event to all agents (assistant will think)
        await conversation.broadcast_event(event)

        # Show assistant's thoughts if verbose
        if verbose:
            print(f"\n🧠 {assistant.name}'s thoughts:")
            for thought in assistant.thought_reservoir.thoughts:
                if thought.generated_turn == conversation.turn_number:
                    print(f"  💭 {thought.content}")
                    print(f"     (Intrinsic Motivation: {thought.intrinsic_motivation['score']})")

        # Check if assistant wants to speak
        next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)

        if next_speaker and next_speaker.name == assistant.name:
            # Assistant speaks
            event = await assistant.send_message(utterance, conversation)
            print(f"\n🤖 {assistant.name}: {utterance}")

            # Broadcast assistant's message
            if i < len(conversation_script) - 1:  # Don't broadcast on last turn
                await predict_turn_taking_type(conversation)
                await conversation.broadcast_event(event)
        else:
            if verbose:
                print(f"\n🤖 {assistant.name}: (listening attentively)")

    # Final check if assistant wants to add anything
    print(f"\n{'─'*70}")
    print(f"Final Assistant Response")
    print(f"{'─'*70}")

    next_speaker, utterance = await decide_next_speaker_and_utterance(conversation)
    if next_speaker and next_speaker.name == assistant.name:
        print(f"\n🤖 {assistant.name}: {utterance}")
    else:
        print(f"\n🤖 {assistant.name}: (conversation concluded)")

    print("\n" + "="*70)
    print("🏁 End of Scenario 1 🏁")
    print("="*70 + "\n")

    # Summary
    print("📋 Conversation Summary:")
    print(f"Total turns: {len(conversation.event_history)}")
    print(f"Assistant participated: {sum(1 for e in conversation.event_history if e.participant_name == assistant.name)} times")
    print("\nFull conversation history:")
    for i, event in enumerate(conversation.event_history):
        participant_name = event.participant_name
        content = event.content[:100] + "..." if len(event.content) > 100 else event.content
        print(f"  {i+1}. {participant_name}: {content}")


async def main():
    """Main entry point for the scenario."""
    # Parse command line arguments
    num_turns = 10  # Default
    verbose = True  # Default

    if len(sys.argv) > 1:
        try:
            num_turns = int(sys.argv[1])
        except ValueError:
            print("Invalid number of turns. Using default of 10.")

    if len(sys.argv) > 2:
        verbose_arg = sys.argv[2].lower()
        if verbose_arg in ['false', 'no', '0']:
            verbose = False

    # Print configuration
    print(f"\n📝 Configuration:")
    print(f"   Completion model: {DEFAULT_COMPLETION_MODEL}")
    print(f"   Embedding model: {DEFAULT_EMBEDDING_MODEL}")
    print(f"   Verbose mode: {verbose}\n")

    await run_scenario1(num_turns, verbose)


if __name__ == "__main__":
    asyncio.run(main())
