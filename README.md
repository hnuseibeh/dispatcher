# Zaki-OS: A Multi-Agent Ecosystem

Zaki-OS is a multi-agent ecosystem designed for task processing and automation, featuring a React-based frontend, a FastAPI backend, a PostgreSQL database, and a Retrieval-Augmented Generation (RAG) system to guide agent behavior.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup and Running Zaki-OS](#setup-and-running-zaki-os)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Configure Environment Variables](#2-configure-environment-variables)
  - [3. Build and Run with Docker Compose](#3-build-and-run-with-docker-compose)
- [Accessing the Application](#accessing-the-application)
  - [Web UI](#web-ui)
  - [API Endpoints & Documentation](#api-endpoints--documentation)
- [Key Technologies](#key-technologies)
- [Future Enhancements (Roadmap)](#future-enhancements-roadmap)
- [Contributing](#contributing)
- [License](#license)

## Architecture Overview

Zaki-OS consists of the following main components:

1.  **Frontend (Web UI)**:
    *   A single-page application (SPA) built with React and TypeScript, located in `ui/frontend/`.
    *   Served by an Nginx web server.
    *   Provides user interfaces for task submission, monitoring task progress, viewing task details (including logs, plans, reports), and an agent registry.
    *   Communicates with the Dispatcher API.

2.  **Dispatcher (Backend API)**:
    *   A FastAPI application located in `ui/dispatcher/`.
    *   Provides a RESTful API for the frontend and potentially for direct API clients or other services.
    *   Handles task reception, validation, and storage.
    *   Manages task lifecycle statuses (e.g., pending, approved, in_progress, done).
    *   Provides endpoints for agent registration and subtask dispatching (A2A protocol).
    *   Connects to the PostgreSQL database.

3.  **Agent Runner**:
    *   A Python script (`scripts/agent_runner.py`) responsible for executing tasks.
    *   Fetches approved tasks from the database.
    *   Utilizes the RAG (Retrieval-Augmented Generation) Kernel (`core/rag/`) to fetch relevant information from documents in the `docs/` directory to assist in plan generation.
    *   Generates a `PLAN.md` for each task, which is then set to `pending_approval`.
    *   (Future: Will execute the plan steps once approved and generate a `REPORT.md`).
    *   Connects to the PostgreSQL database.

4.  **Database (PostgreSQL)**:
    *   A PostgreSQL database service managed by Docker Compose.
    *   Stores information about tasks, agents (via `registry_services`), task logs, etc.
    *   The schema is defined in `sql/schema.sql`.

5.  **RAG System (`core/rag/`)**:
    *   Consists of a `VectorStore` (using ChromaDB) and a `RAGKernel`.
    *   Loads, embeds, and indexes documents from the `docs/` directory.
    *   Provides functionality for the Agent Runner to retrieve lessons/documents relevant to a task prompt.

6.  **Docker Orchestration**:
    *   Uses Docker and Docker Compose to build and run all services in a containerized environment.
    *   Configuration is managed via a `.env` file.

## Features

*   Web-based UI for task management and monitoring.
*   API for task submission and system interaction.
*   Agent workflow with plan generation and (soon) automated execution.
*   Automated plan approval mechanism via API.
*   Retrieval-Augmented Generation (RAG) for intelligent plan creation.
*   Agent-to-Agent (A2A) subtask dispatching capability.
*   PostgreSQL database for robust data storage.
*   Containerized deployment using Docker.

## Prerequisites

*   Docker ([Install Docker](https://docs.docker.com/get-docker/))
*   Docker Compose (usually included with Docker Desktop)
*   Git (for cloning the repository)
*   A text editor or IDE for creating the `.env` file.

## Setup and Running Zaki-OS

### 1. Clone the Repository
```bash
git clone <repository_url>
cd <repository_directory_name>
```

### 2. Configure Environment Variables
Create a `.env` file in the root of the project by copying the example below. You can keep the default values or customize them if needed (e.g., if port 5432 is already in use on your host for PostgreSQL).

```env
# .env
POSTGRES_DB=zaki_os_db
POSTGRES_USER=zaki_user
POSTGRES_PASSWORD=zaki_password
DATABASE_URL=postgresql://zaki_user:zaki_password@db:5432/zaki_os_db

# Optional: Override dispatcher API base URL for A2A dispatcher client if needed
# DISPATCHER_API_BASE_URL=http://dispatcher:8000/api
```

### 3. Build and Run with Docker Compose
From the project root directory (where `docker-compose.yml` is located):

```bash
docker-compose up --build -d
```
*   `--build`: Forces Docker to rebuild the images if there are changes (e.g., in Dockerfiles or application code).
*   `-d`: Runs the containers in detached mode (in the background).

To view logs from all services:
```bash
docker-compose logs -f
```
To view logs from a specific service (e.g., `dispatcher`):
```bash
docker-compose logs -f dispatcher
```

To stop the services:
```bash
docker-compose down
```

## Accessing the Application

### Web UI
Once the services are running, the frontend UI should be accessible at:
*   **URL**: `http://localhost:3000`

The UI provides:
*   **Task Dashboard**: View all tasks and their statuses.
*   **Task Submission Form**: Submit new tasks.
*   **Task Detail View**: View details of a specific task (status, logs, plan, report).
*   **Agent Registry**: View registered agents.

*(Placeholder: Add screenshots of the UI here once available.)*

### API Endpoints & Documentation
The Dispatcher API (FastAPI) provides Swagger UI and ReDoc for interactive API documentation:
*   **Swagger UI**: `http://localhost:8000/docs`
*   **ReDoc**: `http://localhost:8000/redoc`

Key API endpoints include:
*   `POST /api/tasks`: Submit a new task.
*   `GET /api/tasks`: List all tasks.
*   `GET /api/tasks/{task_id}`: Get details for a specific task.
*   `POST /api/tasks/{task_id}/approve`: Approve a task's plan.
*   `GET /api/tasks/{task_id}/logs`: Get logs for a task.
*   `POST /api/tasks/{parent_task_id}/subtasks`: Dispatch a subtask.
*   `GET /api/tasks/{parent_task_id}/subtasks_status`: Get statuses of subtasks for a parent task.
*   `GET /api/agents`: List registered agents.

## Key Technologies

*   **Frontend**: React, TypeScript, Material-UI (or Ant Design - assuming MUI for now)
*   **Backend**: Python, FastAPI, Pydantic
*   **Database**: PostgreSQL
*   **Vector Store (for RAG)**: ChromaDB
*   **Embeddings (for RAG)**: Sentence Transformers
*   **Containerization**: Docker, Docker Compose
*   **A2A Communication**: REST APIs

## Future Enhancements (Roadmap)
*   Full implementation of agent execution logic after plan approval.
*   Real-time log streaming to the UI.
*   User authentication and authorization.
*   More sophisticated agent capabilities and a wider variety of agents.
*   Enhanced A2A protocol with more complex interaction patterns.
*   UI for managing RAG documents/knowledge base.
*   Scalability improvements for handling a larger number of agents and tasks.
*   Comprehensive test suite (unit, integration, e2e).

## Contributing
(Placeholder: Add contribution guidelines if this were an open project.)

## License
(Placeholder: Specify a license, e.g., MIT License.)
