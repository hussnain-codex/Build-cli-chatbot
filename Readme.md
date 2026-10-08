# 🤖 Multi-Provider CLI AI Chatbot

A terminal-based AI chatbot built with **Python and LangChain** that can switch between multiple AI providers — **Groq, Google Gemini, and local Ollama**.

The chatbot supports **streaming responses, conversation memory, provider switching, and saving/loading conversations** directly from the terminal.

---

## 🚀 Project Goal

The goal of this project is to build a practical CLI chatbot that can:

* Switch between **Groq, Gemini, and Ollama**
* Use one command-line flag to select the provider
* Stream AI responses in real time
* Remember the current conversation
* Switch providers during a conversation
* Save conversations to JSON
* Load previous conversations
* Clear conversation memory
* Delete saved conversations
* Use LangChain and LCEL for the chatbot pipeline

---

## ✨ Features

### 🔌 Multiple AI Providers

The chatbot supports three providers:

| Provider | Type  | API Required |
| -------- | ----- | ------------ |
| Groq     | Cloud | ✅            |
| Gemini   | Cloud | ✅            |
| Ollama   | Local | ❌            |

You can select the provider when starting the chatbot:

```bash
python main.py --provider groq
```

```bash
python main.py --provider gemini
```

```bash
python main.py --provider ollama
```

---

### ⚡ Streaming Responses

AI responses are streamed token-by-token instead of waiting for the complete response.

Example:

```text
You: Explain APIs

AI: An API is a way for two software applications
to communicate with each other...
```

This makes the chatbot feel more like a real AI application.

---

### 🧠 Conversation Memory

The chatbot remembers previous messages during the current session.

Example:

```text
You: My name is Hussnain.

AI: Nice to meet you, Hussnain!

You: What is my name?

AI: Your name is Hussnain.
```

Conversation history is maintained using LangChain message objects:

* `HumanMessage`
* `AIMessage`

---

### 🔄 Runtime Provider Switching

You can change the AI provider without restarting the chatbot.

```text
/model groq
```

```text
/model gemini
```

```text
/model ollama
```

Check the current provider:

```text
/model
```

---

### 💾 Save Conversation

Save the current conversation:

```text
/save
```

This creates:

```text
conversation.json
```

---

### 📂 Load Conversation

Load a previously saved conversation:

```text
/load
```

The saved messages are restored into the chatbot's memory.

---

### 🧹 Clear Memory

Clear the current conversation:

```text
/clear
```

This removes the conversation from the current program memory.

It does **not** delete `conversation.json`.

---

### 🗑️ Delete Saved Conversation

Delete the saved JSON conversation:

```text
/delete
```

This deletes:

```text
conversation.json
```

It does not automatically clear the current in-memory conversation.

---

## 🏗️ Architecture

The project follows a simple multi-provider architecture:

```text
                    ┌───────────────────┐
                    │    CLI Chatbot    │
                    │     main.py       │
                    └─────────┬─────────┘
                              │
                       --provider flag
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
          ┌──────┐        ┌────────┐       ┌────────┐
          │ Groq │        │ Gemini │       │ Ollama │
          └──┬───┘        └───┬────┘       └───┬────┘
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                         LangChain
                              │
                              ▼
                            LCEL
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
             Prompt                    History
                 │                         │
                 └────────────┬────────────┘
                              ▼
                           LLM Call
                              │
                              ▼
                          Streaming
                              │
                              ▼
                           Terminal
```

---

## 🛠️ Technologies Used

### Programming Language

* Python

### AI / LLM Framework

* LangChain
* LCEL

### AI Providers

* Groq
* Google Gemini
* Ollama

### Environment Management

* `python-dotenv`

### Data Storage

* JSON

### CLI

* Python `argparse`

---

## 📁 Project Structure

```text
Build-cli-chatbot/
│
├── .venv/
│
├── main.py
├── .env
├── .gitignore
├── conversation.json
├── README.md
└── NOTES.md
```

### Important Files

#### `main.py`

Main chatbot application containing:

