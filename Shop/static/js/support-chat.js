// Support Chat WebSocket Handler
const userId = document.getElementById('user-id')?.dataset.userId;

if (userId) {
    // WebSocket connection
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const chatSocket = new WebSocket(
        protocol + '//' + window.location.host + '/ws/chat/' + userId + '/'
    );

    // DOM elements
    const supportBtn = document.getElementById('support-btn');
    const chatModal = document.getElementById('support-chat');
    const closeBtn = document.getElementById('close-chat');
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    // Open chat modal
    supportBtn.onclick = () => {
        chatModal.style.display = 'flex';
        chatInput.focus();
    };

    // Close chat modal
    closeBtn.onclick = () => {
        chatModal.style.display = 'none';
    };

    // Send message function
    function sendMessage() {
        const message = chatInput.value.trim();
        if (message) {
            chatSocket.send(JSON.stringify({
                'message': message,
                'type': 'support_request'
            }));
            
            // Display user's message immediately
            const messageDiv = document.createElement('div');
            messageDiv.className = 'user-message';
            messageDiv.textContent = message;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            chatInput.value = '';
        }
    }

    // Send message on button click
    sendBtn.onclick = sendMessage;

    // Send message on Enter key
    chatInput.onkeypress = (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    };

    // WebSocket event handlers
    chatSocket.onopen = () => {
        console.log('Support chat connected');
    };

    chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        const messageDiv = document.createElement('div');
        messageDiv.className = data.sender === 'user' ? 'user-message' : 'support-message';
        messageDiv.textContent = data.message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    chatSocket.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    chatSocket.onclose = (e) => {
        console.log('Support chat disconnected');
        if (e.code !== 1000) {
            // Attempt to reconnect after 3 seconds if connection was not closed normally
            setTimeout(() => {
                console.log('Attempting to reconnect...');
                location.reload();
            }, 3000);
        }
    };
}
