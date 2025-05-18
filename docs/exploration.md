# 💡 AI Financial Assistant — Model–Compute–Plan (MCP) Architecture

This project is a modular, intelligent assistant that analyzes bank statements, extracts insights, and suggests personalized financial optimizations using an emerging **Model–Compute–Plan (MCP)** pattern.

---

## 🧠 What is MCP?

**Model–Compute–Plan (MCP)** is a modern AI architecture pattern for intelligent agents:

| Component | Description |
|----------|-------------|
| **Model**  | Uses an LLM to understand queries and generate reasoning |
| **Compute**| Executes actions (query data, categorize, summarize) |
| **Plan**   | Orchestrates the flow — decides what to do next |

This structure helps you build intelligent systems that are **modular**, **explainable**, and **scalable**.

---


## 🏗️ Project Structure (Phase 1)

```
ai_finance_mcp/
├── main.py                   # FastAPI app with `/ask` endpoint
├── .env                      # Holds OpenAI API key
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation

├── agent/
│   ├── llm_model.py          # Handles GPT-4o calls (Model)
│   ├── planner.py            # Orchestrates steps (Plan)
│   └── executor.py           # Performs analysis (Compute)

├── data/
│   └── graph_db.py           # Mock Neo4j/Snowflake interface

├── prompts/
│   ├── summarize.prompt      # Prompt template for summarization
│   └── optimize.prompt       # Prompt for financial advice
```


## 🚀 Running the App

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your OpenAI key

Create a `.env` file:

```env
OPENAI_API_KEY=your-openai-key-here
```

### 3. Start the FastAPI server

```bash
uvicorn main:app --reload
```


## 📡 Using the `/ask` Endpoint

Once running, you can ask financial questions:

```http
GET /ask?q=How can I reduce my monthly spending?
```

Example response:

```json
{
  "response": "Consider reducing dining expenses by 20% and canceling unused subscriptions."
}
```


## 📌 Phase Roadmap

### ✅ Phase 1: Core Framework

- [x] Modular architecture (Model–Compute–Plan)
- [x] FastAPI interface
- [x] GPT-4o integration
- [x] Mock executor + planner logic

### 🔜 Phase 2: Real Graph + Memory

- [ ] Connect to Neo4j and query real data
- [ ] Replace executor mock with real transaction queries
- [ ] Add session-based memory (LangGraph / CrewAI)
- [ ] Support multi-turn conversation context