* Provider configuration
* LangChain setup
* LCEL pipeline
* Conversation memory
* Streaming
* Commands
* Save/load functionality

#### `.env`

Stores API keys.

Example:

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

> Never upload `.env` to GitHub.

#### `conversation.json`

Stores saved conversations.

This file is generated when `/save` is used.

#### `NOTES.md`

Contains learning notes about concepts such as:

* Temperature
* Streaming
* Context windows
* LangChain
* LCEL
* Provider differences

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Build-cli-chatbot.git
```

Move into the project:

```bash
cd Build-cli-chatbot
```

---

## 2. Create Virtual Environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If activation is blocked by PowerShell policy, you can use:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

Install the required packages:

```bash
pip install langchain langchain-groq langchain-google-genai langchain-ollama python-dotenv
```

---

# 🔑 API Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

### Groq

The project currently uses:

```text
openai/gpt-oss-20b
```

through the Groq provider.

### Gemini

The project currently uses:

```text
gemini-2.5-flash
```

### Ollama

Ollama runs locally, so an API key is not required.

The project currently uses:

```text
llama3.2
```

---

# 🦙 Ollama Setup

Install Ollama on your computer.

Then download the model:

```bash
ollama pull llama3.2
```

Check available models:

```bash
ollama list
```

Test Ollama:

```bash
ollama run llama3.2
```

If the model responds, Ollama is ready.

Then run the chatbot:

```bash
python main.py --provider ollama
```

---

# ▶️ Running the Chatbot

## Groq

```bash
python main.py --provider groq
```

## Gemini

```bash
python main.py --provider gemini
```

## Ollama

```bash
python main.py --provider ollama
```

If no provider is specified, the default provider is:

```text
Groq
```

So you can also run:

```bash
python main.py
```

---

# 💻 Available Commands

Inside the chatbot:

| Command         | Description                       |
| --------------- | --------------------------------- |
| `/model`        | Show current provider             |
| `/model groq`   | Switch to Groq                    |
| `/model gemini` | Switch to Gemini                  |
| `/model ollama` | Switch to Ollama                  |
| `/clear`        | Clear current conversation memory |
| `/save`         | Save conversation to JSON         |
| `/load`         | Load saved conversation           |
| `/delete`       | Delete saved JSON conversation    |
| `exit`          | Exit chatbot                      |

---

# 🧪 Example Session

```text
==================================================
           MULTI-PROVIDER AI CHATBOT
==================================================
Current provider: groq

Commands:
/model              → Show current provider
/model groq         → Switch to Groq
/model gemini       → Switch to Gemini
/model ollama       → Switch to Ollama
/clear              → Clear current memory
/save               → Save conversation to JSON
/load               → Load conversation from JSON
/delete             → Delete saved JSON only
exit                → Exit chatbot

You: My name is Hussnain.

AI: Nice to meet you, Hussnain!

You: What is Python?

AI: Python is a high-level programming language...

You: /model

Current provider: groq

You: /model ollama

Switched to ollama

You: What is my name?

AI: Your name is Hussnain.
```

---

# 🔗 LCEL Pipeline

The chatbot uses LangChain Expression Language (LCEL).

The basic pipeline is:

```text
User Question
      ↓
ChatPromptTemplate
      ↓
Conversation History
      ↓
Selected LLM
      ↓
StrOutputParser
      ↓
Streaming Response
      ↓
