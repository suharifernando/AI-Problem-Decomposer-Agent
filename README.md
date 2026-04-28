# 🤖 AI Problem Decomposer + Self Improving Agent

A distinction level AI agent that demonstrates **reasoning**, **planning**, **reflection**, and **goal-based improvement** using the Groq API.

---

## 🧠 How It Works

```
User Input
    │
    ▼
┌─────────────────────────────────┐
│  Stage 1: DECOMPOSE             │  agent.decompose()
│  Break problem into 6–8 steps   │  → Planning
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│  Stage 2: SELF-CRITIQUE         │  agent.critique()
│  Analyze its own steps          │  → Reflection
│  Find gaps and weaknesses       │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│  Stage 3: IMPROVE               │  agent.improve()
│  Generate better plan           │  → Goal-based action
│  Addressing all critiques       │
└─────────────────────────────────┘
              │
              ▼
         Final Output
```

This is real AI agent behaviour:
- ✅ **Reasoning** — structured thinking at each stage
- ✅ **Memory** — state shared across all three stages via `AgentMemory`
- ✅ **Reflection** — the agent evaluates its own output
- ✅ **Goal-based action** — improvement is driven by critique goals

---

## 📁 Project Structure

```
ai-agent/
│
├── app.py          # Entry point — run this
├── agent.py        # Core agent logic (3 stages)
├── memory.py       # Agent memory (stores state between stages)
├── prompts.py      # System prompts for each stage
├── .env            # Your API key (never commit this)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your Groq API key

Get a free key at [console.groq.com](https://console.groq.com), then edit `.env`:

```
GROQ_API_KEY=your_actual_key_here
```

### 3. Run the agent

```bash
# Interactive mode — it will ask for your problem
python app.py

# Or pass the problem directly as an argument
python app.py "Build a mobile app for food delivery"
python app.py "Launch a startup in 90 days"
python app.py "Create an e-commerce website"
```

---

## 💡 Example Output

```
Problem: Build a website

🧩  Step Decomposition
────────────────────────────────────────────────────────────
  01. Define the website's purpose, target audience, and goals
  02. Choose a tech stack (HTML/CSS/JS, React, WordPress, etc.)
  03. Design wireframes and UI mockups
  04. Develop the frontend interface
  05. Develop backend and database if needed
  06. Deploy to a hosting provider

🔍  Self-Critique
────────────────────────────────────────────────────────────
  ⚠  Missing testing and QA phase before deployment
  ⚠  No mention of SEO or performance optimisation
  ⚠  Steps lack timeline or milestones
  ⚠  No content creation or copywriting step

✨  Improved Plan
────────────────────────────────────────────────────────────
  01. Define purpose, audience, and SMART goals with deadlines
  02. Research competitors and create a sitemap
  03. Choose tech stack based on requirements and budget
  04. Write all content and copy before design begins
  05. Design wireframes, then high-fidelity mockups
  06. Develop frontend with accessibility in mind
  07. Develop backend and connect database
  08. Write and run unit + integration tests
  09. Optimise for SEO, page speed, and mobile
  10. Deploy to hosting with CI/CD pipeline
  11. Monitor analytics and gather user feedback
```

---

## 🔧 Customisation

**Change the AI model** — edit `agent.py`:
```python
MODEL = "llama-3.3-70b-versatile"   # default
MODEL = "mixtral-8x7b-32768"        # alternative
MODEL = "gemma2-9b-it"              # lighter model
```

**Adjust prompts** — edit `prompts.py` to change how each stage behaves.

**Extend memory** — add new fields in `memory.py` (e.g. timestamps, confidence scores).

---

## 📚 Assignment Mapping

| AI Concept        | Where It Appears                         |
|-------------------|------------------------------------------|
| Reasoning         | All three LLM calls use structured prompts |
| Planning          | `agent.decompose()` — Stage 1            |
| Memory            | `AgentMemory` class in `memory.py`       |
| Reflection        | `agent.critique()` — Stage 2             |
| Goal-based action | `agent.improve()` — Stage 3             |
