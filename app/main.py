from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.chat import router as chat_router

app = FastAPI()

app.include_router(chat_router)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>ChatBot</title>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }

            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .chat-container {
                width: 100%;
                max-width: 700px;
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,0.1);
                box-shadow: 0 25px 45px rgba(0,0,0,0.3);
                overflow: hidden;
            }

            .chat-header {
                background: linear-gradient(90deg, #6C63FF, #48CAE4);
                padding: 20px 24px;
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .chat-header .avatar {
                width: 45px;
                height: 45px;
                background: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 22px;
            }

            .chat-header h2 {
                color: white;
                font-size: 20px;
                font-weight: 600;
            }

            .chat-header p {
                color: rgba(255,255,255,0.8);
                font-size: 12px;
            }

            .online-dot {
                width: 10px;
                height: 10px;
                background: #00ff88;
                border-radius: 50%;
                margin-left: auto;
                box-shadow: 0 0 6px #00ff88;
                animation: pulse 1.5s infinite;
            }

            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.4; }
            }

            #chat-box {
                height: 450px;
                overflow-y: auto;
                padding: 24px;
                display: flex;
                flex-direction: column;
                gap: 14px;
                scrollbar-width: thin;
                scrollbar-color: rgba(255,255,255,0.2) transparent;
            }

            #chat-box::-webkit-scrollbar { width: 5px; }
            #chat-box::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 10px; }

            .message {
                display: flex;
                gap: 10px;
                align-items: flex-end;
                animation: fadeIn 0.3s ease;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to   { opacity: 1; transform: translateY(0); }
            }

            .message.user { flex-direction: row-reverse; }

            .message .bubble {
                max-width: 75%;
                padding: 12px 16px;
                border-radius: 18px;
                font-size: 14px;
                line-height: 1.5;
                word-wrap: break-word;
            }

            .message.user .bubble {
                background: linear-gradient(135deg, #6C63FF, #48CAE4);
                color: white;
                border-bottom-right-radius: 4px;
            }

            .message.bot .bubble {
                background: rgba(255,255,255,0.1);
                color: #e0e0e0;
                border-bottom-left-radius: 4px;
                border: 1px solid rgba(255,255,255,0.1);
            }

            .message .icon {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
                flex-shrink: 0;
            }

            .message.user .icon { background: linear-gradient(135deg, #6C63FF, #48CAE4); }
            .message.bot  .icon { background: rgba(255,255,255,0.1); }

            .typing {
                display: flex;
                gap: 5px;
                align-items: center;
                padding: 12px 16px;
                background: rgba(255,255,255,0.1);
                border-radius: 18px;
                border-bottom-left-radius: 4px;
                width: fit-content;
            }

            .typing span {
                width: 8px;
                height: 8px;
                background: #aaa;
                border-radius: 50%;
                animation: bounce 1.2s infinite;
            }

            .typing span:nth-child(2) { animation-delay: 0.2s; }
            .typing span:nth-child(3) { animation-delay: 0.4s; }

            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50%       { transform: translateY(-6px); background: #6C63FF; }
            }

            .chat-input {
                display: flex;
                gap: 10px;
                padding: 16px 24px;
                background: rgba(0,0,0,0.2);
                border-top: 1px solid rgba(255,255,255,0.08);
            }

            #user-input {
                flex: 1;
                padding: 12px 18px;
                border-radius: 30px;
                border: 1px solid rgba(255,255,255,0.15);
                background: rgba(255,255,255,0.08);
                color: white;
                font-size: 14px;
                outline: none;
                transition: border 0.3s;
            }

            #user-input::placeholder { color: rgba(255,255,255,0.4); }
            #user-input:focus { border-color: #6C63FF; }

            #send-btn {
                width: 48px;
                height: 48px;
                border-radius: 50%;
                border: none;
                background: linear-gradient(135deg, #6C63FF, #48CAE4);
                color: white;
                font-size: 20px;
                cursor: pointer;
                transition: transform 0.2s, opacity 0.2s;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            #send-btn:hover { transform: scale(1.1); opacity: 0.9; }
            #send-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <div class="avatar">🤖</div>
                <div>
                    <h2>AI Assistant</h2>
                    <p>Powered by OpenAI</p>
                </div>
                <div class="online-dot"></div>
            </div>

            <div id="chat-box"></div>

            <div class="chat-input">
                <input id="user-input" placeholder="Type a message..." autocomplete="off" />
                <button id="send-btn" onclick="sendMessage()">➤</button>
            </div>
        </div>

        <script>
            let history = [];

            function appendMessage(role, text) {
                const chatBox = document.getElementById("chat-box");
                const div = document.createElement("div");
                div.className = `message ${role}`;
                div.innerHTML = `
                    <div class="icon">${role === "user" ? "🧑" : "🤖"}</div>
                    <div class="bubble">${text}</div>
                `;
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function showTyping() {
                const chatBox = document.getElementById("chat-box");
                const div = document.createElement("div");
                div.className = "message bot";
                div.id = "typing-indicator";
                div.innerHTML = `
                    <div class="icon">🤖</div>
                    <div class="typing"><span></span><span></span><span></span></div>
                `;
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function removeTyping() {
                const el = document.getElementById("typing-indicator");
                if (el) el.remove();
            }

            async function sendMessage() {
                const input = document.getElementById("user-input");
                const btn = document.getElementById("send-btn");
                const userText = input.value.trim();
                if (!userText) return;

                appendMessage("user", userText);
                history.push({ role: "user", content: userText });
                input.value = "";
                btn.disabled = true;
                showTyping();

                try {
                    const res = await fetch("/chat", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ messages: history })
                    });

                    const data = await res.json();
                    removeTyping();

                    // ✅ Handles both "reply" and "response" field names
                    const botReply = data.reply || data.response || "Sorry, I could not get a response.";
                    appendMessage("bot", botReply);
                    history.push({ role: "assistant", content: botReply });

                } catch (err) {
                    removeTyping();
                    appendMessage("bot", "⚠️ Error connecting to server.");
                } finally {
                    btn.disabled = false;
                    input.focus();
                }
            }

            document.getElementById("user-input").addEventListener("keypress", e => {
                if (e.key === "Enter") sendMessage();
            });
        </script>
    </body>
    </html>
    """