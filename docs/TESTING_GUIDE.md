# Testing Guide for Thoughtful Agents Web Demo

This document provides comprehensive instructions for testing the web UI and extended scenarios.

## Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set OpenAI API Key**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

4. **Install spaCy language model** (if not already installed)
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Quick Start Testing

### Automated Test Script

Run the automated test script to validate your setup:

```bash
bash scripts/test_web_demo.sh
```

This will check:
- ✓ Python version compatibility
- ✓ Directory structure
- ✓ Required files presence
- ✓ Python dependencies
- ✓ OpenAI API key configuration
- ✓ Python syntax validation

## Manual Testing

### Test 1: Web UI - Basic Scenario

**Objective**: Test the three-panel web interface with the basic vehicle assistant scenario

**Steps**:
1. Navigate to the web demo directory:
   ```bash
   cd web_demo
   ```

2. Start the Flask server:
   ```bash
   python app.py
   ```

3. Open browser to `http://localhost:5000`

4. Click "▶️ Start Demo"

**Expected Results**:
- ✓ Status indicator shows "Running"
- ✓ Memory panel populates with agent's learned patterns
- ✓ Conversation panel shows dialogue between driver and assistant
- ✓ Inner Thoughts panel displays agent's cognitive process with IM scores
- ✓ Low fuel warning triggers proactive gas station suggestion
- ✓ All updates appear in real-time via SSE

**Key Things to Verify**:
- [ ] Memory panel shows daily 8:30 AM refueling pattern
- [ ] Memory panel shows nearby gas stations information
- [ ] Conversation flows naturally between system, driver, and assistant
- [ ] Inner thoughts show intrinsic motivation scores
- [ ] Assistant proactively responds to low fuel warning
- [ ] UI is responsive and updates smoothly
- [ ] No JavaScript errors in browser console
- [ ] SSE connection remains stable throughout demo

### Test 2: Web UI - Custom Triggers

**Objective**: Test manual trigger functionality

**Steps**:
1. With demo running (from Test 1)
2. Enter custom message in trigger input:
   ```
   Traffic congestion detected on Nguyễn Huệ Street
   ```
3. Click "Send Trigger"

**Expected Results**:
- ✓ Message appears in conversation panel
- ✓ Assistant generates thoughts about the trigger
- ✓ Assistant may respond based on context
- ✓ Intrinsic motivation scores update

**Additional Triggers to Test**:
- "Driver mentions feeling hungry"
- "Weekend is approaching"
- "Need restaurant recommendation"
- "Looking for cultural activities"

### Test 3: Extended Scenario - CLI

**Objective**: Test the extended scenario with restaurant and museum features

**Steps**:
1. Return to repository root:
   ```bash
   cd ..
   ```

2. Run the extended scenario:
   ```bash
   python examples/vehicle_assistant_extended.py
   ```

**Expected Results**:
- ✓ **Part 1**: Low fuel alert with gas station suggestion
- ✓ **Part 2**: Restaurant recommendation based on preferences
  - Should consider time of day (lunch)
  - Should match dietary preferences (light meal)
  - Should suggest restaurants with ratings and locations
- ✓ **Part 3**: Museum suggestion with timing advice
  - Should recall driver's interest in Vietnamese history
  - Should provide optimal visit times
  - Should consider driver's weekend schedule

**Key Things to Verify**:
- [ ] Agent memory includes detailed preferences
- [ ] Restaurant suggestions match stated preferences
- [ ] Museum recommendations align with interests
- [ ] Bilingual responses (Vietnamese/English) work correctly
- [ ] Context awareness across different times of day
- [ ] Multiple conversation topics flow naturally
- [ ] Execution time summary appears at the end

### Test 4: Basic Scenario - CLI

**Objective**: Verify the original scenario still works correctly

**Steps**:
```bash
python examples/vehicle_assistant_scenario2.py
```

**Expected Results**:
- ✓ Focus on low fuel memory pattern
- ✓ Morning greeting based on time context
- ✓ Proactive response to fuel warning
- ✓ Navigation assistance provided
- ✓ Summary shows all key features demonstrated

### Test 5: Browser Compatibility

**Objective**: Ensure web UI works across different browsers

**Browsers to Test**:
- [ ] Chrome/Chromium (latest)
- [ ] Firefox (latest)
- [ ] Safari (if available)
- [ ] Edge (if available)

**What to Check**:
- SSE connection stability
- CSS rendering (three-panel layout)
- Animations (slide-in effects)
- Scrolling behavior
- Button interactions
- Input field functionality

### Test 6: Concurrent Sessions

