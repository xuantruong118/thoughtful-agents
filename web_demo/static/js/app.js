// Thoughtful Agents Web Demo - Client-Side JavaScript

// State
let eventSource = null;
let demoRunning = false;
let turnCount = 0;
let thoughtCount = 0;
let memoryCount = 0;

// DOM Elements
const startBtn = document.getElementById('start-btn');
const restartBtn = document.getElementById('restart-btn');
const statusBadge = document.getElementById('status-badge');
const speakerSelect = document.getElementById('speaker-select');
const messageInput = document.getElementById('message-input');
const sendMessageBtn = document.getElementById('send-message-btn');
const triggerPreset = document.getElementById('trigger-preset');
const triggerInput = document.getElementById('trigger-input');
const sendTriggerBtn = document.getElementById('send-trigger-btn');

// Content panels
const memoryContent = document.getElementById('memory-content');
const conversationContent = document.getElementById('conversation-content');
const thoughtsContent = document.getElementById('thoughts-content');

// Counters
const memoryCountBadge = document.getElementById('memory-count');
const turnCountBadge = document.getElementById('turn-count');
const thoughtCountBadge = document.getElementById('thought-count');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkServerState();
});

// Event Listeners
function setupEventListeners() {
    startBtn.addEventListener('click', startDemo);
    restartBtn.addEventListener('click', restartDemo);
    sendMessageBtn.addEventListener('click', sendUserMessage);
    sendTriggerBtn.addEventListener('click', sendSystemTrigger);

    // Enter key support
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendUserMessage();
        }
    });

    // Preset trigger selection
    triggerPreset.addEventListener('change', (e) => {
        if (e.target.value) {
            triggerInput.value = e.target.value;
        }
    });
}

// Check server state on load
async function checkServerState() {
    try {
        const response = await fetch('/state');
        const data = await response.json();

        if (data.running) {
            setStatus('running');
            connectToEventStream();
        }
    } catch (error) {
        console.error('Failed to check server state:', error);
    }
}

// Start demo
async function startDemo() {
    try {
        startBtn.disabled = true;
        setStatus('starting');

        const response = await fetch('/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
            setStatus('running');
            connectToEventStream();
        }
    } catch (error) {
        console.error('Failed to start demo:', error);
        setStatus('error');
        startBtn.disabled = false;
    }
}

// Restart demo
function restartDemo() {
    location.reload();
}

// Connect to Server-Sent Events
function connectToEventStream() {
    if (eventSource) {
        eventSource.close();
    }

    eventSource = new EventSource('/events');

    eventSource.onopen = () => {
        console.log('SSE connection established');
        setStatus('running');
    };

    eventSource.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            handleEvent(data);
        } catch (error) {
            console.error('Error parsing event:', error);
        }
    };

    eventSource.onerror = (error) => {
        console.error('SSE error:', error);
        setTimeout(() => {
            console.log('Reconnecting...');
            connectToEventStream();
        }, 3000);
    };
}

// Handle different event types
function handleEvent(event) {
    console.log('Event received:', event.type, event.data);

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
        case 'error':
            handleError(event.data);
            break;
    }
}

// Event Handlers
function handleScenarioStarted(data) {
    clearEmptyState(conversationContent);
    addScenarioBanner('🎬 Demo Scenario Started');
}

function handleMemoryInitialized(data) {
    clearEmptyState(memoryContent);
    memoryCount = data.count || 0;
    updateCounter(memoryCountBadge, memoryCount);

    if (data.memories) {
        data.memories.forEach((memory, index) => {
            addMemoryItem(index + 1, memory.content);
        });
    }
}

function handleAgentMessage(data) {
    clearEmptyState(conversationContent);
    turnCount = data.turn || turnCount + 1;
    updateCounter(turnCountBadge, turnCount);
    addMessage('agent', data.speaker, data.message, data.turn);
}

function handleHumanMessage(data) {
    clearEmptyState(conversationContent);
    turnCount = data.turn || turnCount + 1;
    updateCounter(turnCountBadge, turnCount);
    addMessage('human', data.speaker, data.message, data.turn);
}

function handleSystemMessage(data) {
    clearEmptyState(conversationContent);
    addScenarioBanner(data.message);
}

function handleSystemTrigger(data) {
    clearEmptyState(conversationContent);
    turnCount = data.turn || turnCount + 1;
    updateCounter(turnCountBadge, turnCount);
    addMessage('system', 'System Trigger', data.message, data.turn);
}

