.PHONY: install test lint typecheck demo mcp api docker

install:
	python -m pip install -U pip
	pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check src tests

typecheck:
	mypy src

demo:
	agentic-lab run-demo --provider mock

mcp:
	python -m agentic_lab.mcp_server

api:
	uvicorn agentic_lab.api:app --host 0.0.0.0 --port 8080

docker:
	docker compose up --build