Terminal
```

In code:

```python
chain = prompt | llm | parser_output
```

This demonstrates the core LangChain pipeline concept.

---

# 🧠 Conversation Memory

The chatbot maintains conversation history using:

```python
HumanMessage
AIMessage
```

The prompt uses:

```python
MessagesPlaceholder(variable_name="history")
```

This allows previous messages to be inserted into the prompt.

Example:

```python
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI assistant."
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])
```

---

# 🌡️ Temperature

The chatbot uses:

```python
temperature=0.7
```

Temperature controls how predictable or creative the AI response can be.

### Temperature 0

```text
More predictable
Less variation
```

### Temperature 0.7

```text
Balanced
Good for general conversation
```

### Temperature 1.5

```text
More creative
More variation
```

---

# 🔐 Security

API keys should **never** be hardcoded inside Python files.

Use:

```text
.env
```

instead.

The `.gitignore` file should contain:

```gitignore
.venv/
.env
__pycache__/
*.pyc
conversation.json
```

This prevents sensitive information and local files from being committed to GitHub.

---

# 🎯 Learning Outcomes

This project helped build practical understanding of:

### Python

* Functions
* Lists
* Loops
* Exception handling
* JSON
* Environment variables
* Command-line arguments
* File handling

### APIs

* API authentication
* Sending messages
* Receiving responses
* Streaming responses
* Token usage
* Provider differences

### LangChain

* Chat models
* `ChatGroq`
* `ChatGoogleGenerativeAI`
* `ChatOllama`
* Messages
* Prompt templates
* `MessagesPlaceholder`
* `StrOutputParser`
* LCEL
* `.invoke()`
* `.stream()`

### AI Engineering

* Multi-provider architecture
* Conversation memory
* Model switching
* Local LLMs
* Cloud LLMs
* CLI application design
* Environment/security practices

---

# 📈 Development Roadmap

## ✅ Completed

* [x] Raw Groq API
* [x] System + user messages
* [x] Token usage
* [x] Chat loop
* [x] Conversation memory
* [x] Streaming
* [x] Temperature testing
* [x] Context management basics
* [x] LangChain integration
* [x] Groq integration
* [x] Gemini integration
* [x] Ollama integration
* [x] Provider flag
* [x] Runtime provider switching
* [x] LCEL pipeline
* [x] Save conversation
* [x] Load conversation
* [x] Clear memory
* [x] Delete saved conversation

## 🔜 Future Improvements

* [ ] Automatic provider fallback
* [ ] Better retry handling
* [ ] Context-window management
* [ ] Conversation summarization
* [ ] Better CLI interface
* [ ] Rich terminal formatting
* [ ] Token/cost tracking
* [ ] Multiple conversation files
* [ ] Conversation history database
* [ ] Unit tests
* [ ] Configuration file
* [ ] Logging system
* [ ] Production-ready error handling

---

# 🚨 Troubleshooting

## Groq API Key Error

If you see:

```text
GROQ_API_KEY not found in .env
```

Check that `.env` exists in the project root:

```text
Build-cli-chatbot/
├── main.py
└── .env
```

And contains:

```env
GROQ_API_KEY=your_key
```

---

## Gemini API Key Error

Make sure `.env` contains:

```env
GOOGLE_API_KEY=your_key
```

Then restart the terminal.

---

## Ollama Model Not Found

If you see:

```text
model 'llama3.2' not found
```

Run:

```bash
ollama pull llama3.2
```

Then verify:

```bash
ollama list
```

---

## PowerShell Cannot Activate Virtual Environment

Try:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then:

```powershell
.venv\Scripts\Activate.ps1
```

---

# 📌 Important Notes

### `/delete` vs `\delete`

The chatbot commands use a forward slash:

```text
/delete
```

Not:

```text
\delete
```

The backslash version will be treated as a normal user message.

---

# 📜 License

This project is created for **learning, experimentation, and AI engineering practice**.

You are free to modify and extend the project for your own learning and development.

---

# 👨‍💻 Author

**Hussnain Naeem**

Full Stack Developer & AI Engineering Learner

### Skills explored in this project

```text
Python
LangChain
LCEL
Groq
Google Gemini
Ollama
REST APIs
CLI Applications
AI Engineering
```

---

## ⭐ If You Like This Project

Give the repository a ⭐ on GitHub and feel free to improve the project with new providers, better memory, tools, agents, and production-ready features.

---

## 🚀 Next Step

The next major improvement for this project is:

```text
User Request
     ↓
Current Provider
     ↓
   ERROR?
    /   \
  No     Yes
  ↓       ↓
Answer   Fallback
          ↓
       Ollama
          ↓
        Answer
```

This will make the chatbot more reliable by automatically switching to another provider when the selected provider fails.
