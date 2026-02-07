.PHONY: help
PYTHON ?= /usr/local/bin/python3.14

help:
	@echo "Usage:"
	@echo "  make dev                Run the package with developer settings"
	@echo "  make prod               Run the pacakge with production settings"
	@echo "  make test               CI: Run tests"
	@echo "  make cov                CI: Run test and calculate coverage"
	@echo "  make check              CI: Lint the code"
	@echo "  make format             CI: Format the code"
	@echo "  make type               CI: Check typing"
	@echo "  make doc                Run local documentation server"
	@echo "  make build              Build the package wheel before publishing to Pypi"
	@echo "  make publish            Publish package to Pypi"
	@echo "  make dockerbuild        Build the docker image"
	@echo "  make dockerrun          Run the docker image"
	@echo "  make allci              Run all CI steps (check, format, type, test coverage)"
	@echo "  make install            Install the package and its dependencies"

install:
	rm -rf .venv
	uv venv --python $(PYTHON)
	uv pip install --upgrade --requirement requirements.txt

dev:
	uv run  python_boilerplate execute --starting-index 26087598 --ending-index 26087811

dev-anchor:
	uv run  python_boilerplate execute-anchor
prod:
	uv run modern_python_boilerplate

test:
	uv run pytest -s tests/

cov:
	uv sync --group test
	uv run pytest --cov=src/python_boilerplate tests/ --cov-report=term-missing

check:
	uv run ruff check $$(git diff --name-only --cached -- '*.py')

format:
	uv run ruff format $$(git diff --name-only --cached -- '*.py')

type:
	uv run mypy .

doc:
	uvx --with mkdocstrings  --with mkdocs-material --with mkdocstrings-python --with mkdocs-include-markdown-plugin mkdocs serve

build:
	uv build

publish:
	uv publish

dockerbuild:
	docker build

allci:
	$(MAKE) check
	$(MAKE) format
	$(MAKE) type
	$(MAKE) cov

fix-all:
	uv run ruff check --fix-only
	uv run ruff format
	uv run mypy .

docker-shell:
	@docker rm -f $$(docker ps -q --filter ancestor=selenium/standalone-chrome:latest) 2>/dev/null || true
	docker run --platform linux/amd64 -d -p 4444:4444 -p 7900:7900 --shm-size="2g" -e SE_NODE_MAX_SESSIONS=20 -e SE_NODE_OVERRIDE_MAX_SESSIONS=true selenium/standalone-chrome:latest
	docker compose run app bash