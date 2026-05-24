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

## TDD Workflow

Every feature follows strict Red → Green → Refactor:

1. **Red** — write the failing test, run it, confirm it fails for the right reason
2. **Green** — write minimal code to make the test pass, run it, confirm it passes
3. **Refactor** — clean up if needed, run tests again to confirm still green

The user commits manually after each Red step and each Green step. **Never auto-commit.**

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
