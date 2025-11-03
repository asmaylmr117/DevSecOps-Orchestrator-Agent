#  ACIP DevSecOps Orchestrator Agent (Phase 1 Deliverable)

This repository contains the initial implementation of the **DevSecOps Orchestrator Agent (Layer 1)**, a core component of the Advanced Cybersecurity Intelligence Platform (ACIP). This agent is responsible for automating the critical process of **vulnerability prioritization** and ticket creation.

---

##  Phase 1 Success Summary

This deliverable successfully establishes the intelligent backend logic for the DevSecOps Dashboard.

### Key Achievements
* **State Machine Built:** The entire workflow is modeled as a robust, stateful graph using **LangGraph**.
* **Intelligence Core:** The **Prioritization Agent** implements the core **Risk-Scoring Algorithm** to convert raw security data into actionable severity scores.
* **Integration Ready:** The service is fully containerized and exposes an API endpoint for command delegation from the Master Orchestrator.

##  Architectural & Tech Stack

| Component | Technology / Framework | Role in Implementation |
| :--- | :--- | :--- |
| **Logic Core (MAS)** | **Python 3.10+** (LangGraph, Pydantic) | Builds the agent state machine and manages complex task flow. |
| **Prioritization Agent** | Custom Python Functionality | Implements the **Risk-Scoring Algorithm**. |
| **JIRA Integration** | **Python Requests Library** | Handles external API calls to create tickets. |
| **Distribution** | **Docker** & **Docker Compose** | Containerizes the agent as an independent Microservice. |

---

##  Execution Guide (How to Run the Service)

### Prerequisites
1.  **Docker Desktop:** Must be installed and running (ensuring WSL 2 is enabled).
2.  **Required Libraries:** (LangGraph, pytest, requests) are listed in `requirements.txt`.

### Step 1: running
Execute this command in the root directory of the project (`ACIP_Project/`):

```bash
docker build -t acip-devsecops-orchestrator .

```bash
tests:
  python -m pytest devsecops_module/tests/

docker:
  docker build -t acip-devsecops-orchestrator .
  docker compose up -d

langgraph_studio:
  # install langgraph-cli
   python -m pip install langgraph-cli
  # Windows
  C:\Users\GooGle\AppData\Local\Programs\Python\Python311\Scripts\langgraph.exe dev
  # or (cross-platform)
  python -m langgraph dev
