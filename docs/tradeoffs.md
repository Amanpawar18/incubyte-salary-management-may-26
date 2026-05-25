# Architectural Trade-offs

## SQLite over PostgreSQL

**Chosen:** SQLite via SQLModel.

SQLite requires zero infrastructure — no server process, no connection string secrets, no Docker service. For a 10,000-row dataset with a single writer at a time, it is more than sufficient and dramatically simplifies local setup (`make seed` just works).

**Trade-off:** SQLite serialises all writes. Under concurrent mutation load (many parallel POSTs) it becomes a bottleneck. The migration path is a one-line change to the engine URL in `database.py` — SQLModel/SQLAlchemy abstracts everything else.

---

## SQLModel over raw SQLAlchemy

**Chosen:** SQLModel (SQLAlchemy + Pydantic v2 unified).

A single class definition serves as both the database table and the root for API schemas. Less duplication, fewer synchronisation bugs between ORM models and Pydantic schemas.

**Trade-off:** SQLModel adds a layer of magic (metaclass tricks, auto-`__tablename__`). Stack traces at the ORM level are deeper and harder to read. Mitigated by keeping `models.py` simple and placing all query logic in `repository.py`, which is plain Python.

---

## Bulk INSERT for seeding over ORM session.add()

**Chosen:** `session.execute(sa_insert(Employee), batch)` in batches of 500, wrapped in a single transaction.

Calling `session.add(employee)` for 10,000 employees triggers 10,000 round-trips plus 10,000 INSERTs. SQLAlchemy's `insert()` with a list of dicts compiles one statement per batch.

**Trade-off:** Bypasses ORM-level hooks and does not auto-populate server-side defaults via `RETURNING`. Worked around by computing `created_at`/`updated_at` in Python before building the row dicts.

Result: 10,000 rows seeded in ~0.27 s.

---

## Single `Employee` table — no separate `Department` or `Country` table

**Chosen:** Department and country are plain string columns on `Employee`.

The scope is read-heavy analytics on a flat employee list. Normalising into `departments` and `countries` tables would require joins on every aggregate query and add FK constraints to manage in tests, with no real benefit since departments are never updated independently.

**Trade-off:** Typos in department names cause silent splits in metrics (e.g. "Enginering" vs "Engineering"). Acceptable for this scope; a production system would use a FK to a `departments` table with an enum or lookup.

---

## useCallback + .then() for data fetching

**Chosen:** `fetchEmployees` is a `useCallback` returning the raw Promise. `setData` is called inside `.then()` in the `useEffect` body, never synchronously.

React 19's `eslint-plugin-react-hooks` v7 introduced `react-hooks/set-state-in-effect`, which flags synchronous `setState` calls inside `useEffect` bodies to prevent cascading render chains.

**Trade-off:** More verbose than a simple `useEffect(() => { fetchData().then(setData) }, [])`. Requires wrapping the fetch callback in `useCallback` and being deliberate about dependency arrays. Upside: compatible with strict-mode double-invocation and future React concurrent features.

---

## No client-side state management library

**Chosen:** All state lives in `App.tsx`, passed down as props.

One page, one primary data domain (employees). Introducing Redux, Zustand, or React Query would add dependency weight and conceptual overhead for no real benefit at this scale.

**Trade-off:** `App.tsx` is ~150 lines. If a second route or data domain were added, the React Context API or a lightweight store (Zustand) would be the right next step.

---

## Layered backend architecture (router → service → repository)

**Chosen:** Three explicit layers instead of putting query logic directly in route handlers.

Keeps each layer testable in isolation: repository can be tested with a real session, service with a mock repository, and routes via the FastAPI TestClient. FastAPI handlers stay thin — they only validate input and format output.

**Trade-off:** More files and indirection for a small app. Justified because the test suite caught several real bugs (duplicate email on update, route ordering with `/metrics` vs `/{id}`) that would have been harder to isolate in a monolithic handler.
