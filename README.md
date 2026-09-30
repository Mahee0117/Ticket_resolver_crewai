# 🤖 SupportCrew AI

### Multi-Agent Customer Support & Ticket Resolution System

> An AI-powered customer support system built with **CrewAI** that
> automatically understands, classifies, routes, and resolves customer
> support tickets using specialized AI agents.

---

## 🚀 What is SupportCrew AI?

Traditional support systems often send every customer request to the
same support workflow.

**SupportCrew AI takes a multi-agent approach.**

A dedicated **Triage Agent** first analyzes the ticket, determines its
category and priority, and routes it to the appropriate specialist.

```mermaid
flowchart LR

    A[🎫 Customer Ticket] --> B[🧠 Triage Agent]

    B --> C{Category}

    C -->|Billing| D[💳 Billing Agent]
    C -->|Technical| E[🛠️ Technical Agent]
    C -->|Account| F[👤 Account Agent]
    C -->|General| G[💬 General Support Agent]

    D --> H[✅ Resolution]
    E --> H
    F --> H
    G --> H
✨ Current Version — v1.0
Multi-Agent Triage & Routing

Implemented:

🧠 AI-powered ticket triage
🏷️ Automatic category classification
🚦 Priority classification
🔀 Category-based agent routing
🤖 Specialized support agents
📦 Pydantic structured outputs
🎫 Multiple ticket processing
💬 Customer-friendly resolutions
🤖 Agent Architecture
Agent	Responsibility
🧠 Triage Agent	Classifies tickets and assigns priority
💳 Billing Agent	Payments, refunds, duplicate charges & subscriptions
🛠️ Technical Agent	Bugs, crashes, errors & troubleshooting
👤 Account Agent	Login, passwords, profiles & account security
💬 General Support Agent	General questions & information requests
🔄 How It Works
1️⃣ Customer submits a ticket
"The application crashes whenever I try to upload a PDF."
2️⃣ Triage Agent analyzes it
Category : Technical
Priority : High
Issue    : Application crashes during PDF upload
3️⃣ Router selects the specialist
Technical
    ↓
Technical Agent
    ↓
Technical Task
    ↓
Resolution

Only the relevant specialist agent is executed.

🧠 Structured Triage

Instead of relying on unstructured AI text, the triage result is
represented using Pydantic:

class TriageResult(BaseModel):
    category: str
    priority: str
    issue: str

This allows the application to make deterministic routing decisions
from the AI's output.

                 Triage Result
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
       Category    Priority      Issue
          │
          ↓
        Router
🛠️ Tech Stack
Technology	Purpose
🐍 Python	Core application
🤖 CrewAI	Multi-agent orchestration
🧩 Pydantic	Structured agent outputs
🤗 Hugging Face	LLM inference
📦 uv	Python environment & dependency management
🔐 python-dotenv	Environment configuration
📂 Project Structure
supportcrew-ai/
│
├── src/
│   └── supportcrew_ai/
│       ├── __init__.py
│       └── main.py
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
🚀 Getting Started
1. Clone the repository
git clone https://github.com/Mahee0117/Ticket_resolver_crewai.git

cd Ticket_resolver_crewai
2. Install dependencies
uv sync
3. Configure environment variables

Create a .env file:

HF_TOKEN=your_huggingface_token

⚠️ Never commit your .env file or API keys to GitHub.

4. Run
uv run python src/supportcrew_ai/main.py
🧪 Example
Input
Someone has gained unauthorized access to my account
and I can see transactions that I did not make.
Triage
Category : Account
Priority : Urgent
Routing
Account
   ↓
Account Agent
   ↓
Security Analysis
   ↓
Resolution
📈 Development Roadmap
✅ v1.0 — Multi-Agent Routing

Completed

Ticket
  ↓
Triage
  ↓
Structured Output
  ↓
Routing
  ↓
Specialist
  ↓
Resolution
🔜 v2.0 — QA & Validation

Planned

Add a dedicated QA Agent to review specialist responses.

Specialist
    ↓
Resolution
    ↓
QA Agent
   ↙   ↘
PASS   FAIL
 ↓      ↓
Final  Retry / Escalate
🔜 v3.0 — Human Escalation

Introduce human-in-the-loop escalation for:

Critical security issues
Failed resolutions
Complex customer problems
Low-confidence responses
🔜 v4.0 — Tools

Give agents access to real support operations:

get_customer()
get_order()
get_payment()
get_account()
search_logs()
🔜 v5.0 — RAG Knowledge Base

Allow agents to retrieve information from:

Product documentation
FAQs
Refund policies
Troubleshooting guides
Internal support documentation
Ticket
  ↓
Specialist Agent
  ↓
Knowledge Base
  ↓
Relevant Information
  ↓
Resolution
🔜 v6.0 — CrewAI Flow

Move the overall workflow orchestration into CrewAI Flow.

                 CrewAI Flow
                     │
                   Triage
                     │
                   Router
                ↙    ↓    ↘
          Billing Technical Account
                \     |     /
                 Resolution
                     │
                     QA
🔜 v7.0 — Production Application

Future architecture:

┌──────────────────┐
│  React Frontend  │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  FastAPI Backend │
└────────┬─────────┘
         ↓
┌──────────────────┐
│   CrewAI Flow    │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Agents + Tools   │
│      + RAG       │
└────────┬─────────┘
         ↓
┌──────────────────┐
│   PostgreSQL     │
└──────────────────┘
🎯 Long-Term Vision

The goal is to evolve SupportCrew AI from a multi-agent routing
prototype into a complete AI-powered customer support platform.

Customer
   ↓
Ticket Intake
   ↓
Triage
   ↓
Priority
   ↓
Specialist Routing
   ↓
Tools + RAG
   ↓
Resolution
   ↓
Quality Check
   ↓
┌──────────────┐
│              │
▼              ▼
Resolved     Human
             Escalation
📚 Development Approach

This project is being developed incrementally to understand and
implement agentic AI concepts step by step.

Single Agent
     ↓
Multi-Agent
     ↓
Routing
     ↓
Structured Outputs
     ↓
QA
     ↓
Tools
     ↓
RAG
     ↓
CrewAI Flow
     ↓
Production Application

Each version represents a new stage of the system.

👨‍💻 Author
Mahesh M S K

Computer Science Student | Agentic AI | DevOps | Cloud | Full-Stack

⭐ SupportCrew AI is actively being developed.

Current Version: v1.0


### Why this will look much better

Your current README has huge blocks of text like:

```text
Customer Ticket
      ↓
Triage Agent
      ↓
Structured Triage Result
...