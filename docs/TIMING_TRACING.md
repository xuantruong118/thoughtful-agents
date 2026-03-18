# Execution Time Tracing

This document explains how to use the execution time tracing features to measure and analyze the performance of LLM calls and agent operations in the Thoughtful Agents framework.

## Overview

The timing utilities provide a comprehensive system for tracking execution times throughout the agent's thinking pipeline, including:

- **LLM API calls** - Track time spent waiting for model responses
- **Thought generation** - Measure System 1 and System 2 thought generation
- **Thought evaluation** - Track time spent evaluating intrinsic motivation
- **Thought articulation** - Measure articulation into natural language

## Quick Start

### Basic Usage

```python
import asyncio
from thoughtful_agents.models import Agent, Conversation
from thoughtful_agents.utils.timing import TimingTracker, set_timing_tracker

async def main():
    # 1. Create and set a timing tracker
    tracker = TimingTracker()
    set_timing_tracker(tracker)

    # 2. Run your agent code normally
    conversation = Conversation(context="A friendly chat")
    agent = Agent(name="Alice")
    agent.initialize_memory("I love discussing AI and technology")

    # ... your agent operations ...

    # 3. Print the timing summary
    tracker.print_summary(detailed=False)

if __name__ == "__main__":
    asyncio.run(main())
```

### Example Output

When you run an example with timing enabled, you'll see output like this:

```
======================================================================
⏱️  EXECUTION TIME SUMMARY
======================================================================
Total Operations: 12
Total Time: 8.456s

Operation Breakdown:
----------------------------------------------------------------------
Operation                      Count    Total      Avg        Min        Max
----------------------------------------------------------------------
llm_call                       6        7.234      1.206      0.892      1.534
evaluate_thought               3        3.145      1.048      0.967      1.123
generate_system2_thoughts      1        2.456      2.456      2.456      2.456
generate_system1_thought       1        1.234      1.234      1.234      1.234
articulate_thought             1        1.156      1.156      1.156      1.156
======================================================================
```

## Components

### TimingTracker

The main class for tracking execution times.

**Methods:**
- `record(operation, duration, metadata=None)` - Record an operation's execution time
- `get_summary()` - Get a dictionary with summary statistics
- `print_summary(detailed=False)` - Print a formatted summary
- `clear()` - Clear all recorded timings

**Example:**
```python
tracker = TimingTracker()
tracker.record('my_operation', 1.5, {'model': 'gpt-4o'})
summary = tracker.get_summary()
```

### Context Management

Use `set_timing_tracker()` and `get_timing_tracker()` to manage the global timing context:

```python
from thoughtful_agents.utils.timing import TimingTracker, set_timing_tracker, get_timing_tracker

# Set the tracker
tracker = TimingTracker()
set_timing_tracker(tracker)

# Later, retrieve it
current_tracker = get_timing_tracker()
```

### Timer Context Manager

For custom timing in your own code:

```python
from thoughtful_agents.utils.timing import Timer

with Timer('custom_operation', {'key': 'value'}):
    # Your code here
    await some_async_function()
```

### Async Decorator

For timing async functions:

```python
from thoughtful_agents.utils.timing import time_async

@time_async('my_function', lambda *args, **kwargs: {'arg1': kwargs.get('arg1')})
async def my_function(arg1, arg2):
    # Your code here
    return result
```

## What Gets Tracked

### Automatic Tracking

The following operations are automatically tracked when a timing tracker is set:

1. **LLM API Calls** (`llm_call`)
   - All calls to `get_completion()` in `llm_api.py`
   - Metadata: model, temperature, response_format

2. **System 1 Thought Generation** (`generate_system1_thought`)
   - Quick, intuitive thought generation
   - Metadata: agent name

3. **System 2 Thought Generation** (`generate_system2_thoughts`)
   - Deliberate, memory-based thought generation
   - Metadata: agent name, number of thoughts

4. **Thought Evaluation** (`evaluate_thought`)
   - Intrinsic motivation scoring
   - Metadata: agent name, motivation score

5. **Thought Articulation** (`articulate_thought`)
   - Converting thoughts to natural language
   - Metadata: agent name

### Custom Tracking

You can add custom timing to your own code:

```python
from thoughtful_agents.utils.timing import get_timing_tracker
import time

async def my_custom_operation():
    start_time = time.perf_counter()
    tracker = get_timing_tracker()

    # Your operation
    result = await do_something()

    # Record timing
    if tracker:
        duration = time.perf_counter() - start_time
        tracker.record('my_custom_operation', duration, {'custom': 'metadata'})

    return result
```

## Examples with Timing

### ai_thought_process.py

Shows detailed step-by-step execution with timing:

```bash
python examples/ai_thought_process.py
```

### hello_world.py

Simple two-agent conversation with timing:

```bash
python examples/hello_world.py
```

### multiparty_conversation.py

Multi-turn conversation with timing summary:

```bash
python examples/multiparty_conversation.py 5
```

## Advanced Usage

### Detailed Timing Output

For detailed information about each operation:

```python
tracker.print_summary(detailed=True)
```

This will show individual timing records with metadata.

### Accessing Raw Timing Data

```python
summary = tracker.get_summary()
print(f"Total time: {summary['total_time']:.2f}s")
print(f"Total operations: {summary['total_operations']}")

for op, stats in summary['operations'].items():
    print(f"{op}: {stats['count']} calls, avg {stats['avg_time']:.3f}s")
```

### Disabling Timing

To disable timing without changing code:

```python
# Don't set a tracker, or set it to None
set_timing_tracker(None)
```

All timing code will be skipped with minimal overhead.

### Per-Agent Timing

Track timing separately for different agents:

```python
alice_tracker = TimingTracker()
bob_tracker = TimingTracker()

# Switch between trackers as needed
set_timing_tracker(alice_tracker)
await alice.think(conversation, event)

set_timing_tracker(bob_tracker)
await bob.think(conversation, event)

# Compare results
print("Alice's timing:")
alice_tracker.print_summary()

print("Bob's timing:")
bob_tracker.print_summary()
```

## Performance Considerations

- **Minimal Overhead**: When no tracker is set, timing checks add negligible overhead (simple `if tracker:` checks)
- **Async-Safe**: Uses `contextvars` for proper async context isolation
- **High Precision**: Uses `time.perf_counter()` for sub-millisecond accuracy

## Testing

Run the timing utilities test suite:

```bash
python -m unittest tests.test_timing -v
```

## Best Practices

1. **Always initialize the tracker early** - Set it up before creating agents or conversations
2. **Print summary at the end** - Add `tracker.print_summary()` at the end of your main function
3. **Use metadata** - Add relevant metadata to help analyze performance bottlenecks
4. **Clear between runs** - Call `tracker.clear()` if reusing the same tracker
5. **Disable in production** - Don't set a tracker in production unless needed for debugging

## Troubleshooting

**No timing data collected:**
- Ensure `set_timing_tracker()` is called before agent operations
- Verify the tracker is set in the correct async context

**Incomplete data:**
- Check that the tracker is set before all operations you want to measure
- Ensure you're using the same tracker instance throughout

**Unexpected timings:**
- Remember that LLM calls include network latency and API processing time
- Parallel operations (System 1 + System 2) will show overlapping times
