# 🏆 EdgeMarket Sports Prediction Agent

An AI-powered sports and events forecasting backend for [EdgeMarket.ai](https://edgemarket.ai) — a decentralized prediction market platform. The agent uses real-time web search to generate probabilistic predictions on sports matches, elections, crypto prices, and other verifiable world events.

---

## 🧠 How It Works

The agent is built on the [Agno](https://github.com/agno-agi/agno) framework and powered by **GPT-4.1 Mini**. It:

1. Accepts a user query about an upcoming event or match
2. Performs multiple real-time web and news searches
3. Returns a structured prediction with probability, confidence level, and key factors
4. Persists conversation history in **MongoDB** for multi-turn context

The API is served via **FastAPI** with streaming support, so responses are delivered token-by-token as the agent reasons.

---

## 📁 Project Structure

```
.
├── agent.py      # Agent definition (model, tools, DB, instructions)
├── main.py       # FastAPI app with /chat streaming endpoint
├── .env          # Environment variables (not committed)
└── requirements.txt
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-org/edgemarket-agent.git
cd edgemarket-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
MONGO_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/
OPENAI_API_KEY=sk-...
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## 🔌 API Reference

### `POST /chat`

Streams the agent's prediction response.

**Request Body**

```json
{
  "query": "Who will win the PSG vs Barcelona Champions League match?",
  "session_id": "optional-uuid-for-continuity",
  "user_id": "optional-user-identifier"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | string | ✅ | The prediction question |
| `session_id` | string | ❌ | Resume a previous session; auto-generated if omitted |
| `user_id` | string | ❌ | Associate the session with a user |

**Response**

- Content-Type: `text/plain` (streamed)
- Header: `X-Session-ID` — the session ID used (useful if you let the server generate it)

**Example cURL**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Will Real Madrid win La Liga this season?"}' \
  --no-buffer
```

**Example Response (streamed)**

```
Prediction: Real Madrid wins La Liga
Probability: 65-72%
Confidence: Med
Key Factors:
Current 4-point lead with 8 games remaining
Strongest squad depth in the league
Barcelona injury concerns in midfield
```

---

## 🤖 Agent Behavior

The agent is scoped **strictly** to prediction market topics:

✅ **In scope**
- Sports match outcomes (football, basketball, cricket, tennis, etc.)
- Prediction market events (elections, crypto price targets, world events on EdgeMarket)
- Odds, probabilities, and forecasts for verifiable events

❌ **Out of scope** — responds with:
> "I can only assist with prediction market forecasts on EdgeMarket.ai"

### Output Format

Every in-scope response follows this structure:

```
Prediction: <outcome>
Probability: <XX% or XX-YY% range>
Confidence: <Low / Med / High>
Key Factors:
<Factor 1>
<Factor 2>
<Factor 3>
```

---

## 🗄️ Session Persistence

Conversation history is stored in **MongoDB** under the `edgemarket` database, `agent_sessions` collection. The agent uses the last **2 conversation turns** as context for follow-up questions.

Each unique `session_id` maps to an independent conversation thread.

---

## 🛡️ CORS Configuration

The server allows requests from:

- `https://edgemarket.ai` (production)
- `http://localhost:5174` (local development)

To add more origins, update `allow_origins` in `main.py`.

---

## 🧩 Tech Stack

| Component | Technology |
|---|---|
| Agent Framework | [Agno](https://github.com/agno-agi/agno) |
| LLM | OpenAI GPT-4.1 Mini |
| Web Search | Agno `WebSearchTools` |
| Database | MongoDB (via `agno.db.mongo`) |
| API Server | FastAPI |
| Streaming | `StreamingResponse` (FastAPI) |

---

## 📄 License

MIT © EdgeMarket.ai