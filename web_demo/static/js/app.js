/**
 * Thoughtful Agents Web Demo - Enhanced Client-side JavaScript
 *
 * Handles Server-Sent Events (SSE) for real-time updates, multi-user support,
 * and system triggers for proactive agent behavior.
 */

// UI Elements
const startBtn = document.getElementById('startBtn');
const sendUserBtn = document.getElementById('sendUserBtn');
const triggerBtn = document.getElementById('triggerBtn');
const speakerSelect = document.getElementById('speakerSelect');
const userInput = document.getElementById('userInput');
const triggerPreset = document.getElementById('triggerPreset');
const triggerInput = document.getElementById('triggerInput');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const memoryContent = document.getElementById('memoryContent');
const conversationContent = document.getElementById('conversationContent');
const thoughtsContent = document.getElementById('thoughtsContent');
const memoryCount = document.getElementById('memoryCount');
const turnCount = document.getElementById('turnCount');
const thoughtCount = document.getElementById('thoughtCount');

// State
let eventSource = null;
let isRunning = false;
let memoryItemCount = 0;
let currentTurn = 0;
let thoughtItemCount = 0;

// Initialize event listeners
startBtn.addEventListener('click', startDemo);
sendUserBtn.addEventListener('click', sendUserMessage);
triggerBtn.addEventListener('click', sendTrigger);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendUserMessage();
    }
});

triggerInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendTrigger();
    }
});

triggerPreset.addEventListener('change', (e) => {
    if (e.target.value) {
        triggerInput.value = e.target.value;
    }
});

/**
 * Start the demo scenario
 */
async function startDemo() {
    if (isRunning) {
        return;
    }

    try {
        // Disable start button
        startBtn.disabled = true;
        startBtn.textContent = '⏳ Starting...';

        // Clear previous content
        clearPanels();

        // Reset counters
        memoryItemCount = 0;
        currentTurn = 0;
        thoughtItemCount = 0;
        updateCounters();

        // Update status
        updateStatus('Starting demo...', 'active');

        // Start the demo
        const response = await fetch('/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to start demo');
        }

        // Connect to SSE
        connectToEvents();

        isRunning = true;
        startBtn.textContent = '▶️ Demo Running';
        sendUserBtn.disabled = false;
        triggerBtn.disabled = false;

    } catch (error) {
        console.error('Error starting demo:', error);
        updateStatus('Error starting demo', 'error');
        startBtn.disabled = false;
        startBtn.textContent = '▶️ Start Demo';
    }
}

/**
 * Connect to Server-Sent Events stream
 */
function connectToEvents() {
    // Close existing connection if any
    if (eventSource) {
        eventSource.close();
    }

    eventSource = new EventSource('/events');

    eventSource.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            handleEvent(data);
        } catch (error) {
            console.error('Error parsing event data:', error);
        }
    };

    eventSource.onerror = (error) => {
        console.error('SSE connection error:', error);
        if (eventSource.readyState === EventSource.CLOSED) {
            updateStatus('Connection closed', 'error');
        }
    };
}

/**
 * Handle incoming events from the server
 */
function handleEvent(event) {
    console.log('Event received:', event);

    switch (event.type) {
        case 'scenario_started':
            handleScenarioStarted(event.data);
            break;
        case 'memory_initialized':
            handleMemoryInitialized(event.data);
            break;
        case 'agent_message':
            handleAgentMessage(event.data);
            break;
        case 'human_message':
            handleHumanMessage(event.data);
            break;
        case 'system_message':
            handleSystemMessage(event.data);
            break;
        case 'system_trigger':
            handleSystemTrigger(event.data);
            break;
        case 'inner_thought':
            handleInnerThought(event.data);
            break;
        case 'scenario_completed':
            handleScenarioCompleted(event.data);
            break;
        default:
            console.log('Unknown event type:', event.type);
    }
}

/**
 * Handle scenario started event
 */
function handleScenarioStarted(data) {
    updateStatus(`Running: ${data.scenario}`, 'active');

    // Add scenario banner to conversation
    const banner = document.createElement('div');
    banner.className = 'scenario-banner';
    banner.innerHTML = `
        <h3>🚀 Scenario Started</h3>
        <p><strong>${data.scenario}</strong></p>
        <p>Time: ${data.time}</p>
        <p>Participants: ${data.participants.join(', ')}</p>
    `;
    conversationContent.innerHTML = '';
    conversationContent.appendChild(banner);
}

/**
 * Handle memory initialization
 */
function handleMemoryInitialized(data) {
    memoryContent.innerHTML = '';

    data.memory_items.forEach((item, index) => {
        const memoryItem = document.createElement('div');
        memoryItem.className = 'memory-item';

        const header = document.createElement('div');
        header.className = 'memory-item-header';
        header.innerHTML = `
            <span class="memory-id">KNO #${index + 1}</span>
        `;

        const content = document.createElement('div');
        content.textContent = item;

        memoryItem.appendChild(header);
        memoryItem.appendChild(content);
        memoryContent.appendChild(memoryItem);
    });

    memoryItemCount = data.memory_items.length;
    updateCounters();
}

/**
 * Handle agent message
 */
function handleAgentMessage(data) {
    addMessage('agent', data.speaker, data.content, data.turn);
    currentTurn = data.turn;
    updateCounters();
}

/**
 * Handle human message
 */
