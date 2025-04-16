let ws = new WebSocket(`ws://${location.host}/ws/chat`);


async function sendMessage() {
    let input = document.getElementById("messageInput");
    let role = document.getElementById("role").value;
    let userLang = document.getElementById("userLang").value;

    if (input.value.trim() === "") return;

    let original = input.value;
    input.value = "Translating...";

    // Determine source and target languages based on role
    let sourceLang = userLang;
    let targetLang = role === "patient" ? "English" : "Urdu"; // or whatever default for counterpart

    // Call backend to get translation
    const response = await fetch("/translate", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            text: original,
            source_lang: sourceLang,
            target_lang: targetLang
        })
    });

    const data = await response.json();
    input.value = "";

    let payload = {
        role: role.charAt(0).toUpperCase() + role.slice(1), // Capitalize for display
        message: `${original}<br><em>${data.translated}</em>`
    };

    ws.send(JSON.stringify(payload));
}


ws.onmessage = function(event) {
    let chatBox = document.getElementById("chat-box");
    let data = JSON.parse(event.data);

    let msgWrapper = document.createElement("div");
    msgWrapper.classList.add("chat-wrapper");
    msgWrapper.classList.add(data.role === "Patient" ? "left" : "right");

    let msgBubble = document.createElement("div");
    msgBubble.classList.add("chat-bubble");
    msgBubble.innerHTML = `<strong>${data.role}:</strong> ${data.message}`;

    msgWrapper.appendChild(msgBubble);
    chatBox.appendChild(msgWrapper);
    chatBox.scrollTop = chatBox.scrollHeight;
};


// Voice recognition using browser's Web Speech API
function startRecognition() {
    const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;

    // 🧠 Get the selected source language
    const sourceLang = document.getElementById("userLang").value;

    // 🌐 Language map: convert readable name to browser lang code
    const langMap = {
        "English": "en-US",
        "Urdu": "ur-PK",
        "Hindi": "hi-IN",
        "Spanish": "es-ES"
    };

    recognition.lang = langMap[sourceLang] || "en-US";

    recognition.onstart = function () {
        console.log(`🎤 Listening (${recognition.lang})...`);
    };

    recognition.onresult = function (event) {
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

    recognition.onerror = function (event) {
        console.error("❌ Speech recognition error:", event.error);
    };

    recognition.start();
}
