PACKAGE_NAME := research_navigator
# Define the app directory
APP_DIR := app

install: ## Install dependencies using uv
	uv sync

run: ## Run the FastAPI development server
	uv run fastapi dev --app $(APP_DIR) --reload

run-crew: ## Run the main crew script
	uv run run_crew

test: ## Run the test script
	uv run test

lint: ## Lint the code using Ruff
	uv run ruff check .

format: ## Format the code using Ruff
	uv run ruff format .

clean: ## Clean up build artifacts and cache files
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache .ruff_cache .mypy_cache build dist *.egg-info .coverage htmlcov *.log out/

build:
	uv run dockerpyze

