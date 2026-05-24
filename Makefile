.PHONY: install dev test lint be-dev fe-dev be-test fe-test be-lint fe-typecheck seed

install:
	cd backend && uv sync --all-groups
	cd frontend && pnpm install

be-dev:
	cd backend && uv run uvicorn app.main:app --reload

fe-dev:
	cd frontend && pnpm dev

dev:
	$(MAKE) -j2 be-dev fe-dev

be-test:
	cd backend && uv run pytest --cov=app --cov-report=term-missing

fe-test:
	cd frontend && pnpm test

test: be-test fe-test

be-lint:
	cd backend && uv run ruff check .

fe-typecheck:
	cd frontend && pnpm exec tsc --noEmit

lint: be-lint fe-typecheck

seed:
	cd backend && uv run python seed.py
