# Quick Start Guide - Web Demo UI

## ⚡ 5-Minute Setup

### Step 1: Prerequisites Check

```bash
# Check Python version (need 3.8+)
python --version

# Check if you have the package
pip list | grep thoughtful-agents
```

### Step 2: Set API Key

```bash
# Set your OpenAI API key
export OPENAI_API_KEY=your_api_key_here

# Verify it's set
echo $OPENAI_API_KEY
```

### Step 3: Start the Server

```bash
# Navigate to web_demo directory
cd web_demo

# Start Flask server
python app.py
```

You should see:
```
Starting Thoughtful Agents Web Demo...
Open http://localhost:5000 in your browser
...
* Running on http://127.0.0.1:5000
```

### Step 4: Open in Browser

Open your browser and go to:
```
http://localhost:5000
```

### Step 5: Start the Demo

1. Click the **"▶️ Start Demo"** button
2. Watch the automatic scenario play out:
   - Memory items appear in the left panel
   - Conversation starts in the middle panel
   - Inner thoughts show up in the right panel with IM scores

## 🎮 Interactive Usage

### Try User Messages

1. **Select a speaker** from the dropdown:
   - Minh (Driver)
   - Passenger A
   - Passenger B

2. **Type a message**, for example:
   ```
   "What's the best route to the airport?"
   ```

3. **Click "📤 Send Message"** or press Enter

4. **Watch the AI**:
   - Inner thoughts appear (right panel)
   - AI responds when motivated enough (middle panel)

### Try System Triggers

1. **Select a preset** from the "System Trigger" dropdown:
   - ⛽ Low Fuel
   - 🛞 Low Tire Pressure
   - 🌧️ Heavy Rain
   - etc.

2. **Or write custom JSON**:
   ```json
   {"event": "low_fuel", "level": "10%", "range": "25km"}
   ```

3. **Click "⚡ Send System Trigger"**

4. **Observe proactive behavior**:
   - System event appears in conversation
   - AI generates thoughts about it
   - AI may proactively speak without being asked!

## 🔍 What to Look For

### In the Left Panel (Long-term Memory)
- **KNO #1, #2, #3...**: Things the AI has learned
- Driver's patterns and preferences
- Location knowledge

### In the Middle Panel (Conversation)
- 🟢 **Green**: Human messages
- 🔵 **Blue**: AI agent responses
- 🟡 **Orange**: System events/triggers
- **Turn numbers** for reference

### In the Right Panel (Inner Thoughts)
- **IM scores**: 1-5 scale
  - Low (1-2): Not motivated to speak
  - Medium (2.5-3.5): Considering speaking
  - High (3.5-4.5): Wants to speak
  - Very High (4.5-5): Will interrupt if needed
- **Thought content**: What AI is thinking
- **Turn reference**: When the thought occurred

## 💡 Example Interactions

### Example 1: Ask for Recommendations

```
Speaker: Minh (Driver)
Message: "I need coffee, any suggestions?"

Expected behavior:
- AI checks memory for coffee preferences
- Generates thoughts about nearby coffee shops
- Responds with personalized suggestion
```

### Example 2: Trigger Low Fuel

```
Preset: ⛽ Low Fuel (15%, 45km range)

Expected behavior:
- System trigger appears in conversation
- AI thinks about fuel level + driver's patterns
- AI proactively suggests gas station
- May mention it's close to driver's usual refuel time
```

### Example 3: Multi-Party Conversation

```
Passenger A: "Have you heard about the new Tesla Model 3?"
Passenger B: "Yeah, but I prefer BMWs for their reliability"

Expected behavior:
- AI listens and generates thoughts
- If IM score is high enough, AI joins conversation
- Provides relevant information about car brands
```

## 🎯 Key Concepts to Understand

### Proactive vs Reactive

**Reactive** (Traditional AI):
```
User: "What's the weather?"
AI: "It's sunny"
```

**Proactive** (This Demo):
```
System: Heavy rain detected
AI Inner Thought: (IM: 4.5) "Rain + user driving + slippery roads"
AI: "I notice heavy rain. Please drive carefully, visibility is low."
```

### Inner Thoughts Show "Why"

Without inner thoughts:
```
AI: "Let's stop for gas"
(User: Why now?)
```

With inner thoughts (visible):
```
Inner Thought (IM: 4.5): "Fuel at 15%, user's usual refuel time (8:30 AM), preferred station nearby"
AI: "It's almost 8:30, your usual refuel time. The Petrolimex station is 1.2km away, and we're at 15% fuel."
(User: Ah, makes sense!)
```

## 🔧 Customization Tips

### Change AI Personality

Edit `app.py`, line ~175:
```python
assistant = UIAgent(name="Smart Vehicle Assistant", proactivity_config={
    'im_threshold': 2.5,  # Lower = more talkative
    'system1_prob': 0.4,
    'interrupt_threshold': 2.8  # Lower = interrupts more
})
```

Try:
- **More proactive**: `im_threshold: 2.0, interrupt_threshold: 2.5`
- **Less proactive**: `im_threshold: 3.5, interrupt_threshold: 4.0`

### Add Your Own Memory

Edit `app.py`, line ~180:
```python
assistant_memory = """
I am a smart vehicle assistant.

Driver's patterns:
- Your custom patterns here
- Favorite restaurants
- Regular destinations
- Music preferences
"""
```

## 🐛 Common Issues

### "Connection lost"
- **Fix**: Refresh the page (F5)
- SSE reconnects automatically

### "No inner thoughts appearing"
- **Reason**: IM scores might be too low
- **Fix**: Try a stronger trigger (low fuel, tire pressure)

### "AI not responding"
- **Check**: Is OpenAI API key set?
- **Check**: Any errors in terminal?
- **Try**: Click "🔄 Restart" button

### "Port 5000 already in use"
- **Fix**: Stop other Flask apps or change port in `app.py`:
  ```python
  app.run(debug=True, threaded=True, port=5001)
  ```

## 📚 Next Steps

1. **Read the full README.md** for detailed documentation
2. **Experiment with different triggers** to see proactive behavior
3. **Try multi-party conversations** with different speakers
4. **Check the paper**: [Proactive Conversational Agents with Inner Thoughts](https://arxiv.org/pdf/2501.00383)

## 🎓 Learning Resources

- **Framework docs**: Check main README.md in repository root
- **Example scenarios**: See `examples/` directory
- **Vehicle assistant**: See `examples/VEHICLE_ASSISTANT_README.md`

## ✅ Checklist: Am I Using It Right?

- [ ] Can see three panels: Memory, Conversation, Thoughts
- [ ] Control panel has buttons and inputs
- [ ] Status badge shows "Running" when demo starts
- [ ] Counters update when events occur
- [ ] Can send user messages
- [ ] Can send system triggers
- [ ] Inner thoughts show IM scores
- [ ] AI responds in conversation panel

If all checked ✅, you're ready to explore!

## 🚀 Have Fun!

This demo showcases cutting-edge research in AI conversation. Explore, experiment, and see how AI can be proactive, thoughtful, and context-aware!

---

**Need Help?** Open an issue on GitHub or check the troubleshooting section in README.md
