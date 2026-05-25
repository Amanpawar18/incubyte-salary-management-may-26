# Prompts & AI Collaboration Log

This document records the key prompts and instructions given to Claude Code (claude-sonnet-4-6) via the Superpowers plugin throughout development.

---

## Phase 1: Brainstorming & Design

**Prompt used to kick off the project:**

> "I need to build a salary management tool as part of a technical assessment. The tool manages 10,000 employees for an HR manager persona. Requirements: full CRUD on employees (full name, job title, country, salary, any other meaningful data), salary insights (min/max/avg by country, avg salary for a given job title in a country), seed script using first_names.txt and last_names.txt, ReactJS frontend, FastAPI backend, SQLite, component library of choice."

The `superpowers:brainstorming` skill guided a structured Q&A covering:
- Component library → chose @base-ui/react + Tailwind v4 (headless, no class conflicts with Tailwind)
- Layout → single-page 30/70 sidebar (metrics left, employee table right)
- ORM strategy → SQLModel for unified model + schema, avoids duplicating Pydantic models
- Test strategy → pytest + httpx (BE), vitest + RTL (FE), in-memory SQLite per test for full isolation

Output saved to `docs/superpowers/specs/2026-05-23-salary-management-design.md`.

---

## Phase 2: Implementation Plan

**Prompt:**
> "Write an implementation plan for the design we just created."

The `superpowers:writing-plans` skill produced `docs/superpowers/plans/2026-05-23-salary-management.md` — a task-by-task TDD plan covering all features with exact file paths, full code blocks, and expected test output at each step.

---

## Phase 3: Feature execution (TDD Red → Green)

Each feature was implemented following the Red → Green cycle. Representative prompts:

- **Health check:** `"Let's start — run task 1 of the plan."`
- **POST /api/employees:** `"BE Red for create employee."`
- **GET /api/employees (paginated):** `"Next feature — list employees with pagination, name search, country filter."`
- **Employee detail + edit + delete:** `"Next"` (repeated after each user push)
- **Salary metrics:** `"Let's add salary metrics."`
- **Seed script:** `"Seed script with 10,000 employees. Full names generated from first_names.txt × last_names.txt. Assume engineers run this regularly — performance matters."`

Claude Code read the plan file, marked tasks in-progress, wrote the failing test, confirmed failure, wrote the minimal implementation, confirmed green, then reported the commit message. The user ran `git commit` manually after each Red and each Green step.

---

## Phase 4: Bug fixes (selected)

**react-hooks/set-state-in-effect lint error:**
> "Error: Calling setState synchronously within an effect [...] Avoid calling setState() directly within an effect. Analyse the error and find the correct solution."

Claude diagnosed that `setData` was being called synchronously in the `useEffect` body. The fix: make `fetchEmployees` return the raw Promise and call `setData` in `.then()` in the effect — satisfying the rule while keeping the same behaviour.

**TypeScript error with z.coerce.number() and useForm:**
> "Type 'Resolver<{...salary: unknown...}>' is not assignable to type 'Resolver<{...salary: number...}>'"

Claude identified that `z.coerce.number()` causes Zod's input type (before coercion) to be `unknown` while the output type is `number`. Fix: use `z.input<typeof schema>` and `z.output<typeof schema>` as separate types, pass `useForm<EmployeeFormInput, unknown, EmployeeFormData>`.

**Seed script produced 9,898 rows instead of 10,000:**
> "The seed produced 9898 rows — first_names.txt had 101 entries and last_names.txt had 98. Fix the name files."

Claude counted both files, removed one first name and added two last names to reach exactly 100 × 100 = 10,000 combinations.

**Table text cropping:**
> "Table is still getting cropped — it should be responsive. Let's add text trim as well."

Claude applied `table-fixed` to the Table component, `truncate max-w-0` to long-text cells, and explicit percentage column widths summing to 100%.

---

## Phase 5: Gap analysis & follow-up plan

**Prompt:**
> "Review the current implementation and git logs and confirm if everything is correctly developed and implemented from the assignment details."

Claude cross-referenced every requirement against the commit history and running code. Identified two functional gaps (per-country min/max salary, job-title-in-country lookup) and three missing artifact docs, then wrote a new plan (`docs/superpowers/plans/2026-05-25-salary-insights-and-docs.md`) to close them.

Execution followed the same Red → Green discipline — one step at a time, user tests and pushes between each step.
