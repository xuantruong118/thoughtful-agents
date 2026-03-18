"""Unit tests for timing utilities."""
import unittest
import asyncio
import time
from thoughtful_agents.utils.timing import (
    TimingTracker,
    get_timing_tracker,
    set_timing_tracker,
    Timer,
    time_async
)


class TestTimingTracker(unittest.TestCase):
    def test_timing_tracker_creation(self):
        """Test that a timing tracker can be created."""
        tracker = TimingTracker()
        self.assertIsNotNone(tracker)
        self.assertEqual(len(tracker.timings), 0)

    def test_record_timing(self):
        """Test that timings can be recorded."""
        tracker = TimingTracker()
        tracker.record('test_operation', 1.5, {'key': 'value'})

        self.assertEqual(len(tracker.timings), 1)
        self.assertEqual(tracker.timings[0]['operation'], 'test_operation')
        self.assertEqual(tracker.timings[0]['duration'], 1.5)
        self.assertEqual(tracker.timings[0]['metadata']['key'], 'value')

    def test_get_summary(self):
        """Test that timing summary is calculated correctly."""
        tracker = TimingTracker()
        tracker.record('op1', 1.0)
        tracker.record('op1', 2.0)
        tracker.record('op2', 3.0)

        summary = tracker.get_summary()

        self.assertEqual(summary['total_operations'], 3)
        self.assertEqual(summary['total_time'], 6.0)
        self.assertEqual(summary['operations']['op1']['count'], 2)
        self.assertEqual(summary['operations']['op1']['total_time'], 3.0)
        self.assertEqual(summary['operations']['op1']['avg_time'], 1.5)
        self.assertEqual(summary['operations']['op2']['count'], 1)
        self.assertEqual(summary['operations']['op2']['total_time'], 3.0)

    def test_clear(self):
        """Test that timings can be cleared."""
        tracker = TimingTracker()
        tracker.record('test', 1.0)
        self.assertEqual(len(tracker.timings), 1)

        tracker.clear()
        self.assertEqual(len(tracker.timings), 0)

    def test_context_variable(self):
        """Test that timing tracker can be set and retrieved from context."""
        tracker = TimingTracker()
        set_timing_tracker(tracker)

        retrieved = get_timing_tracker()
        self.assertIs(retrieved, tracker)

    def test_timer_context_manager(self):
        """Test that Timer context manager works."""
        tracker = TimingTracker()
        set_timing_tracker(tracker)

        with Timer('test_operation', {'test': 'data'}):
            time.sleep(0.01)  # Sleep for at least 10ms

        self.assertEqual(len(tracker.timings), 1)
        self.assertEqual(tracker.timings[0]['operation'], 'test_operation')
        self.assertGreater(tracker.timings[0]['duration'], 0.01)
        self.assertEqual(tracker.timings[0]['metadata']['test'], 'data')

    def test_async_decorator(self):
        """Test that async timing decorator works."""
        tracker = TimingTracker()
        set_timing_tracker(tracker)

        @time_async('async_operation', lambda *args, **kwargs: {'arg': args[0] if args else None})
        async def test_function(value):
            await asyncio.sleep(0.01)
            return value * 2

        # Run the async function
        result = asyncio.run(test_function(5))

        self.assertEqual(result, 10)
        self.assertEqual(len(tracker.timings), 1)
        self.assertEqual(tracker.timings[0]['operation'], 'async_operation')
        self.assertGreater(tracker.timings[0]['duration'], 0.01)
        self.assertEqual(tracker.timings[0]['metadata']['arg'], 5)

    def test_disabled_tracker(self):
        """Test that operations work when no tracker is set."""
        set_timing_tracker(None)

        # Should not raise any errors
        with Timer('test'):
            pass

        @time_async('test_op')
        async def test_func():
            return 42

        result = asyncio.run(test_func())
        self.assertEqual(result, 42)


if __name__ == "__main__":
    unittest.main()
