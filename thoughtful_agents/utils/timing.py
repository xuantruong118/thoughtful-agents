"""Timing and tracing utilities for measuring execution time of LLM calls and agent operations."""
import time
from typing import Optional, Dict, Any, Callable
import functools
import asyncio
from contextvars import ContextVar
import logging

logger = logging.getLogger(__name__)

# Context variable to store timing information throughout async call chain
_timing_context: ContextVar[Optional[Dict[str, Any]]] = ContextVar('timing_context', default=None)


class TimingTracker:
    """Tracks execution times for various operations."""

    def __init__(self):
        self.timings = []
        self.enabled = True

    def record(self, operation: str, duration: float, metadata: Optional[Dict[str, Any]] = None):
        """Record an operation's execution time.

        Args:
            operation: Name of the operation (e.g., "llm_call", "system1_thought", "evaluate_thought")
            duration: Duration in seconds
            metadata: Additional metadata (e.g., model, temperature, tokens)
        """
        if not self.enabled:
            return

        record = {
            'operation': operation,
            'duration': duration,
            'timestamp': time.time()
        }
        if metadata:
            record['metadata'] = metadata
        self.timings.append(record)

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all recorded timings.

        Returns:
            Dictionary with summary statistics
        """
        if not self.timings:
            return {'total_operations': 0, 'total_time': 0}

        total_time = sum(t['duration'] for t in self.timings)
        operations = {}

        for timing in self.timings:
            op = timing['operation']
            if op not in operations:
                operations[op] = {
                    'count': 0,
                    'total_time': 0,
                    'min_time': float('inf'),
                    'max_time': 0
                }

            operations[op]['count'] += 1
            operations[op]['total_time'] += timing['duration']
            operations[op]['min_time'] = min(operations[op]['min_time'], timing['duration'])
            operations[op]['max_time'] = max(operations[op]['max_time'], timing['duration'])

        # Calculate averages
        for op in operations:
            operations[op]['avg_time'] = operations[op]['total_time'] / operations[op]['count']

        return {
            'total_operations': len(self.timings),
            'total_time': total_time,
            'operations': operations
        }

    def print_summary(self, detailed: bool = False):
        """Print a formatted summary of timings.

        Args:
            detailed: If True, print detailed information for each operation
        """
        summary = self.get_summary()

        if summary['total_operations'] == 0:
            print("\n⏱️  No timing data recorded")
            return

        print("\n" + "="*70)
        print("⏱️  EXECUTION TIME SUMMARY")
        print("="*70)
        print(f"Total Operations: {summary['total_operations']}")
        print(f"Total Time: {summary['total_time']:.3f}s")
        print()

        if 'operations' in summary:
            print("Operation Breakdown:")
            print("-" * 70)
            print(f"{'Operation':<30} {'Count':<8} {'Total':<10} {'Avg':<10} {'Min':<10} {'Max':<10}")
            print("-" * 70)

            for op, stats in sorted(summary['operations'].items(),
                                   key=lambda x: x[1]['total_time'],
                                   reverse=True):
                print(f"{op:<30} {stats['count']:<8} {stats['total_time']:<10.3f} "
                      f"{stats['avg_time']:<10.3f} {stats['min_time']:<10.3f} {stats['max_time']:<10.3f}")

        if detailed and self.timings:
            print("\n" + "-" * 70)
            print("Detailed Timing Records:")
            print("-" * 70)
            for i, timing in enumerate(self.timings, 1):
                print(f"\n{i}. {timing['operation']}: {timing['duration']:.3f}s")
                if 'metadata' in timing:
                    for key, value in timing['metadata'].items():
                        print(f"   - {key}: {value}")

        print("="*70 + "\n")

    def clear(self):
        """Clear all recorded timings."""
        self.timings.clear()


def get_timing_tracker() -> Optional[TimingTracker]:
    """Get the current timing tracker from context.

    Returns:
        TimingTracker instance or None if not set
    """
    return _timing_context.get()


def set_timing_tracker(tracker: Optional[TimingTracker]):
    """Set the timing tracker in context.

    Args:
        tracker: TimingTracker instance or None to disable tracking
    """
    _timing_context.set(tracker)


class Timer:
    """Context manager for timing code blocks."""

    def __init__(self, operation: str, metadata: Optional[Dict[str, Any]] = None):
        self.operation = operation
        self.metadata = metadata
        self.start_time = None
        self.duration = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duration = time.perf_counter() - self.start_time
        tracker = get_timing_tracker()
        if tracker:
            tracker.record(self.operation, self.duration, self.metadata)


def time_async(operation: str, metadata_fn: Optional[Callable] = None):
    """Decorator to time async functions.

    Args:
        operation: Name of the operation
        metadata_fn: Optional function to extract metadata from function arguments

    Example:
        @time_async("my_operation", lambda *args, **kwargs: {"arg1": kwargs.get("arg1")})
        async def my_function(arg1, arg2):
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            tracker = get_timing_tracker()
            if not tracker:
                # No tracker set, just execute the function
                return await func(*args, **kwargs)

            metadata = metadata_fn(*args, **kwargs) if metadata_fn else None
            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = time.perf_counter() - start_time
                tracker.record(operation, duration, metadata)

        return wrapper
    return decorator