function handleHumanMessage(data) {
    addMessage('human', data.speaker, data.content, data.turn);
    currentTurn = data.turn;
    updateCounters();
}

/**
 * Handle system message
 */
function handleSystemMessage(data) {
    addMessage('system', 'System', data.content, data.turn);
}

/**
 * Handle system trigger
 */
function handleSystemTrigger(data) {
    addMessage('system', '⚙️ System Trigger', data.content, data.turn);
}

/**
 * Add a message to the conversation panel
 */
function addMessage(type, speaker, content, turn) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;

    const icon = type === 'agent' ? '🤖' : type === 'human' ? '👤' : '⚙️';

    messageDiv.innerHTML = `
        <div class="message-header">
            <span class="message-speaker">${icon} ${escapeHtml(speaker)}</span>
            <span class="message-turn">Turn ${turn}</span>
        </div>
        <div class="message-content">${escapeHtml(content)}</div>
    `;

    conversationContent.appendChild(messageDiv);
    conversationContent.scrollTop = conversationContent.scrollHeight;
}

/**
 * Handle inner thought event
 */
function handleInnerThought(data) {
    const thoughtDiv = document.createElement('div');
    thoughtDiv.className = 'thought-item';

    thoughtDiv.innerHTML = `
        <div class="thought-header">
            <span class="thought-turn">Turn ${data.turn}</span>
            <span class="thought-score">IM: ${data.intrinsic_motivation.toFixed(2)}</span>
        </div>
        <div class="thought-content">${escapeHtml(data.thought)}</div>
    `;

    thoughtsContent.appendChild(thoughtDiv);
    thoughtsContent.scrollTop = thoughtsContent.scrollHeight;

    thoughtItemCount++;
    updateCounters();
}

/**
 * Handle scenario completed event
 */
function handleScenarioCompleted(data) {
    updateStatus('Demo completed', 'active');

    const banner = document.createElement('div');
    banner.className = 'completion-banner';
    banner.innerHTML = `
        <h3>🏁 Scenario Completed</h3>
        <p>Total turns: ${data.total_turns}</p>
        <p>Assistant participated: ${data.assistant_turns} times</p>
    `;
    conversationContent.appendChild(banner);
    conversationContent.scrollTop = conversationContent.scrollHeight;

    // Re-enable start button
    startBtn.disabled = false;
    startBtn.textContent = '🔄 Restart Demo';
    isRunning = false;
}

/**
 * Send a user message
 */
async function sendUserMessage() {
    const message = userInput.value.trim();
    const speaker = speakerSelect.value;

    if (!message) {
        alert('Please enter a message');
        return;
    }

    if (!isRunning) {
        alert('Please start the demo first');
        return;
    }

    try {
        sendUserBtn.disabled = true;
        sendUserBtn.textContent = 'Sending...';

        const response = await fetch('/trigger', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                speaker: speaker,
                type: 'user'
            })
        });

        if (!response.ok) {
            throw new Error('Failed to send message');
        }

        // Clear input
        userInput.value = '';

    } catch (error) {
        console.error('Error sending message:', error);
        alert('Failed to send message: ' + error.message);
    } finally {
        sendUserBtn.disabled = false;
        sendUserBtn.textContent = 'Send';
    }
}

/**
 * Send a system trigger
 */
async function sendTrigger() {
    let message = triggerInput.value.trim();

    if (!message) {
        alert('Please enter a trigger or select a preset');
        return;
    }

    if (!isRunning) {
        alert('Please start the demo first');
        return;
    }

    try {
        triggerBtn.disabled = true;
        triggerBtn.textContent = 'Sending...';

        // Try to parse as JSON to format it nicely
        try {
            const jsonObj = JSON.parse(message);
            message = `🚨 VEHICLE SYSTEM ALERT: ${JSON.stringify(jsonObj)}`;
        } catch (e) {
            // If not JSON, use as-is
            message = `🚨 SYSTEM TRIGGER: ${message}`;
        }

        const response = await fetch('/trigger', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                type: 'system'
            })
        });

        if (!response.ok) {
            throw new Error('Failed to send trigger');
        }

        // Clear input and reset preset
        triggerInput.value = '';
        triggerPreset.value = '';

    } catch (error) {
        console.error('Error sending trigger:', error);
        alert('Failed to send trigger: ' + error.message);
    } finally {
        triggerBtn.disabled = false;
        triggerBtn.textContent = 'Send Trigger';
    }
}

/**
 * Update status indicator
 */
function updateStatus(text, state) {
    statusText.textContent = text;
    statusDot.className = 'status-dot';

    if (state === 'active') {
        statusDot.classList.add('active');
    } else if (state === 'error') {
        statusDot.classList.add('error');
    }
}

/**
 * Update counters
 */
function updateCounters() {
    memoryCount.textContent = `${memoryItemCount} items`;
    turnCount.textContent = `Turn ${currentTurn}`;
    thoughtCount.textContent = `${thoughtItemCount} thoughts`;
}

/**
 * Clear all panels
 */
function clearPanels() {
    memoryContent.innerHTML = '<div class="empty-state"><p>🧠 Loading memory...</p></div>';
    conversationContent.innerHTML = '<div class="empty-state"><p>📝 Loading conversation...</p></div>';
    thoughtsContent.innerHTML = '<div class="empty-state"><p>🤔 Loading thoughts...</p></div>';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize status and disable buttons
updateStatus('Ready', '');
sendUserBtn.disabled = true;
triggerBtn.disabled = true;
