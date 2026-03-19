# Quick Start Guide - Web Demo

Get the Thoughtful Agents web demo running in 5 minutes!

## Step 1: Setup (2 minutes)

```bash
# Clone repository (if not already done)
git clone https://github.com/xuantruong118/thoughtful-agents.git
cd thoughtful-agents

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'
```

## Step 2: Run the Demo (1 minute)

```bash
# Start the web server
cd web_demo
python app.py
```

You should see:
```
🚗 Thoughtful Agents Web Demo 🚗
======================================
Starting Flask server...
Open http://localhost:5000 in your browser to view the demo
```

## Step 3: View in Browser (2 minutes)

1. Open http://localhost:5000
2. Click "▶️ Start Demo"
3. Watch the three panels update in real-time:
   - **Memory**: Agent's learned patterns
   - **Conversation**: Real-time dialogue
   - **Inner Thoughts**: Cognitive process with scores

## What You'll See

### Scenario: Vehicle Assistant with Low Fuel Alert

The demo shows a smart vehicle assistant that:
1. **Remembers** the driver refuels at 8:30 AM daily
2. **Responds** proactively when fuel is low
3. **Suggests** the best gas station based on patterns
4. **Thinks** before speaking (you can see the thoughts!)

### Key Features

- 🧠 **Inner Thoughts**: See the AI's cognitive process
- 💾 **Memory System**: Agent remembers preferences and patterns
- 🤖 **Proactive Behavior**: Doesn't wait to be asked
- 📊 **Intrinsic Motivation**: Scores show why agent speaks
- ⚡ **Real-Time**: Updates stream live via Server-Sent Events

## Try Custom Triggers

While the demo is running, try these:

```
Traffic congestion on Nguyễn Huệ Street
```

```
Driver mentions feeling tired
```

```
Need a restaurant recommendation
```

The agent will think about your trigger and respond appropriately!

## What's Next?

### Run the Extended Scenario

Want to see more features? Try the extended scenario with restaurants and museums:

```bash
cd ..  # Back to repository root
python examples/vehicle_assistant_extended.py
```

This includes:
- 🍽️ Restaurant recommendations
- 🏛️ Museum suggestions
- 🌏 Location-aware responses
- 🗣️ Bilingual support (Vietnamese/English)

### Explore the Code

- **Web UI**: `web_demo/app.py`
- **Frontend**: `web_demo/static/` and `web_demo/templates/`
- **Scenarios**: `examples/vehicle_assistant_*.py`
- **Framework**: `thoughtful_agents/`

### Read the Docs

- 📖 [Full Testing Guide](../docs/TESTING_GUIDE.md)
- 📚 [Web Demo README](README.md)
- 🔬 [Research Paper](https://arxiv.org/pdf/2501.00383)

## Troubleshooting

**Demo won't start?**
- Run: `bash scripts/test_web_demo.sh`
- This checks your setup and tells you what's missing

**No updates appearing?**
- Check your OpenAI API key is set
- Look at the Flask console for errors

**SSE connection issues?**
- Try a different browser (Chrome works best)
- Check no firewall is blocking port 5000

## Need Help?

- Check the [Testing Guide](../docs/TESTING_GUIDE.md) for detailed instructions
- Review the [Web Demo README](README.md) for technical details
- Look at existing scenarios in `examples/` for code examples

---

**Enjoy exploring proactive AI agents with inner thoughts! 🚀**
