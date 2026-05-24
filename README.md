# Salary Management

A full-stack employee salary management application built with FastAPI and React.

## Features

- Browse, search, and filter 10,000 employees by name and country
- View detailed employee profiles in a side panel
- Create, update, and delete employees
- Live salary metrics dashboard — total headcount, average / min / max salary, breakdowns by department and country
- Skeleton loading states and error toasts on every data operation
- Paginated employee list (20 per page)

## Tech Stack

| Layer    | Technology                                          |
|----------|-----------------------------------------------------|
| Backend  | Python 3.14, FastAPI, SQLModel, SQLite, uvicorn     |
| Frontend | React 19, Vite 8, TypeScript, Tailwind v4           |
| UI       | @base-ui/react, lucide-react, sonner                |
| Testing  | pytest + httpx (BE), vitest + @testing-library (FE) |
| Linting  | ruff (BE), eslint + typescript-eslint (FE)          |
| CI       | GitHub Actions                                      |

## Project Structure

```
incubyte-salary-management/
├── backend/
│   ├── app/
│   │   ├── employees/
│   │   │   ├── repository.py   # DB queries
│   │   │   ├── router.py       # FastAPI routes
│   │   │   ├── schemas.py      # Pydantic request/response models
│   │   │   └── service.py      # Business logic
│   │   ├── database.py         # SQLite engine + session factory
│   │   ├── main.py             # App factory, router registration
│   │   └── models.py           # SQLModel table definitions
│   ├── tests/
│   ├── first_names.txt         # 100 first names used by the seeder
│   ├── last_names.txt          # 100 last names used by the seeder
│   └── seed.py                 # Seeds 10,000 employees (idempotent)
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── employees/
│       │   │   ├── EmployeeDetail.tsx   # Detail sheet with edit / delete
│       │   │   ├── EmployeeForm.tsx     # Create / edit form
│       │   │   ├── EmployeeTable.tsx    # Paginated table
│       │   │   └── MetricsPanel.tsx     # Salary metrics sidebar
│       │   └── ui/                      # Shared UI primitives
│       ├── lib/
│       │   └── api.ts                   # Typed API client
│       └── pages/
├── .github/workflows/ci.yml
├── Makefile
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12+ with [uv](https://docs.astral.sh/uv/)
- Node.js 18+ with [pnpm](https://pnpm.io/)

### Install dependencies

```bash
make install
```

### Seed the database

Generates 10,000 employees from `first_names.txt × last_names.txt` in a single atomic transaction. Safe to run multiple times — skips if already seeded.

```bash
make seed
```

### Run locally

```bash
make dev          # starts both servers in parallel
```

- Backend API: http://localhost:8000
- Frontend:    http://localhost:5173
- API docs:    http://localhost:8000/docs

Or start them separately:

```bash
make be-dev       # FastAPI on :8000
make fe-dev       # Vite on :5173
```

## API Reference

| Method | Route                    | Description                             |
|--------|--------------------------|-----------------------------------------|
| GET    | `/api/employees`         | List employees (paginated, filterable)  |
| POST   | `/api/employees`         | Create employee                         |
| GET    | `/api/employees/{id}`    | Get employee by ID                      |
| PUT    | `/api/employees/{id}`    | Update employee                         |
| DELETE | `/api/employees/{id}`    | Delete employee                         |
| GET    | `/api/employees/metrics` | Salary metrics with department/country breakdowns |
| GET    | `/health`                | Health check                            |

### Query parameters for `GET /api/employees`

| Parameter  | Type   | Description              |
|------------|--------|--------------------------|
| `page`     | int    | Page number (default: 1) |
| `page_size`| int    | Items per page (default: 20, max: 100) |
| `name`     | string | Filter by name (case-insensitive partial match) |
| `country`  | string | Filter by country (case-insensitive partial match) |

## Running Tests

```bash
make test           # run all tests (backend + frontend)
make be-test        # backend only
make fe-test        # frontend only
```

## Linting

```bash
make lint           # ruff (BE) + tsc --noEmit (FE)
make be-lint        # backend only
make fe-typecheck   # frontend only
```

## Development Approach

Built with strict TDD — every backend route and frontend component was written test-first, cycling through Red → Green per feature before moving to the next. No implementation code was written without a failing test demanding it.
