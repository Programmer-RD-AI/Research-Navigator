# Research-Navigator

Research Navigator: A FastAPI backend and crewAI setup for research tasks.

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
