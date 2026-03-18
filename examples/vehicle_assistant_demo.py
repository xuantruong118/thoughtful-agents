"""
Vehicle Virtual Assistant - Combined Demo

This script demonstrates both scenarios of a proactive virtual assistant in a vehicle:

Scenario 1: Passenger Conversation About Car Brands
- Two passengers discuss Vinfast, BMW, and Mercedes
- Assistant proactively provides relevant information

Scenario 2: Memory-Based Low Fuel Alert
- Driver alone in vehicle
- Assistant remembers daily 8:30 AM refueling pattern
- Low fuel trigger causes proactive gas station suggestion

Usage:
    python examples/vehicle_assistant_demo.py [scenario] [verbose]

    scenario: 1, 2, or 'both' (default: both)
    verbose: true or false (default: true)

Examples:
    python examples/vehicle_assistant_demo.py both true
    python examples/vehicle_assistant_demo.py 1 false
    python examples/vehicle_assistant_demo.py 2
"""

import asyncio
import sys

# Import both scenarios
from vehicle_assistant_scenario1 import run_scenario1
from vehicle_assistant_scenario2 import run_scenario2

async def run_demo(scenario: str = "both", verbose: bool = True):
    """
    Run the vehicle assistant demo for specified scenario(s).

    Args:
        scenario: Which scenario to run ('1', '2', or 'both')
        verbose: Whether to show detailed thought processes
    """

    if scenario == "both" or scenario == "1":
        print("\n" + "🌟"*35)
        print("SCENARIO 1: Passenger Conversation About Car Brands")
        print("🌟"*35 + "\n")
        await run_scenario1(num_turns=10, verbose=verbose)

        if scenario == "both":
            print("\n\n")
            input("Press Enter to continue to Scenario 2...")
            print("\n\n")

    if scenario == "both" or scenario == "2":
        print("\n" + "🌟"*35)
        print("SCENARIO 2: Memory-Based Low Fuel Alert")
        print("🌟"*35 + "\n")
        await run_scenario2(verbose=verbose)

    # Final summary
    print("\n" + "="*70)
    print("✅ DEMO COMPLETED ✅")
    print("="*70)
    print("\nBoth scenarios demonstrate:")
    print("  • Proactive conversational AI behavior")
    print("  • Memory-based pattern recognition")
    print("  • Context-aware responses")
    print("  • Event-driven triggers")
    print("  • Natural multi-turn conversations")
    print("\nBased on the 'Thoughtful Agents' framework")
    print("Paper: 'Proactive Conversational Agents with Inner Thoughts' (CHI 2025)")
    print("="*70 + "\n")


def main():
    """Parse arguments and run the demo."""
    scenario = "both"
    verbose = True

    # Parse scenario argument
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['1', '2', 'both']:
            scenario = arg
        else:
            print(f"Invalid scenario '{arg}'. Using 'both'.")

    # Parse verbose argument
    if len(sys.argv) > 2:
        verbose_arg = sys.argv[2].lower()
        if verbose_arg in ['false', 'no', '0']:
            verbose = False

    print("\n" + "="*70)
    print("🚗 VEHICLE VIRTUAL ASSISTANT DEMONSTRATION 🚗")
    print("="*70)
    print(f"\nConfiguration:")
    print(f"  Scenario: {scenario}")
    print(f"  Verbose: {verbose}")
    print("\nRequirements:")
    print("  • Set OPENAI_API_KEY environment variable")
    print("  • Install dependencies: pip install -r requirements.txt")
    print("="*70)

    # Run the demo
    asyncio.run(run_demo(scenario, verbose))


if __name__ == "__main__":
    main()