function handleInnerThought(data) {
    clearEmptyState(thoughtsContent);
    thoughtCount++;
    updateCounter(thoughtCountBadge, thoughtCount);
    addThought(data.turn, data.score, data.content);
}

function handleScenarioCompleted(data) {
    addScenarioBanner('✅ Demo Scenario Completed');
    setStatus('completed');
    startBtn.style.display = 'none';
    restartBtn.style.display = 'inline-block';
}

function handleError(data) {
    console.error('Error from server:', data.message);
    addSystemMessage('⚠️ Error: ' + data.message);
}

// UI Update Functions
function setStatus(status) {
    demoRunning = (status === 'running');

    switch (status) {
        case 'starting':
            statusBadge.textContent = 'Starting...';
            statusBadge.className = 'status-badge running';
            break;
        case 'running':
            statusBadge.textContent = 'Running';
            statusBadge.className = 'status-badge running';
            startBtn.style.display = 'none';
            break;
        case 'completed':
            statusBadge.textContent = 'Completed';
            statusBadge.className = 'status-badge';
            break;
        case 'error':
            statusBadge.textContent = 'Error';
            statusBadge.className = 'status-badge';
            statusBadge.style.background = 'var(--color-danger)';
            break;
        default:
            statusBadge.textContent = 'Ready';
            statusBadge.className = 'status-badge';
    }
}

function clearEmptyState(container) {
    const emptyState = container.querySelector('.empty-state');
    if (emptyState) {
        emptyState.remove();
    }
}

function updateCounter(element, count) {
    element.textContent = count;
}

function addMemoryItem(id, content) {
    const item = document.createElement('div');
    item.className = 'memory-item';
    item.innerHTML = `
        <div class="memory-item-header">
            <span class="memory-id">KNO #${id}</span>
        </div>
        <div class="memory-content">${escapeHtml(content)}</div>
    `;
    memoryContent.appendChild(item);
    scrollToBottom(memoryContent);
}

function addMessage(type, speaker, message, turn) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = `
        <div class="message-speaker">
            ${escapeHtml(speaker)}
            <span class="message-turn">#${turn || ''}</span>
        </div>
        <div class="message-content">${escapeHtml(message)}</div>
    `;
    conversationContent.appendChild(messageDiv);
    scrollToBottom(conversationContent);
}

function addScenarioBanner(text) {
    const banner = document.createElement('div');
    banner.className = 'scenario-banner';
    banner.textContent = text;
    conversationContent.appendChild(banner);
    scrollToBottom(conversationContent);
}

function addThought(turn, score, content) {
    const thought = document.createElement('div');
    thought.className = 'thought-item';
    thought.innerHTML = `
        <div class="thought-header">
            <span class="thought-turn">Turn #${turn || '?'}</span>
            <span class="thought-score">IM: ${score ? score.toFixed(1) : '?'}</span>
        </div>
        <div class="thought-content">${escapeHtml(content)}</div>
    `;
    thoughtsContent.appendChild(thought);
    scrollToBottom(thoughtsContent);
}

function scrollToBottom(element) {
    setTimeout(() => {
        element.scrollTop = element.scrollHeight;
    }, 100);
}

// User Actions
async function sendUserMessage() {
    const speaker = speakerSelect.value;
    const message = messageInput.value.trim();

    if (!message) {
        alert('Please enter a message');
        return;
    }

    try {
        sendMessageBtn.disabled = true;

        const response = await fetch('/trigger', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                speaker: speaker,
                message: message,
                type: 'user'
            })
        });

        if (response.ok) {
            messageInput.value = '';
            sendMessageBtn.disabled = false;
        }
    } catch (error) {
        console.error('Failed to send message:', error);
        alert('Failed to send message');
        sendMessageBtn.disabled = false;
    }
}

async function sendSystemTrigger() {
    const triggerText = triggerInput.value.trim();

    if (!triggerText) {
        alert('Please enter a trigger (JSON format)');
        return;
    }

    // Validate JSON
    try {
        JSON.parse(triggerText);
    } catch (error) {
        alert('Invalid JSON format. Please check your trigger input.');
        return;
    }

    try {
        sendTriggerBtn.disabled = true;

        const response = await fetch('/trigger', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: triggerText,
                type: 'system'
            })
        });

        if (response.ok) {
            triggerInput.value = '';
            triggerPreset.value = '';
            sendTriggerBtn.disabled = false;
        }
    } catch (error) {
        console.error('Failed to send trigger:', error);
        alert('Failed to send trigger');
        sendTriggerBtn.disabled = false;
    }
}

// Utility Functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (eventSource) {
        eventSource.close();
    }
});