**Objective**: Test multiple browser sessions connecting to the same server

**Steps**:
1. Start Flask server
2. Open `http://localhost:5000` in Browser 1
3. Open `http://localhost:5000` in Browser 2
4. Start demo in Browser 1

**Expected Results**:
- ✓ Both browsers receive SSE updates
- ✓ Both show the same conversation progress
- ✓ No conflicts or race conditions
- ✓ Trigger from Browser 2 works while Browser 1 is viewing

### Test 7: Error Handling

**Objective**: Verify graceful error handling

**Scenarios to Test**:

1. **Missing API Key**:
   ```bash
   unset OPENAI_API_KEY
   python web_demo/app.py
   # Try to start demo - should fail gracefully
   ```

2. **Network Interruption**:
   - Start demo
   - Disconnect internet briefly
   - Reconnect
   - Verify SSE reconnection

3. **Rapid Button Clicks**:
   - Click "Start Demo" multiple times rapidly
   - Should prevent concurrent runs

4. **Empty Trigger Message**:
   - Try sending empty trigger
   - Should show validation error

## Performance Testing

### Memory Usage

Monitor memory consumption during demo:

```bash
# In one terminal
cd web_demo && python app.py

# In another terminal
ps aux | grep "python app.py"
# Note RSS memory before and after demo runs
```

**Expected**:
- Memory should remain stable
- No significant memory leaks after multiple runs

### Response Times

Observe response times for:
- Initial page load: < 2 seconds
- SSE connection establishment: < 1 second
- Thought generation: 2-5 seconds (depends on OpenAI API)
- UI updates: Immediate (< 100ms)

## Integration Testing Checklist

- [ ] All Python files compile without syntax errors
- [ ] All dependencies are listed in requirements.txt
- [ ] Flask server starts without errors
- [ ] SSE endpoint returns valid event stream
- [ ] HTML template renders correctly
- [ ] CSS styles apply properly
- [ ] JavaScript loads and executes without errors
- [ ] Agent classes (UIAgent, UIHuman) emit events correctly
- [ ] Event queue handles concurrent access safely
- [ ] Threading model works correctly
- [ ] asyncio event loops don't conflict
- [ ] Git repository structure is maintained
- [ ] README files are comprehensive

## Known Limitations

1. **Single Demo Instance**: Only one demo can run at a time per server instance
2. **API Rate Limits**: OpenAI API rate limits may affect demo speed
3. **Browser Keep-Alive**: SSE connection may timeout after 30 seconds of inactivity
4. **Memory Size**: Extensive memory content may slow initial loading

## Troubleshooting

### Issue: SSE Connection Drops

**Solution**:
- Check Flask console for errors
- Verify no firewall blocking localhost:5000
- Try restarting the Flask server
- Clear browser cache

### Issue: Thoughts Not Appearing

**Solution**:
- Verify OpenAI API key is valid
- Check network connectivity
- Look for errors in Flask console
- Ensure agent's intrinsic motivation threshold is being met

### Issue: Slow Response Times

**Solution**:
- Check OpenAI API status
- Reduce memory content size
- Increase timeout values if needed
- Monitor system resource usage

### Issue: UI Layout Issues

**Solution**:
- Hard refresh browser (Ctrl+Shift+R)
- Check browser console for CSS errors
- Verify all static files are served correctly
- Try different browser

## Test Report Template

After completing tests, document results:

```markdown
# Test Report - [Date]

## Environment
- Python Version:
- OS:
- Browser:
- OpenAI Model:

## Test Results

### Test 1: Web UI - Basic Scenario
- Status: ✓ Pass / ✗ Fail
- Notes:

### Test 2: Web UI - Custom Triggers
- Status: ✓ Pass / ✗ Fail
- Notes:

### Test 3: Extended Scenario - CLI
- Status: ✓ Pass / ✗ Fail
- Notes:

### Test 4: Basic Scenario - CLI
- Status: ✓ Pass / ✗ Fail
- Notes:

### Test 5: Browser Compatibility
- Status: ✓ Pass / ✗ Fail
- Notes:

### Test 6: Concurrent Sessions
- Status: ✓ Pass / ✗ Fail
- Notes:

### Test 7: Error Handling
- Status: ✓ Pass / ✗ Fail
- Notes:

## Issues Found
1.
2.

## Recommendations
1.
2.
```

## Next Steps

After successful testing:
1. Document any issues found
2. Create GitHub issues for bugs
3. Update documentation based on testing insights
4. Consider additional features based on user experience
5. Prepare for deployment if applicable
