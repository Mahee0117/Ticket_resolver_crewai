# 🤖 SupportCrew AI

> A CrewAI-based multi-agent customer support system that automatically
> triages customer tickets, classifies their priority, and routes them
> to specialized support agents.

---

## 📌 Project Overview

SupportCrew AI is an AI-powered customer support system built using
**CrewAI**.

The system receives a customer support ticket and uses a dedicated
**Triage Agent** to understand the issue, classify it into a category,
assign a priority, and route the ticket to the appropriate specialist
agent.

Instead of using one general-purpose AI agent for every customer
request, SupportCrew AI uses multiple specialized agents that handle
different types of problems.

### Current workflow

```text
Customer Ticket
      ↓
Triage Agent
      ↓
Structured Triage Result
      ↓
Category Router
      ↓
 ┌──────────┬────────────┬───────────┬──────────┐
 ↓          ↓            ↓           ↓
Billing   Technical    Account     General
Agent      Agent        Agent       Agent
 ↓          ↓            ↓           ↓
Specialist Task
      ↓
Resolution

🎯 Problem Statement

Customer support systems often receive different types of requests:

Payment and billing issues
Login and account problems
Technical errors
General questions
Security-related account issues

A single support agent may not be ideal for handling every type of
request.

SupportCrew AI addresses this by creating a multi-agent support
workflow where each agent has a specific responsibility.

The system first determines:

What type of issue is this?
How urgent is the issue?
Which specialist should handle it?
🧠 How It Works
1. Customer submits a ticket

Example:

I forgot my password and I cannot log into my account.
The password reset email is not arriving.
2. Triage Agent analyzes the ticket

The Triage Agent determines:

Category: Account
Priority: Medium
Issue: Password reset email is not arriving.

The result is returned using a structured Pydantic model.

3. Router selects the specialist

The category determines which specialist agent should handle the ticket.

Billing   → Billing Agent
Technical → Technical Agent
Account   → Account Agent
General   → General Support Agent

Only the relevant specialist is executed for the ticket.

4. Specialist Agent resolves the issue

The selected specialist analyzes the original ticket and generates a
customer-friendly resolution.

For example:

Account Agent
      ↓
Analyze account problem
      ↓
Identify security concerns
      ↓
Provide recommended steps
      ↓
Generate resolution
🤖 Agents
🔎 Triage Agent

Role: Senior Customer Support Triage Specialist

Responsibilities:

Classify customer tickets
Determine ticket category
Assign priority
Summarize the issue
Route the ticket to the appropriate specialist

Supported categories:

Billing
Account
Technical
General

Supported priorities:

Low
Medium
High
Urgent
💳 Billing Agent

Handles:

Payments
Refunds
Duplicate charges
Subscriptions
Billing problems
🛠️ Technical Agent

Handles:

Application crashes
Bugs
Errors
Technical failures
Troubleshooting
👤 Account Agent

Handles:

Login problems
Password issues
Account access
Profile problems
Account security
💬 General Support Agent

Handles:

General questions
Information requests
How-to questions
Basic customer assistance
🏗️ Architecture
Current v1 architecture
                    ┌───────────────────┐
                    │  Customer Ticket  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Triage Agent    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Structured Result │
                    │                   │
                    │ Category          │
                    │ Priority          │
                    │ Issue             │
                    └─────────┬─────────┘
                              │
                              ▼
                       ┌────────────┐
                       │   Router   │
                       └─────┬──────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
      Billing            Technical           Account
       Agent               Agent              Agent
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ▼
                        Resolution
✨ Current Features — v1.0
Multi-Agent Architecture

The project uses multiple specialized CrewAI agents instead of a
single general-purpose agent.

Intelligent Triage

Tickets are classified into:

Billing
Account
Technical
General
Priority Classification

Each ticket receives:

Low
Medium
High
Urgent
Structured Output

Triage results are represented using a Pydantic model:

class TriageResult(BaseModel):
    category: str
    priority: str
    issue: str
Dynamic Routing

The category produced by the Triage Agent determines which specialist
agent is executed.

Multiple Ticket Processing

The system can process multiple customer tickets using a Python
processing loop.

🧪 Example
Input
The application crashes whenever I try to upload a PDF.
Triage
Category : Technical
Priority : High
Issue    : The application crashes whenever I try to upload a PDF.
Routing
Technical
    ↓
Technical Agent
    ↓
Technical Task
    ↓
Resolution
🛠️ Tech Stack
Python
CrewAI
Pydantic
Hugging Face Inference Providers
OpenAI-compatible API
uv
python-dotenv
📁 Project Structure
supportcrew-ai/
│
├── src/
│   └── supportcrew_ai/
│       ├── __init__.py
│       └── main.py
│
├── .env
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md

.env is excluded from version control and should never contain
credentials that are committed to GitHub.

🚀 Running the Project
1. Clone the repository
git clone https://github.com/Mahee0117/Ticket_resolver_crewai.git
cd Ticket_resolver_crewai
2. Create the environment
uv sync
3. Configure environment variables

Create a .env file:

HF_TOKEN=your_huggingface_token
4. Run the application
uv run python src/supportcrew_ai/main.py
📈 Version Roadmap
🟢 v1.0 — Multi-Agent Triage & Routing

Status: Completed

Implemented:

Triage Agent
Billing Agent
Technical Agent
Account Agent
General Support Agent
Multiple ticket processing
Category classification
Priority classification
Pydantic structured output
Category-based routing
Specialist task execution
🔵 v2.0 — Resolution Validation

Planned

Add a dedicated QA Agent that reviews the specialist's response.

Triage
   ↓
Router
   ↓
Specialist
   ↓
Resolution
   ↓
QA Agent
   ↓
 ┌──────────────┐
 │              │
 PASS          FAIL
 │              │
 ▼              ▼
Final       Retry / Escalate
Response
🟣 v3.0 — Human Escalation

Planned

Introduce escalation for:

High-risk security issues
Complex unresolved tickets
Failed QA validation
Issues requiring human intervention
🟠 v4.0 — Agent Tools

Planned

Specialist agents will be able to interact with external tools.

Examples:

get_customer()
get_order()
get_payment()
get_account()
search_logs()

This will allow agents to work with real support data rather than
only analyzing the ticket text.

🔴 v5.0 — RAG Knowledge Base

Planned

Integrate Retrieval-Augmented Generation so agents can retrieve
relevant information from company documentation.

Potential knowledge sources:

FAQ documents
Refund policies
Account recovery documentation
Product documentation
Troubleshooting guides
Ticket
   ↓
Specialist Agent
   ↓
Knowledge Base
   ↓
Relevant Documents
   ↓
Accurate Resolution
🟡 v6.0 — CrewAI Flow

Planned

Move the routing and workflow orchestration into a structured
CrewAI Flow.

Target architecture:

                    CrewAI Flow
                        │
                        ▼
                     Triage
                        │
                        ▼
                     Router
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Billing       Technical      Account
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                    Resolution
                        │
                        ▼
                        QA
🚀 v7.0 — Production Application

Planned

Build a complete application around the agentic backend:

React Frontend
      ↓
FastAPI Backend
      ↓
CrewAI Workflow
      ↓
Agents + Tools + RAG
      ↓
PostgreSQL

Potential additions:

FastAPI
React
PostgreSQL
Authentication
Ticket database
REST APIs
Docker
Testing
Cloud deployment
Monitoring
🧭 Long-Term Vision

The final goal is to evolve SupportCrew AI from a simple
multi-agent routing prototype into a complete AI-powered customer
support platform.

Customer
   ↓
Ticket Intake
   ↓
Triage
   ↓
Priority
   ↓
Routing
   ↓
Specialist Agent
   ↓
Tools + RAG
   ↓
Resolution
   ↓
QA Agent
   ↓
 ┌───────────────┐
 │               │
Approved       Escalate
 │               │
 ▼               ▼
Customer       Human
Response       Support
📚 Learning Journey

This project is also being developed as a hands-on learning journey
with CrewAI.

The project is intentionally being developed incrementally:

Single Agent
     ↓
Multiple Agents
     ↓
Agent Routing
     ↓
Structured Outputs
     ↓
QA
     ↓
Tools
     ↓
RAG
     ↓
Workflow Orchestration
     ↓
Full Application

Each version represents a new stage of understanding and
implementation.

👨‍💻 Author

Mahesh M S K

Computer Science Student
Interested in:

Agentic AI
Multi-Agent Systems
Generative AI
DevOps
Cloud Computing
Full-Stack Development
⭐ Project Status

Current Version: v1.0

🚧 Actively being developed.

The project will evolve through multiple versions as new agentic AI
capabilities are implemented.


### One recommendation

Don't put **everything you're planning to learn** into the current "Features" section. Keep a clear distinction:

- **Implemented** → v1.0
- **Planned** → future versions
- **Long-term vision** → things you may build later

That way, someone visiting your GitHub won't think you already implemented RAG, FastAPI, PostgreSQL, Flow, etc. when you haven't.

For your current repository, **this README + your working v1 code is enough to make the first GitHub milestone.**