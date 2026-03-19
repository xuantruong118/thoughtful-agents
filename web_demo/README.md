# Web Demo UI - Proactive Conversational Agents with Inner Thoughts

## 🎯 Tổng Quan / Overview

Web Demo UI này được xây dựng dựa trên kiến trúc của paper [Proactive Conversational Agents with Inner Thoughts](https://arxiv.org/pdf/2501.00383) (CHI 2025), với các tính năng đặc thù cho xe hơi (vehicle assistant).

This Web Demo UI is built based on the architecture from the paper [Proactive Conversational Agents with Inner Thoughts](https://arxiv.org/pdf/2501.00383) (CHI 2025), with vehicle-specific features.

## 🏗 Kiến Trúc / Architecture

### Layout 3+1 Cột / 3+1 Column Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    Control Panel (+1)                        │
│  • Start/Restart Demo                                        │
│  • User Message Input (Multi-speaker)                        │
│  • System Trigger Input (Vehicle Events)                     │
└─────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────────┬──────────────────────────┐
│ Long-term    │   Conversation   │    Inner Thoughts        │
│ Memory (LTM) │   (Hội thoại)    │   (Suy nghĩ nội tâm)    │
│              │                  │                          │
│ • Knowledge  │  • User msgs     │  • Thought content      │
│ • Interests  │  • Agent msgs    │  • IM scores            │
│ • Patterns   │  • System events │  • References           │
└──────────────┴──────────────────┴──────────────────────────┘
```

### Tech Stack

- **Backend**: Flask (Python) with asyncio
- **Real-time**: Server-Sent Events (SSE) for live updates
- **Frontend**: Vanilla JavaScript (no framework needed)
- **Styling**: Custom CSS with Tailwind-inspired utilities
- **Communication**: REST API + SSE streaming

## 📦 Cài Đặt / Installation

### Yêu Cầu / Requirements

```bash
Python 3.8+
Flask 2.0+
thoughtful-agents package
OpenAI API key
```

### Các Bước Cài Đặt / Installation Steps

1. **Cài đặt dependencies / Install dependencies**:
```bash
cd /home/runner/work/thoughtful-agents/thoughtful-agents
pip install -r requirements.txt
```

2. **Thiết lập OpenAI API key / Set up OpenAI API key**:
```bash
export OPENAI_API_KEY=your_api_key_here
```

3. **Khởi động server / Start the server**:
```bash
cd web_demo
python app.py
```

4. **Mở trình duyệt / Open browser**:
```
http://localhost:5000
```

## 🚀 Cách Sử Dụng / Usage Guide

### 1. Khởi Động Demo / Start Demo

Click nút **"▶️ Start Demo"** để:
- Khởi tạo conversation context
- Tạo các participants (Driver, Passenger A, Passenger B, AI Assistant)
- Load Long-term Memory của AI
- Chạy scenario demo tự động

Click **"▶️ Start Demo"** button to:
- Initialize conversation context
- Create participants (Driver, Passenger A, Passenger B, AI Assistant)
- Load AI's Long-term Memory
- Run automatic demo scenario

### 2. Gửi Tin Nhắn Người Dùng / Send User Messages

**Mục đích / Purpose**: Giả lập hội thoại nhiều người trên xe

**Steps**:
1. Chọn người nói từ dropdown (Driver / Passenger A / Passenger B)
2. Nhập tin nhắn vào ô input
3. Click "📤 Send Message" hoặc nhấn Enter

**Ví dụ / Examples**:
```
Speaker: Passenger A
Message: "What do you think about electric cars?"

Speaker: Driver
Message: "I'm feeling hungry, any suggestions?"
```

### 3. Gửi System Trigger / Send System Triggers

**Mục đích / Purpose**: Kích hoạt phản ứng chủ động (proactive) của AI dựa trên sự kiện xe

**Cách sử dụng / Usage**:

#### Option A: Sử dụng Preset / Use Presets
1. Chọn một preset từ dropdown:
   - ⛽ Low Fuel (15%, 45km range)
   - 🛞 Low Tire Pressure
   - 🌧️ Heavy Rain
   - 🚗 Traffic Jam
   - 🌡️ High Temperature
2. Click "⚡ Send System Trigger"

#### Option B: Custom JSON Trigger
1. Nhập JSON vào ô "Custom Trigger":
```json
{"event": "low_fuel", "level": "15%", "range": "45km"}
```
2. Click "⚡ Send System Trigger"

**Ví dụ Custom Triggers / Custom Trigger Examples**:

```json
// Cảnh báo nhiên liệu thấp / Low fuel warning
{"event": "low_fuel", "level": "10%", "range": "30km"}

// Áp suất lốp thấp / Low tire pressure
{"event": "tire_pressure_low", "tire": "front_right", "pressure": "25 PSI"}

// Thời tiết xấu / Bad weather
{"event": "weather_change", "condition": "heavy_rain", "visibility": "low"}

// Tắc đường / Traffic jam
{"event": "traffic_jam", "location": "Highway 1", "delay": "20 minutes"}

// Nhiệt độ cao / High temperature
{"event": "temperature_high", "cabin_temp": "38°C", "outside_temp": "35°C"}

// Nhắc nhở bảo trì / Maintenance reminder
{"event": "maintenance_due", "type": "oil_change", "due_in": "500km"}
```

## 🎨 Các Thành Phần UI / UI Components

### Cột 1: Long-term Memory (Bộ Nhớ Dài Hạn)

**Hiển thị / Displays**:
- Knowledge (KNO #): Kiến thức đã học
- Patterns: Thói quen người dùng
- Preferences: Sở thích

**Ví dụ / Examples**:
```
KNO #1: Driver Minh refuels every day at 8:30 AM
KNO #2: Preferred gas station: Petrolimex on Nguyễn Huệ St
KNO #3: Likes Vietnamese food, especially phở
```

### Cột 2: Conversation (Hội Thoại)

**Hiển thị / Displays**:
- 🟢 Human messages (green) - Tin nhắn người dùng
- 🔵 Agent messages (blue) - Phản hồi AI
- 🟡 System events (orange) - Sự kiện hệ thống

**Tính năng / Features**:
- Turn numbers for reference
- Speaker identification
- Color-coded by message type
- Scenario banners

### Cột 3: Inner Thoughts (Suy Nghĩ Nội Tâm)

**Hiển thị / Displays**:
- Thought content - Nội dung suy nghĩ
- IM Score (1-5) - Điểm động lực nội tại
- Turn reference - Số thứ tự turn

**IM Score Interpretation**:
- **1.0-2.0**: Very low motivation (won't speak)
- **2.5-3.5**: Moderate motivation (may speak if appropriate)
- **3.5-4.5**: High motivation (likely to speak)
- **4.5-5.0**: Very high motivation (will interrupt if needed)

## 🔧 Chi Tiết Kỹ Thuật / Technical Details

### Event Types

1. **scenario_started**: Demo initialization
2. **memory_initialized**: LTM loaded
3. **human_message**: User sends message
4. **agent_message**: AI responds
5. **system_message**: System events
6. **system_trigger**: Vehicle triggers
7. **inner_thought**: AI generates thought with IM score
8. **scenario_completed**: Demo finished

### Workflow - Luồng A: User Trigger

```
User sends message
  → Update Conversation panel
  → Backend retrieves from LTM
  → LLM generates Inner Thoughts
  → Push to Inner Thoughts panel via SSE
  → If IM score > threshold: AI speaks
  → Update Conversation panel
```

### Workflow - Luồng B: System Trigger (QUAN TRỌNG!)

```
System event (e.g., low fuel)
  → NOT displayed as regular message
  → Backend receives trigger
  → LLM deliberates (Nghiền ngẫm)
    → Checks vehicle state
    → Retrieves relevant LTM
    → Generates Inner Thoughts
  → Push thoughts to UI
  → If Priority Score > threshold
    → AI proactively interjects
    → Update Conversation panel
```

### SSE Connection

```javascript
EventSource: /events
Heartbeat: Every 30 seconds
Auto-reconnect: On connection loss
Format: JSON data stream
```

## 🎓 Các Tình Huống Sử Dụng / Use Cases

### Scenario 1: Multi-Party Conversation

```
Passenger A: "Have you seen the new Vinfast cars?"
  → AI observes, generates thoughts
  → Retrieves knowledge about car brands
  → IM score: 3.8 (moderate-high)
  → AI: "Yes! Vinfast VF8 is their electric SUV..."
```

### Scenario 2: Proactive Low Fuel Alert

```
System Trigger: {"event": "low_fuel", "level": "15%"}
  → AI retrieves memory: Driver refuels at 8:30 AM daily
  → AI checks time: Currently 8:25 AM
  → AI checks location: Near usual gas station
  → Inner Thought (IM: 4.5): "Time for usual refuel, low fuel"
  → AI proactively speaks: "I notice fuel is at 15%. Your usual Petrolimex station is 1.2km away..."
```

### Scenario 3: Context-Aware Suggestion

```
System Trigger: {"event": "traffic_jam", "delay": "20 minutes"}
User (Driver): "I'm hungry"
  → AI combines: Traffic delay + Hunger + Location
  → AI retrieves: Driver likes phở
  → Inner Thought (IM: 4.2): "Stuck in traffic, user hungry, Phở 24 nearby"
  → AI: "Since we're stuck in traffic, there's a Phở 24 0.5km from here. Would you like me to navigate there?"
```

## 🛠 Tùy Chỉnh / Customization

### Modify Proactivity Config

Edit `app.py`:
```python
assistant = UIAgent(name="Smart Vehicle Assistant", proactivity_config={
    'im_threshold': 2.5,  # Lower = more proactive
    'system1_prob': 0.4,  # 0-1, higher = more intuitive responses
    'interrupt_threshold': 2.8  # Lower = interrupts more
})
```

### Add More Memory

```python
assistant_memory = """
Additional knowledge:
- Driver's favorite music: Jazz
- Regular destinations: Office (9 AM), Gym (6 PM)
- Coffee preference: Cappuccino from Highland Coffee
"""
```

### Create Custom Presets

Edit `templates/index.html`:
```html
<option value='{"event": "custom_event", "param": "value"}'>
    🎵 Your Custom Event
</option>
```

## 📊 Monitoring và Debugging / Monitoring & Debugging

### Browser Console

Mở Developer Tools (F12) để xem:
- SSE events in real-time
- Error messages
- Network requests

### Server Logs

Terminal sẽ hiển thị:
- Incoming requests
- Event emissions
- Agent thought process (if verbose=True)

## 🐛 Khắc Phục Sự Cố / Troubleshooting

### Problem: Demo không khởi động / Demo won't start

**Solutions**:
1. Check OpenAI API key: `echo $OPENAI_API_KEY`
2. Check terminal for errors
3. Verify Flask is running on port 5000
4. Try `pip install --upgrade thoughtful-agents`

### Problem: SSE connection fails

**Solutions**:
1. Hard refresh browser (Ctrl+Shift+R)
2. Check browser console for errors
3. Verify port 5000 is not blocked
4. Try different browser

### Problem: Inner Thoughts không hiện / Inner Thoughts not showing

**Possible causes**:
1. IM scores too low (< threshold)
2. SSE connection lost
3. OpenAI API rate limit
4. Check browser console and server logs

### Problem: System Trigger không hoạt động / System Trigger not working

**Solutions**:
1. Verify JSON format is valid
2. Check that demo is running
3. Look for error messages in console
4. Try a preset trigger first

## 🔮 Tính Năng Tương Lai / Future Enhancements

### Planned Features

1. **Memory Editing UI**
   - Add/edit/delete memory items
   - Import/export memory profiles

2. **Reference Tags Linking**
   - CON# links to conversation messages
   - KNO# links to knowledge items
   - Click to highlight referenced content

3. **Thought Graph Visualization**
   - Visual representation of thought process
   - Show relationships between thoughts
   - IM score heatmap

4. **Recording & Playback**
   - Record entire sessions
   - Replay conversations
   - Export to various formats (JSON, CSV, Markdown)

5. **Voice Integration**
   - Voice input for messages
   - Text-to-speech for AI responses
   - Multilingual support

6. **Advanced Vehicle Features**
   - Real vehicle API simulation
   - GPS/location integration
   - Real-time traffic data
   - Weather API integration

7. **WebSocket Support**
   - Bidirectional communication
   - Lower latency
   - Real-time collaboration

## 📚 Tài Liệu Tham Khảo / References

- [CHI 2025 Paper](https://arxiv.org/pdf/2501.00383)
- [Thoughtful Agents Framework](https://github.com/xybruceliu/thoughtful-agents)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Server-Sent Events Spec](https://html.spec.whatwg.org/multipage/server-sent-events.html)

## 🤝 Đóng Góp / Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

Apache 2.0 License - see LICENSE file for details

## 📧 Liên Hệ / Contact

For questions or feedback:
- GitHub Issues: [thoughtful-agents/issues](https://github.com/xuantruong118/thoughtful-agents/issues)
- Email: Contact repository maintainers

---

**Lưu ý**: Demo này được thiết kế cho mục đích giáo dục và nghiên cứu. Để triển khai production, cần thêm các biện pháp bảo mật và tối ưu hóa.

**Note**: This demo is designed for educational and research purposes. For production deployment, additional security measures and optimizations are needed.
