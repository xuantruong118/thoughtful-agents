// Lecture Practice Coach Demo

let lectureEventSource = null;
let turnCount = 0;
let thoughtCount = 0;
let memoryCount = 0;

const startBtn = document.getElementById('start-btn');
const restartBtn = document.getElementById('restart-btn');
const statusBadge = document.getElementById('status-badge');
const messageInput = document.getElementById('message-input');
const sendMessageBtn = document.getElementById('send-message-btn');

const memoryContent = document.getElementById('memory-content');
const conversationContent = document.getElementById('conversation-content');
const thoughtsContent = document.getElementById('thoughts-content');

const memoryCountBadge = document.getElementById('memory-count');
const turnCountBadge = document.getElementById('turn-count');
const thoughtCountBadge = document.getElementById('thought-count');

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkLectureState();
});

function setupEventListeners() {
    startBtn.addEventListener('click', startLectureSession);
    restartBtn.addEventListener('click', startLectureSession);
    sendMessageBtn.addEventListener('click', sendPresenterMessage);

    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendPresenterMessage();
        }
    });
}

async function checkLectureState() {
    try {
        const response = await fetch('/lecture/state');
        const data = await response.json();

        if (data.running) {
            connectLectureEvents();
            setStatus('running');
        } else {
            setStatus('ready');
        }
    } catch (error) {
        console.error('Failed to check lecture state:', error);
    }
}

async function startLectureSession() {
    try {
        if (!lectureEventSource) {
            connectLectureEvents();
        }

        setStatus('starting');
        startBtn.disabled = true;

        resetUI();

        const response = await fetch('/lecture/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
            setStatus('running');
            restartBtn.style.display = 'inline-block';
            startBtn.style.display = 'none';
        } else {
            setStatus('error');
            startBtn.disabled = false;
        }
    } catch (error) {
        console.error('Failed to start lecture session:', error);
        setStatus('error');
        startBtn.disabled = false;
    }
}

function connectLectureEvents() {
    if (lectureEventSource) {
        lectureEventSource.close();
    }

    lectureEventSource = new EventSource('/lecture/events');

    lectureEventSource.onopen = () => {
        setStatus('running');
    };

    lectureEventSource.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            handleLectureEvent(data);
        } catch (error) {
            console.error('Error parsing lecture event:', error);
        }
    };

    lectureEventSource.onerror = (error) => {
        console.error('Lecture SSE error:', error);
        setTimeout(() => connectLectureEvents(), 3000);
    };
}

function handleLectureEvent(event) {
    switch (event.type) {
        case 'scenario_started':
            handleScenarioStarted(event.data);
            break;
        case 'memory_initialized':
            handleMemoryInitialized(event.data);
            break;
        case 'human_message':
            handleHumanMessage(event.data);
            break;
        case 'agent_message':
            handleAgentMessage(event.data);
            break;
        case 'inner_thought':
            handleInnerThought(event.data);
            break;
        case 'system_message':
            handleSystemMessage(event.data);
            break;
        case 'error':
            handleError(event.data);
            break;
        default:
            break;
    }
}

function handleScenarioStarted(data) {
    clearEmptyState(conversationContent);
    addScenarioBanner('🎬 Lecture practice session started');
    turnCount = 0;
    thoughtCount = 0;
    updateCounter(turnCountBadge, turnCount);
    updateCounter(thoughtCountBadge, thoughtCount);
}

function handleMemoryInitialized(data) {
    clearEmptyState(memoryContent);
    memoryCount = data.count || 0;
    updateCounter(memoryCountBadge, memoryCount);

    memoryContent.innerHTML = '';
    if (data.memories) {
        data.memories.forEach((memory, index) => addMemoryItem(index + 1, memory.content));
    }
}

function handleHumanMessage(data) {
    clearEmptyState(conversationContent);
    turnCount = data.turn || turnCount + 1;
    updateCounter(turnCountBadge, turnCount);
    addMessage('human', data.speaker, data.message, data.turn);
}

function handleAgentMessage(data) {
    clearEmptyState(conversationContent);
    turnCount = data.turn || turnCount + 1;
    updateCounter(turnCountBadge, turnCount);
    addMessage('agent', data.speaker, data.message, data.turn);
}

function handleInnerThought(data) {
    clearEmptyState(thoughtsContent);
    thoughtCount++;
    updateCounter(thoughtCountBadge, thoughtCount);
    addThought(data.turn, data.score, data.content);
}

function handleSystemMessage(data) {
    clearEmptyState(conversationContent);
    addScenarioBanner(data.message);
}

function handleError(data) {
    addSystemMessage('⚠️ Error: ' + data.message);
    setStatus('error');
}

function setStatus(status) {
    switch (status) {
        case 'starting':
            statusBadge.textContent = 'Starting...';
            statusBadge.className = 'status-badge running';
            break;
        case 'running':
            statusBadge.textContent = 'Running';
            statusBadge.className = 'status-badge running';
            startBtn.disabled = true;
            break;
        case 'error':
            statusBadge.textContent = 'Error';
            statusBadge.className = 'status-badge';
            statusBadge.style.background = 'var(--color-danger)';
            startBtn.disabled = false;
            break;
        default:
            statusBadge.textContent = 'Ready';
            statusBadge.className = 'status-badge';
            startBtn.disabled = false;
    }
}

function updateCounter(element, count) {
    element.textContent = count;
}

function clearEmptyState(container) {
    const emptyState = container.querySelector('.empty-state');
    if (emptyState) {
        emptyState.remove();
    }
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

function addSystemMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system';
    messageDiv.innerHTML = `
        <div class="message-content">${escapeHtml(text)}</div>
    `;
    conversationContent.appendChild(messageDiv);
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

async function sendPresenterMessage() {
    const message = messageInput.value.trim();

    if (!message) {
        alert('Please enter a message for the coach.');
        return;
    }

    try {
        sendMessageBtn.disabled = true;
        const response = await fetch('/lecture/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        if (response.ok) {
            messageInput.value = '';
        }
    } catch (error) {
        console.error('Failed to send message:', error);
        alert('Failed to send message');
    } finally {
        sendMessageBtn.disabled = false;
    }
}

function resetUI() {
    memoryContent.innerHTML = `
        <div class="empty-state">
            <p>🔄 Waiting for initialization...</p>
            <p class="empty-hint">Coach knowledge will appear here</p>
        </div>`;

    conversationContent.innerHTML = `
        <div class="empty-state">
            <p>👋 Start the session and speak to the coach</p>
            <p class="empty-hint">Messages will appear here</p>
        </div>`;

    thoughtsContent.innerHTML = `
        <div class="empty-state">
            <p>🤔 Coach thoughts will appear here</p>
            <p class="empty-hint">See why the AI decides to speak</p>
        </div>`;

    turnCount = 0;
    thoughtCount = 0;
    memoryCount = 0;
    updateCounter(turnCountBadge, turnCount);
    updateCounter(thoughtCountBadge, thoughtCount);
    updateCounter(memoryCountBadge, memoryCount);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
}

window.addEventListener('beforeunload', () => {
    if (lectureEventSource) {
        lectureEventSource.close();
    }
});
