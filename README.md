# Research-Navigator

**Research Navigator** is a project designed to automate research tasks using a combination of a FastAPI backend and a sophisticated multi-agent system powered by crewAI. It streamlines the process of gathering, filtering, and synthesizing information based on user queries.

The system leverages specialized AI agents, each responsible for a specific part of the research workflow, from determining query relevance and planning the research approach to retrieving data from various sources (web search, RAG) and synthesizing the final results.

## Features

- **FastAPI Backend:** Provides an API interface for interacting with the research agents (potential future feature).
- **crewAI Integration:** Utilizes a multi-agent framework for complex task decomposition and execution.
- **Modular Agent Design:** Employs distinct agents for relevance checking, research planning, query generation, data retrieval, and synthesis.
- **Asynchronous Operations:** Supports asynchronous tasks like RAG retrieval and web searching for improved performance.
- **Development Tools:** Integrated with `uv`, `ruff` for dependency management, linting, and formatting.

## Installation

Install dependencies using uv:

```bash
make install
# or
uv sync
```

## Running the Application

Run the FastAPI development server:

```bash
make run
# or
uv run fastapi dev --app app --reload
```

## Running the Crew

Run the main crew script directly:

```bash
make run-crew
# or
uv run run_crew
```

## Development Commands

- **Lint:** `make lint` or `uv run ruff check .`
- **Format:** `make format` or `uv run ruff format .`
- **Test:** `make test` or `uv run test`
- **Clean:** `make clean`
- **Build (Docker):** `make build` or `uv run dockerpyze`

## Project Structure

```
.
├── app/                # Main application code (FastAPI, crewAI logic)
│   ├── agents/         # Agent definitions
│   ├── tasks/          # Task definitions
│   ├── tools/          # Custom tools for agents
│   ├── main.py         # FastAPI application entrypoint (if applicable)
│   └── ...
├── tests/              # Unit and integration tests
├── scripts/            # Utility scripts (e.g., run_crew.py)
├── .env.example        # Example environment variables
├── Dockerfile          # Docker configuration
├── Makefile            # Make commands for development tasks
├── pyproject.toml      # Project metadata and dependencies (for uv)
├── ruff.toml           # Ruff linter/formatter configuration
└── README.md           # This file
```

## Agents & Tasks Overview

### Agents

- Relevancy Agent
- Research Agent
- Query Agent
- Retrieval Agent
- Synthesizer Agent

### Tasks

- Is Relevant Question? (Relevancy Agent)
- Create Research Approach (Research Agent)
- Search Query Generation (Dynamic number) (Query Agent)
- RAG Retrieval (Async) (Retrieval Agent)
- Web Search (Async) (Retrieval Agent)
- Keep Relevant Data for Question (Relevancy Agent)
- Summarize Everything (Synthesizer Agent)

## Contributing

Contributions are welcome! Please follow standard fork-and-pull-request workflows. Ensure your code adheres to the project's linting and formatting standards (`make lint` and `make format`).

## License

This project is licensed under the MIT License - see the LICENSE file for details (assuming MIT, add a LICENSE file if needed).
