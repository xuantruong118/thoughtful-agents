/**
 * Thoughtful Agents Web Demo - Client-side JavaScript
 *
 * Handles Server-Sent Events (SSE) for real-time updates and UI interactions.
 */

// UI Elements
const startBtn = document.getElementById('startBtn');
const triggerBtn = document.getElementById('triggerBtn');
const triggerInput = document.getElementById('triggerInput');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const memoryContent = document.getElementById('memoryContent');
const conversationContent = document.getElementById('conversationContent');
const thoughtsContent = document.getElementById('thoughtsContent');

// State
let eventSource = null;
let isRunning = false;

// Initialize event listeners
startBtn.addEventListener('click', startDemo);
triggerBtn.addEventListener('click', sendTrigger);
triggerInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendTrigger();
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
        memoryItem.textContent = item;
        memoryContent.appendChild(memoryItem);
    });
}

/**
 * Handle agent message
 */
function handleAgentMessage(data) {
    addMessage('agent', data.speaker, data.content, data.turn);
}

/**
 * Handle human message
 */
function handleHumanMessage(data) {
    addMessage('human', data.speaker, data.content, data.turn);
}

/**
 * Handle system message
 */
function handleSystemMessage(data) {
    addMessage('system', 'System', data.content, data.turn);
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
            <span>${icon} ${speaker}</span>
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
    startBtn.textContent = '▶️ Restart Demo';
    isRunning = false;
}

/**
 * Send a custom trigger message
 */
async function sendTrigger() {
    const message = triggerInput.value.trim();

    if (!message) {
        alert('Please enter a message');
        return;
    }

    if (!isRunning) {
        alert('Please start the demo first');
        return;
    }

    try {
        triggerBtn.disabled = true;
        triggerBtn.textContent = 'Sending...';

        const response = await fetch('/trigger', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error('Failed to send trigger');
        }

        // Clear input
        triggerInput.value = '';

        // Add user-triggered message to conversation
        addMessage('system', 'User Trigger', message, '-');

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
 * Clear all panels
 */
function clearPanels() {
    memoryContent.innerHTML = '<div class="empty-state"><p>Loading memory...</p></div>';
    conversationContent.innerHTML = '<div class="empty-state"><p>Loading conversation...</p></div>';
    thoughtsContent.innerHTML = '<div class="empty-state"><p>Loading thoughts...</p></div>';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize status
updateStatus('Ready', '');
