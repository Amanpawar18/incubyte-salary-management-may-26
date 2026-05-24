# Salary Management — Claude Code Instructions

## Project Structure

```
incubyte-salary-management/
├── backend/          # FastAPI + SQLModel (Python, uv)
│   ├── app/
│   │   ├── main.py       # FastAPI app factory
│   │   ├── models.py     # SQLModel table definitions
│   │   └── database.py   # SQLite engine + get_session
│   └── tests/
├── frontend/         # React 19 + Vite 8 + Tailwind v4 + @base-ui/react (pnpm)
│   └── src/
│       ├── components/
│       ├── pages/
│       └── test/
├── .github/workflows/ci.yml
├── Makefile
└── CLAUDE.md
```

## File Creation Rule

Only create files and directories when they are directly needed for the current TDD step. Never pre-scaffold future directories or stub files before their task begins.

## Minimal Green Rule

In the Green step, write only the code needed to make the current failing tests pass. Do not implement methods, routes, or logic that have no failing test yet — those belong in the next Red → Green cycle.

## TDD Workflow — Full-Stack Cycle Per Feature

Each feature (e.g. "list employees", "create employee") goes through this exact sequence before moving to the next feature:

```
1. BE Red    — write failing backend test(s), run, confirm they fail
2. BE Green  — write minimal backend code to pass only those tests, run, confirm green
3. FE Red    — write failing frontend test(s), run, confirm they fail
4. FE Green  — implement frontend component + wire to backend API, run, confirm green
5. Smoke     — start both servers, hit the endpoint manually in the browser
```

The user commits manually after each Red and each Green step. **Never auto-commit.**

### TDD Rules (critical — never break these)

- **One feature at a time.** Complete all 5 steps for one feature before starting the next.
- **Green means minimal.** Only write code that makes the current failing tests pass. Ask: "Is there a failing test that requires this?" If not — do not write it.
- **Never write implementation ahead of the test.** No method, route, or component exists until its Red test exists first.
- **Never write tests for future features.** Only write tests for the current feature.

### What "minimal" means in practice

| Current failing tests | What to implement | What NOT to implement |
|---|---|---|
| POST /api/employees | `create` + POST route only | GET, PUT, DELETE routes |
| GET /api/employees | `list_paginated` + GET route only | GET /{id}, PUT, DELETE |
| GET /api/employees/{id} | `get_by_id` + GET /{id} route only | PUT, DELETE |

## Commit Rules

- **Never** run `git add -A` or `git add .` — always stage specific files by name
- **Never** auto-commit — the user runs `git commit` themselves
- **Never** skip pre-commit hooks (`--no-verify`)
- Commit message format: `type: description` (e.g., `feat: add health check test`, `fix: handle empty salary list`)

## Package Management

### Backend — uv
```bash
uv sync --all-groups          # install all deps
uv add <package>              # add runtime dep
uv add --dev <package>        # add dev dep
uv run pytest                 # run tests
uv run uvicorn app.main:app --reload  # dev server
uv run ruff check .           # lint
```

### Frontend — pnpm (always pnpm, never npm or yarn)
```bash
pnpm install                  # install deps
pnpm dev                      # dev server
pnpm test                     # run tests
pnpm exec tsc --noEmit        # typecheck
pnpm add <package>            # add runtime dep
pnpm add -D <package>         # add dev dep
```

## CI Notes

- pnpm is pinned to `version: "10"` in CI (`pnpm/action-setup@v4`) — do not change to `latest`
- pnpm v10 reads `"pnpm": { "onlyBuiltDependencies": [...] }` from `package.json`
- pnpm v11 ignores the `"pnpm"` field in `package.json` — this is why we pin v10
- msw is a transitive dep via `vitest → @vitest/mocker → msw` and cannot be removed; it is approved via `"pnpm": { "onlyBuiltDependencies": ["msw"] }` in `frontend/package.json`
- pnpm supply-chain policy blocks packages published within 24 hours — if install fails with `ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION`, check if a direct dep was recently published and pin it to an older stable version
- Backend pytest uses `|| [ $? -eq 5 ]` to handle exit code 5 (no tests collected) without breaking CI

## Makefile Quick Reference

```bash
make be-dev       # backend dev server
make fe-dev       # frontend dev server
make dev          # both servers in parallel
make be-test      # backend tests
make fe-test      # frontend tests
make test         # all tests
make be-lint      # backend lint
make fe-typecheck # frontend typecheck
make install      # install all deps
```

## Tech Stack

| Layer     | Technology                                      |
|-----------|-------------------------------------------------|
| Backend   | Python 3.14, FastAPI, SQLModel, SQLite, uvicorn |
| Frontend  | React 19, Vite 8, TypeScript, Tailwind v4       |
| UI        | @base-ui/react, lucide-react                    |
| Testing   | pytest + httpx (BE), vitest + @testing-library (FE) |
| Linting   | ruff (BE), eslint + typescript-eslint (FE)      |
| CI        | GitHub Actions                                  |

## Path Aliases

Frontend uses `@/` → `src/`:
```typescript
import { Button } from '@/components/button'
```

## Environment

- Backend runs on `http://localhost:8000`
- Frontend dev server runs on `http://localhost:5173`
- Frontend proxies API calls to the backend — configure in `vite.config.ts` if needed
