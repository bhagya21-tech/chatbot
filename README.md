# 🧠 AI Mentor Chatbot

A personal AI mentor chatbot powered by **Groq (Llama 3.3 70B)**, built with **FastAPI** and **Python**. Runs in your browser, remembers your past conversations, and knows who you are through a personal profile system.

Built as a learning project while studying **Agentic AI, Chatbots, and MCP (Model Context Protocol)**.

---

## ✨ Features

- 💬 **Browser chat UI** — clean dark-themed interface, no terminal needed
- 🧠 **Persistent memory** — saves conversation history to JSON, remembers past sessions
- 👤 **User profile system** — stores your name, goals, and context, injected into every prompt
- ⚡ **Groq-powered** — uses Llama 3.3 70B for fast, high-quality responses
- 🖥️ **Terminal mode** — also works as a terminal chatbot (main.py)
- 🔒 **Secure** — API key stored in `.env`, never hardcoded

---

## 🏗️ Project Structure

```
ai-chatbot/
├── server.py              # FastAPI web server (5 routes)
├── main.py                # Terminal chatbot entry point
├── user_profile.json      # Your personal profile (edit this)
├── requirements.txt       # Python dependencies
├── .env.example           # Copy to .env and add your key
├── static/
│   └── index.html         # Browser chat UI
└── src/
    ├── config.py          # Loads settings from .env
    ├── memory.py          # Conversation history + save/load
    ├── client.py          # Groq API wrapper
    ├── profile.py         # User profile loader + injector
    └── ui.py              # Terminal UI (Rich)
```

---

## 🚀 Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/ai-chatbot.git
cd ai-chatbot
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
```bash
cp .env.example .env
```
Open `.env` and paste your Groq API key from [console.groq.com](https://console.groq.com)

```
GROQ_API_KEY=gsk_your_real_key_here
MODEL=llama-3.3-70b-versatile
SYSTEM_PROMPT=You are a personal mentor and expert teacher. Keep answers short and direct.
MAX_TOKENS=1024
```

### 5. Set up your profile
Edit `user_profile.json` with your name, goals, and context so the AI knows who you are.

---

## ▶️ Run

### Browser UI (recommended)
```bash
python -m uvicorn server:app --reload --port 8000
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Terminal mode
```bash
python main.py
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Llama 3.3 70B via Groq API |
| Backend | FastAPI + Uvicorn |
| Frontend | Vanilla HTML + CSS + JS |
| Memory | JSON file (chat_history.json) |
| Profile | JSON file (user_profile.json) |
| Terminal UI | Rich |

---

## 📚 What I Learned

- How LLMs work and why conversation history must be sent every turn
- Building a REST API with FastAPI
- Connecting a browser frontend to a Python backend
- Persistent memory with JSON
- Injecting user context into system prompts
- Environment variable management with python-dotenv

---

## 🔮 Next Steps

- [ ] Add tool use (calculator, web search) → agentic AI
- [ ] Connect MCP servers (Gmail, Google Drive)
- [ ] Add streaming responses in the browser
- [ ] Deploy to cloud (Railway / Render)

---

## 📄 License

MIT — free to use and modify.