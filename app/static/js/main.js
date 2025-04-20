let selectedUser = null;
let ably;
let channel;

// Initialize Ably with token authentication
ably = new Ably.Realtime({
    authUrl: '/ably/token',
    clientId: currentUser.username
});
ably.connection.on('connected', () => {
    console.log('Connected to Ably');
});

function startChat(username) {
    if (username === currentUser.username) {
        alert("You cannot chat with yourself!");
        return;
    }
    selectedUser = username;
    document.getElementById("chat-header").textContent = `Chatting with: ${username}`;
    document.getElementById("chat-box").innerHTML = "";
    fetchChatHistory(username);

    // Subscribe to Ably channel for this conversation
    const channelName = `chat:${[currentUser.username, selectedUser].sort().join(':')}`;
    channel = ably.channels.get(channelName);
    channel.subscribe('message', (msg) => {
        displayMessage(msg.data);
    });
}

function fetchChatHistory(username) {
    fetch(`/chat/history/${username}`, {
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include"
    })
        .then(response => {
            if (!response.ok) throw new Error(`Failed to fetch chat history: ${response.statusText}`);
            return response.json();
        })
        .then(messages => {
            const chatBox = document.getElementById("chat-box");
            messages.forEach(displayMessage);
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => console.error("Error fetching chat history:", error));
}

function displayMessage(message) {
    if (
        (message.sender === currentUser.username && message.recipient === selectedUser) ||
        (message.sender === selectedUser && message.recipient === currentUser.username)
    ) {
        const chatBox = document.getElementById("chat-box");
        const msgWrapper = document.createElement("div");
        msgWrapper.classList.add("chat-wrapper");
        msgWrapper.classList.add(message.sender === currentUser.username ? "right" : "left");

        const msgBubble = document.createElement("div");
        msgBubble.classList.add("chat-bubble");
        // Show original message
        let content = `<strong>${message.sender}:</strong> ${message.content}`;
        // Show translated message if available Only show to recipient
        if (message.translated_content && message.recipient === currentUser.username) {
            content += `<br><em>Translated: ${message.translated_content}</em>`;
            if (message.audio_url) {
                content += `<br><button onclick="playAudio('${message.audio_url}')">🎵 Play Audio</button>`;
            }
        }
        msgBubble.innerHTML = content;

        msgWrapper.appendChild(msgBubble);
        chatBox.appendChild(msgWrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

function playAudio(audioUrl) {
    const audio = new Audio(audioUrl);
    audio.play().catch(error => {
        console.error("Audio playback error:", error);
        alert("Failed to play audio: " + error.message);
    });
}

function sendMessage() {
    if (!selectedUser) {
        alert("Please select a user to chat with!");
        return;
    }
    const messageInput = document.getElementById("messageInput");
    const message = messageInput.value.trim();
    if (!message) return;

    fetch('/chat/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ recipient: selectedUser, content: message })
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to send message');
        messageInput.value = "";
    })
    .catch(error => {
        console.error('Error sending message:', error);
        alert('Failed to send message');
    });
}

function startRecognition() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = false;
    recognition.interimResults = true;

    const sourceLang = currentUser.language;
    const langMap = {
        "en": "en-US",
        "ur": "ur-PK",
        "hi": "hi-IN",
        "es": "es-ES",
        "fr": "fr-FR",
        "ja": "ja-JP",  // Added Japanese
        "ru": "ru-RU"   // Added Russian
    };
    recognition.lang = langMap[sourceLang] || "en-US";

    recognition.onstart = function() {
        console.log(`🎤 Listening (${recognition.lang})...`);
    };

    recognition.onresult = function(event) {
        let interim = "";
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                document.getElementById("messageInput").value = event.results[i][0].transcript;
            } else {
                interim += event.results[i][0].transcript;
                document.getElementById("messageInput").value = interim;
            }
        }
    };

    recognition.onerror = function(event) {
        console.error("❌ Speech recognition error:", event.error);
        alert(`Speech recognition error: ${event.error}`);
        document.getElementById("messageInput").placeholder = "Type or speak your message...";
    };

    recognition.onend = function() {
        document.getElementById("messageInput").placeholder = "Type or speak your message...";
    };

    recognition.start();
}