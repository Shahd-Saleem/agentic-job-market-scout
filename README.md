# TalentScout AI Agent

TalentScout AI is an intelligent career assistant built with **Python, LangGraph, LangChain, and Google Gemini**.

The agent acts as a conversational technical recruiter that collects a candidate's career preferences, searches for matching job opportunities in the UAE, and analyzes skill gaps between the candidate's profile and available roles.


## Features

- Conversational career profile discovery
- Collects:
  - Industry/field (AI, Data, Software Engineering...)
  - Seniority level (Entry-Level, Mid-Level, Senior)
  - Preferred location (Dubai, Abu Dhabi...)
  - Technical skills
  - Projects
  - Certifications
- Searches for relevant job opportunities
- Calculates job match percentages
- Identifies missing skills for target roles
- Provides skill-gap analysis
- Uses tool calling through Google Gemini
- Maintains multi-turn conversation history
- Uses LangGraph for agent workflow and tool routing
- Focused on UAE technology and professional roles


## How It Works

```text
User
  ↓
TalentScout AI Agent
  ↓
Collect Candidate Profile
  ↓
Gemini Decides Whether a Tool Is Needed
  ↓
LangGraph Tool Routing
  ↓
Job Search / Skill Gap Analysis
  ↓
Tool Results Returned to Agent
  ↓
Personalized Career Response
```

The agent first gathers enough information about the candidate before using its tools.

Once the user's field, skills, and preferred location are available, Gemini can call the appropriate tools to:

- Search for matching jobs
- Analyze missing skills
- Calculate job match percentages

LangGraph controls the workflow between the AI agent and its tools.


## Agent Workflow

The LangGraph workflow contains two main nodes:

### `agent`

Uses Google Gemini to understand the conversation, gather missing candidate information, and decide when tools should be called.

### `tools`

Executes the available career tools and returns the results to the agent.

The workflow follows this structure:

```text
START
  ↓
Agent
  ↓
Tools (if required)
  ↓
Agent
  ↓
Final Response
```

If no tool is required, the agent responds directly.


## Available Tools

### Job Search

Searches the available job dataset for roles that match the candidate's:

- Industry
- Skills
- Seniority
- Location preferences

The agent displays relevant roles along with their calculated match percentages.

### Skill Gap Analysis

Compares the candidate's current technical skills with the skills required for target roles.

The analysis helps identify:

- Matching skills
- Missing skills
- Areas for improvement


## Tech Stack

- **Python** — Core programming language
- **LangGraph** — Agent workflow and state graph orchestration
- **LangChain** — LLM integration, messages, and tool binding
- **Google Gemini** — Language model and tool-calling intelligence
- **Pydantic** — Structured user profile models
- **JSON** — Mock job dataset storage


## Project Structure

```text
agentic-job-market-scout/
│
├── data/
│   └── mock_jobs.json
│
├── src/
│   ├── agent.py
│   ├── state.py
│   └── tools.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

### `agent.py`

Contains the main AI agent and LangGraph workflow. 
Responsibilities include initializing Gemini, defining the TalentScout system prompt, binding tools to the model, creating the LangGraph workflow, routing tool calls, maintaining conversation history, and running the interactive terminal interface.

### `tools.py`

Contains the tools available to the agent, including job searching, skill-gap analysis, and job match calculations.

### `state.py`

Defines the structured candidate profile using Pydantic.

The profile can contain:

```text
Industry
Seniority
Tech Stack
Certifications
Projects
Target Location
```

### `mock_jobs.json`

The project uses a mock job dataset containing technology and professional roles from companies across the UAE.

Example roles include:

- AI Engineering Intern
- Junior Machine Learning Engineer
- Software Engineering Intern
- Technical Product Manager
- Cloud & DevOps Engineer

Each job contains information such as:

```json
{
  "title": "Backend AI Engineering Intern",
  "company": "Talabat",
  "location": "Dubai",
  "required_skills": [
    "Python",
    "LangGraph",
    "RAG"
  ]
}
```


## Installation

Clone the repository:

```bash
git clone https://github.com/Shahd-Saleem/agentic-job-market-scout.git
cd agentic-job-market-scout
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Make sure your `.env` file is included in `.gitignore`:

```text
.env
venv/
__pycache__/
```

## Run the Agent

Run the application from the terminal:

```bash
python src/agent.py
```

The agent will start an interactive conversation:

```text
TalentScout AI is live and interactive!

You: I am looking for entry-level AI engineering jobs in Dubai.

TalentScout AI:
...
```

Type:

```text
exit
```

or:

```text
quit
```

to end the session.


## Disclaimer

The current project uses a mock job dataset for demonstration and development purposes.

Job listings and match percentages should not be treated as live employment opportunities or guaranteed hiring outcomes.

## Author

**Shahd Saleem**
